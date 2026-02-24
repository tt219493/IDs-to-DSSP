`ids-to-dssp.pdb`
===
```Python
def ids_to_pdb_download(ids: list[str], output_dir_path: str, verbose: bool = False, file_format: str = 'mmCif') -> list[str]:
    '''
    Given a list of PDB IDs, download the associated files from RCSB PDB to a given output directory.

    Parameters
    ----------
    ids : list[str] 
        List of PDB IDs to download data for
    output_dir_path : str
        Path to directory to store downloaded files
    verbose : bool = False
        Changes verbose setting for `PDBList()`
    file_format: bool = False
        Changes file output setting for `PDBList()`

    
    Returns
    -------
    list[str]
        List containing paths to all downloaded files

    '''


def process_entry(entry: dict) -> dict:
    '''
    Helper function for `id_to_sequences`. Takes in one entry given by DataQuery from RCSB API and returns a dict of `sequence`, `length`, `strand_id`, and `type` 
    
    Parameters
    ----------
    entry : dict
        Dictionary pertaining to related information for a polymer from RCSB PDB

    
    Returns
    -------
    list[str]
        Dictionary with information that can be readily converted to DataFrame


    '''

def ids_to_sequences(ids: list[str], use_lazy: bool = True, use_concurrency: bool = False, max_workers: int = 2, chunk_size: int = 50) -> pl.LazyFrame | pl.DataFrame:
    '''
    Given a list of PDB IDs, return Polars LazyFrame or DataFrame with `id`, `rcsb_id`, `sequence`, `length`, `strand_id`, and `type` 
     Uses default config settings for RCSB API query.

    Parameters
    ----------
    ids : list[str] 
        List of PDB IDs to download data for
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
        Contains `id`, `rcsb_id`, `sequence`, `length`, `strand_id`, and `type` 

    '''
```
    
    


