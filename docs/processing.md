`ids_to_dssp.processing`
===
```Python
def ids_to_df(path_to_ids: str, use_lazy : bool = True, ids_only : bool = False, is_parquet : bool = False) -> pl.LazyFrame | pl.DataFrame | list[str]:
    '''
    Returns a Polars LazyFrame or DataFrame given a path to a TSV or parquet file containing PDB IDs.
    Assumes file contains header labeled `id` and formatted as `{pdb_id}_{amino_acid}_{index}` 
    where `pdb_id` is 4 character ID and `amino_acid` is 3 character abbreviation.

    Parameters
    ----------
    path_to_ids : str 
        Path to TSV file
    use_lazy : bool = True
        Returns LazyFrame if set to True and DataFrame if set to False
    ids_only : bool = False
        Returns list of unique IDs if set to True and includes everything if set to False
    is_parquet: bool = False
        Use `pl.scan_csv()` if False or `pl.scan_parquet()` if True

    
    Returns
    -------
    LazyFrame | DataFrame | list[str]
        LazyFrame or DataFrame containing information from the TSV file or list[str] if ids_only = True

    '''

def df_to_output(df: pl.LazyFrame | pl.DataFrame, path_to_output_dir: str, output_name: str, is_formatted: bool = True, 
                 use_rcsb_id : bool = False, only_secondary_structure: bool = False, to_parquet: bool = False) -> None:
    '''
    Given a Polars LazyFrame or DataFrame with `id`, `amino_acid`, and `index`, output a TSV or Parquet file containing the data in the format used as the file input.
    Currently, it will also output all other columns present in the Frame.

    Parameters
    ----------
    df : pl.LazyFrame | pl.DataFrame
        Frame to output to file
    path_to_output_dir : str 
        Path to output directory
    output_name : str
        Name of outputted file
    is_formatted : bool = True
        Output file will have IDs formatted as `{pdb_id}_{amino_acid}_{index}` if True and will remain separate if False. 
    use_rcsb_id : bool = False
        Output with 4 letter ID if False and RCSB ID (4 letter with sequence ID) if True. Only works if `is_formatted=True` 
    only_secondary_structure : bool = False
        Output with all columns present if False and only secondary structure if True. Only works if `is_formatted=True`
    to_parquet : bool = False
        Output file will be TSV if False and Parquet if false
    
    Returns
    -------
    None
    '''
    id = 'rcsb_id' if use_rcsb_id else 'id'

    if is_formatted:
        df = (df.with_columns(pl.concat_str([pl.col(id),
                                            pl.col("amino_acid"),
                                            pl.col("index")],
                                            separator="_").alias('id'))
                .drop('amino_acid', 'index'))
        if use_rcsb_id:
            df = df.drop(id)
        if only_secondary_structure:
            df = df.select('id', 'secondary_structure')
    
    if type(df) == pl.LazyFrame:
        df = df.collect()

    if not to_parquet:
        df.write_csv(os.path.join(path_to_output_dir, f"{output_name}.tsv"), separator='\t')
    else:
        df.write_parquet(os.path.join(path_to_output_dir, f"{output_name}.parquet"))

def df_to_fasta(df: pl.LazyFrame | pl.DataFrame, path_to_output_dir: str, output_name: str, use_rcsb_id : bool = False) -> None:
    '''
    Given a Polars LazyFrame or DataFrame with `id` and `sequence`, output Fasta file containing the ids and sequences

    Parameters
    ----------
    df : pl.LazyFrame | pl.DataFrame
        Frame to output to file
    path_to_output_dir : str 
        Path to output directory
    output_name : str
        Name of outputted file
    use_rcsb_id : bool = False
        Output with 4 letter ID if False and RCSB ID (4 letter with sequence ID) if True
    
    Returns
    -------
    None
    '''
    id = 'rcsb_id' if use_rcsb_id else 'id'
    df = (df.with_columns(pl.concat_str(
                            [
                                pl.lit(">"),
                                pl.col(id),
                                pl.lit("\n"),
                                pl.col("sequence"),
                                pl.lit("\n"),
                            ],
                            separator="").alias("output")
                    ).select("output").unique("output").sort("output"))
    
    if type(df) == pl.LazyFrame:
        df = df.collect()
    
    with open(os.path.join(path_to_output_dir, f'{output_name}.fasta'), 'w') as f:
        for row in df.iter_rows(named=True):
            f.write(row['output'])


def combine_to_full(df1: pl.LazyFrame | pl.DataFrame, df2: pl.LazyFrame | pl.DataFrame, 
                   use_lazy: bool = True) -> pl.LazyFrame | pl.DataFrame:
    '''
    Given two Lazy or DataFrames, with sharing columns `id`, `strand_id` 
    with one having `secondary_structure`, `index`, and `amino_acid` and the other with `sequence` and `length`,
    join into one Lazy or DataFrame

    Parameters
    ----------
    df1 : pl.LazyFrame | pl.DataFrame
        First DataFrame to join
    df2: pl.LazyFrame | pl.DataFrame
        Second DataFrame to join
    use_lazy : bool = True
        Combine and output as LazyFrames
    
    Returns
    -------
    None
    '''    

```
