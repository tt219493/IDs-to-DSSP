import rs_dssp
import polars as pl 

three_letter ={'V':'VAL', 'I':'ILE', 'L':'LEU', 'E':'GLU', 'Q':'GLN', \
'D':'ASP', 'N':'ASN', 'H':'HIS', 'W':'TRP', 'F':'PHE', 'Y':'TYR',    \
'R':'ARG', 'K':'LYS', 'S':'SER', 'T':'THR', 'M':'MET', 'A':'ALA',    \
'G':'GLY', 'P':'PRO', 'C':'CYS'}

def files_to_dssp(files: list[str], use_lazy: bool = True, use_three_letter: bool = True, 
                  num_threads: int = 0) -> pl.LazyFrame | pl.DataFrame:
    '''
    Given a list of PDB IDs, return Polars LazyFrame or DataFrame with `id`, `amino_acid` `index`, `secondary_structure`, `strand_id`.  
    Uses rs-dssp implementation from https://pypi.org/project/rs-dssp/


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
    
    Returns
    -------
    Polars LazyFrame or DataFrame
        Contains `id`, `amino_acid` `index`, `secondary_structure`, `strand_id`
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
            'index': seq_id_list,
            'secondary_structure': secondary_structure_list,
            'strand_id': strand_id_list,
        })

    df = (pl.LazyFrame(dict_list).explode(['amino_acid', 'index', 'secondary_structure', 'strand_id'])
            .with_columns(
                secondary_structure=pl.when(pl.col('secondary_structure')==' ')
                                      .then(pl.lit('.'))
                                      .otherwise(pl.col('secondary_structure'))))
    if use_three_letter:
        df = df.with_columns(amino_acid = pl.col('amino_acid').replace(three_letter))

    if not use_lazy:
        df = df.collect()

    return df
