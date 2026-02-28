`ids_to_dssp.rs_dssp`
===
```Python
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
```
