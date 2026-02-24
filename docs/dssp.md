`ids_to_dssp.dssp` 
===
**Requirement:** install `mkdssp` from https://github.com/PDB-REDO/dssp

```Python
def process_file(file_path : str) -> dict:
    '''
    Helper function for `files_to_dssp`. 
    Takes path to mmCif file and uses mkdssp to get info regarding amino acids, index, secondary structure, and strand id and return as a dict
    
    Parameters
    ----------
    file_path:
        path to one mmCif file
    
    Returns
    -------
    dict
    Contains amino acid, index, secondary structure, and strand id data 

    '''

def files_to_dssp(files: list[str], use_lazy: bool = True, use_concurrency: bool = False, 
                     max_workers: int = 2, chunk_size: int = 50) -> pl.LazyFrame | pl.DataFrame:
    '''
    Given a list of PDB IDs, return Polars LazyFrame or DataFrame with `id`, `rcsb_id`, `sequence`, `length`, `strand_id`, and `type` 

    Parameters
    ----------
    files : list[str] 
        List of file paths to get DSSP data for
    use_lazy : bool = True
        Returns LazyFrame if set to True and DataFrame if set to False
    use_concurrency: bool = False
        Turn on concurrency for faster processsing
    max_workers : int = 2
        CPU workers to use for concurrency
    chunk_size : int = 50
        Chunk size to use in concurrency
    
    Returns
    -------
    Polars LazyFrame or DataFrame
        Contains `id`, `amino_acid` `index`, `secondary_structure`, `strand_id`
    '''
```