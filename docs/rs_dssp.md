`ids_to_dssp.rs_dssp`
===
```Python
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
```
