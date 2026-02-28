import rs_dssp
import polars as pl 
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from concurrent.futures import ProcessPoolExecutor

three_letter ={'V':'VAL', 'I':'ILE', 'L':'LEU', 'E':'GLU', 'Q':'GLN', \
'D':'ASP', 'N':'ASN', 'H':'HIS', 'W':'TRP', 'F':'PHE', 'Y':'TYR',    \
'R':'ARG', 'K':'LYS', 'S':'SER', 'T':'THR', 'M':'MET', 'A':'ALA',    \
'G':'GLY', 'P':'PRO', 'C':'CYS'}

def files_to_dssp(files: list[str], use_lazy: bool = True, use_three_letter: bool = True, 
                  num_threads: int = 0, num_workers: int = 2) -> pl.LazyFrame | pl.DataFrame:
    '''
    Given a list of PDB IDs, return Polars LazyFrame or DataFrame with `id`, `amino_acid` `index`, `secondary_structure`, `strand_id`.  
    Uses rs-dssp implementation from https://pypi.org/project/rs-dssp/.

    Unfortunately, requires Bio parsing all files to properly align the returned indices.


    Parameters
    ----------
    files : list[str] 
        List of file paths to get DSSP data for
    use_lazy : bool = True
        Returns LazyFrame if set to True and DataFrame if set to False
    use_three_letter : bool = True
        Returns `amino_acid` in three letter code if True and one letter code if False
    num_threads : int = 0
        Number of threads to use for `rs_dssp`. Default of 0 is auto. 
    num_workers: int = 2
        Number of workers to use for MMCIF2Dict Concurrency
    
    Returns
    -------
    Polars LazyFrame or DataFrame
        Contains `id`, `amino_acid` `index`, `secondary_structure`, `strand_id`, 'asym_id`
    '''

    dict_list = []
    ids = [file_path.split('/')[-1].split('.')[0].upper() for file_path in files]
    result = rs_dssp.assign_batch(files, n_threads=num_threads)

    for id, seq in zip(ids, result):
        aa_list = []
        seq_id_list = []
        secondary_structure_list = []
        strand_id_list = []

        for res in seq.residues:
            aa_list.append(res.amino_acid)
            seq_id_list.append(res.seq_id)
            secondary_structure_list.append(res.structure)
            strand_id_list.append(res.chain_id)

    dict_list.append({
        'id': id,
        'amino_acid': aa_list,
        'pdb_seq_num': seq_id_list,
        'secondary_structure': secondary_structure_list,
        'strand_id': strand_id_list,
    })
    df = (pl.LazyFrame(dict_list).explode(['amino_acid', 'pdb_seq_num', 'secondary_structure', 'strand_id'])
            .with_columns(
                secondary_structure=pl.when(pl.col('secondary_structure')==' ')
                                      .then(pl.lit('.'))
                                      .otherwise(pl.col('secondary_structure'))))
    if use_three_letter:
        df = df.with_columns(amino_acid = pl.col('amino_acid').replace(three_letter))

    def process_file(args):
        id, file = args
        temp_dict = MMCIF2Dict(file)
        return {
            'id': id,
            'asym_id': temp_dict['_pdbx_poly_seq_scheme.asym_id'], 
            'strand_id': temp_dict['_pdbx_poly_seq_scheme.pdb_strand_id'],
            'pdb_seq_num': temp_dict['_pdbx_poly_seq_scheme.pdb_seq_num'],
            'index': temp_dict['_pdbx_poly_seq_scheme.seq_id']
        }

    bio_dict_list = []

    with ProcessPoolExecutor(max_workers=2) as executor:
        bio_dict_list = list(
            executor.map(process_file, zip(ids, files))
        )

    bio_df = (pl.LazyFrame(bio_dict_list).explode(['strand_id', 'pdb_seq_num', 'index'])
                                            .cast({
                                                'index': pl.Int64,
                                                'pdb_seq_num': pl.Int64,
                                            }))
    
    df = bio_df.join(df, on=['pdb_seq_num', 'strand_id'], how='left'
                     ).with_columns(pl.col('secondary_structure').fill_null(' ')).drop('pdb_seq_num')

    if not use_lazy:
        df = df.collect()

    return df
