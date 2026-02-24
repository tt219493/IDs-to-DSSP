from ids_to_dssp.pdb.pdb import *
from ids_to_dssp.dssp.mkdssp import *
from ids_to_dssp.processing.df import *
import polars as pl

def ids_to_ss(input_path: str, download_path: str, parquet_input: bool = False) -> pl.LazyFrame:
    '''
    Given IDs in file, return a LazyFrame with all secondary structures for given IDs. 
    LazyFrame output will be enforced for efficiency.
    
    Parameters
    ----------
    input_path: str
        Path to file 
    download_path: str
        Path to directory where all mmCif files will be downloaded
    parquet_input: bool = False
        Set whether the input is a parquet or TSV
    
    Returns
    -------
    pl.LazyFrame
    Contains amino acid, index, secondary structure, and strand id data 

    '''
    id_list = ids_to_df(input_path, ids_only=True, is_parquet=parquet_input)
    file_list = ids_to_pdb_download(id_list, download_path)
    return files_to_dssp(file_list)


def ids_to_ss_output(input_path: str, download_path: str, output_path: str, output_name: str, 
                     parquet_input: bool = False, parquet_output: bool = False, 
                     is_formatted: bool = True, only_secondary_structure: bool = False) -> None:
    '''
    Given IDs in file, save output of secondary structure to file 
    
    Parameters
    ----------
    input_path: str
        Path to file 
    download_path: str
        Path to directory where all mmCif files will be downloaded
    output_path: str
        Path to directory where output file will be stored
    output_name : str
        Name of output file
    parquet_input: bool = False
        Set whether the input is a parquet or TSV
    parquet_output: bool = False
        Set whether the output is a parquet or TSV
    is_formatted : bool = True
        Output file will have IDs formatted as `{pdb_id}_{amino_acid}_{index}` if True and will remain separate if False. 
    only_secondary_structure: bool = False
        Set whether output will only contain `id` and `secondary_structure`. Only works if `is_formatted = True`
 
    Returns
    -------
    None

    '''
    df = ids_to_ss(input_path, parquet_input)
    df_to_output(df, output_path, output_name, is_formatted=is_formatted, 
                 only_secondary_structure=only_secondary_structure, to_parquet=parquet_output)
    
def ids_to_seq(input_path: str, parquet_input: bool = False) -> pl.LazyFrame:
    '''
    Given IDs in file, return a LazyFrame with all sequences for given IDs. 
    LazyFrame output will be enforced for efficiency.
    
    Parameters
    ----------
    input_path: str
        Path to file 
    parquet_input: bool = False
        Set whether the input is a parquet or TSV
    
    Returns
    -------
    pl.LazyFrame

    '''
    id_list = ids_to_df(input_path, ids_only=True, is_parquet=parquet_input)
    return ids_to_sequences(id_list)

def ids_to_seq_output(input_path : str, output_path: str, output_name: str, 
                      parquet_output: bool = False, fasta_ouput: bool = False,
                     is_formatted: bool = True, use_rcsb_id: bool = False) -> None:
    '''
    Given a list of PDB IDs, save output or fasta containing sequences

    Parameters
    ----------
    input_path: str
        Path to file 
    output_path: str
        Path to directory where output file will be stored
    output_name : str
        Name of output file
    parquet_output: bool = False
        Set whether the output is a parquet or TSV
    fasta_output: bool = False
        Set whether the output is a fasta. Takes priority over `parquet_output`
    is_formatted : bool = True
        Output file will have IDs formatted as `{pdb_id}_{amino_acid}_{index}` if True and will remain separate if False. 
    use_rcsb_id : bool = False
        Output with 4 letter ID if False and RCSB ID (4 letter with sequence ID) if True. Only works if `is_formatted=True` 
 
    Returns
    -------
    None
    '''
    df = ids_to_seq(input_path, parquet_input)
    if fasta_ouput:
        df_to_fasta(df, output_path, output_name, use_rcsb_id)
    else:
        df_to_output(df, output_path, output_name, is_formatted=is_formatted, use_rcsb_id=use_rcsb_id,
                    to_parquet=parquet_output)

def ids_to_full(input_path: str, download_path: str, parquet_input: bool = False) -> pl.LazyFrame:
    '''
    Given IDs in file, return a LazyFrame with full information
    
    Parameters
    ----------
    input_path: str
        Path to file 
    download_path: str
        Path to directory where all mmCif files will be downloaded
    parquet_input: bool = False
        Set whether the input is a parquet or TSV
    
    Returns
    -------
    pl.LazyFrame

    '''

    ss_df = ids_to_ss(input_path, download_path, parquet_input)
    seq_df = ids_to_seq(input_path, parquet_input)
    return combine_to_full(ss_df, seq_df)

def ids_to_full_output(input_path : str, download_path: str, output_path: str, output_name: str, 
                       parquet_input: bool = False, parquet_output: bool = False,
                       is_formatted: bool = True, use_rcsb_id: bool = False) -> None:
    '''
    Given a list of PDB IDs, save output to TSV or paquet containing full information

    Parameters
    ----------
    input_path: str
        Path to file 
    download_path: str
        Path to directory where all mmCif files will be downloaded
    output_path: str
        Path to directory where output file will be stored
    output_name : str
        Name of output file
    parquet_input: bool = False
        Set whether the input is a parquet or TSV
    parquet_output: bool = False
        Set whether the output is a parquet or TSV
    is_formatted : bool = True
        Output file will have IDs formatted as `{pdb_id}_{amino_acid}_{index}` if True and will remain separate if False. 
    use_rcsb_id : bool = False
        Output with 4 letter ID if False and RCSB ID (4 letter with sequence ID) if True. Only works if `is_formatted=True` 
 
    Returns
    -------
    None
    '''
    df = ids_to_full(input_path, download_path, parquet_input)
    df_to_output(df, output_path, output_name, is_formatted=is_formatted, use_rcsb_id=use_rcsb_id,
                    to_parquet=parquet_output)



     