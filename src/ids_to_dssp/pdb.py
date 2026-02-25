from Bio.PDB.PDBList import PDBList
import os
from rcsbapi.data import DataQuery as Query
import polars as pl
from concurrent.futures import ProcessPoolExecutor


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
    pdb_list = PDBList(verbose=verbose)
    pdb_list.download_pdb_files(ids, pdir=output_dir_path, file_format=file_format)

    return [entry.path for entry in os.scandir(output_dir_path)]


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
    entities = entry['polymer_entities']
    return {
        'id'       : entry['rcsb_id'],

        'rcsb_id'  : ([(e['rcsb_id'])
                    for e in entities]),

        'sequence' : ([(e['entity_poly']
                        ['pdbx_seq_one_letter_code_can'])
                    for e in entities]),

        'length'   :([(e['entity_poly']
                        ['rcsb_sample_sequence_length'])
                    for e in entities]),

        'strand_id'  : ([(e['rcsb_polymer_entity_container_identifiers']
                        ['auth_asym_ids'])
                        for e in entities]),

        'type'     : ([(e['entity_poly']
                        ['rcsb_entity_polymer_type'])
                    for e in entities]),

    }

def ids_to_sequences(ids: list[str], use_lazy: bool = True, use_concurrency: bool = False, max_workers: int = 2, chunk_size: int = 50) -> pl.LazyFrame | pl.DataFrame:
    '''
    Given a list of PDB IDs, return Polars LazyFrame or DataFrame with `id`, `rcsb_id`, `sequence`, `length`, `strand_id`
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
        Contains `id`, `rcsb_id`, `sequence`, `length`, `strand_id`

    '''

    query = Query(
        input_type="entries",
        input_ids=ids,
        return_data_list=[
            "polymer_entities.rcsb_id",
            "polymer_entities.entity_poly.pdbx_seq_one_letter_code_can",
            "polymer_entities.entity_poly.rcsb_entity_polymer_type",
            "polymer_entities.entity_poly.rcsb_sample_sequence_length",
            "polymer_entities.rcsb_polymer_entity_container_identifiers.auth_asym_ids",
    ])

    query.exec()
    entry_list = query.get_response()['data']['entries']

    if use_concurrency:
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            dict_list = list(executor.map(process_entry, entry_list, chunksize=chunk_size))
    else:
        dict_list = [process_entry(entry) for entry in entry_list]

    df = (pl.LazyFrame(dict_list).explode(['rcsb_id', 'sequence', 'length', 'strand_id', 'type'])
                  .filter(pl.col('type')=='Protein')
                  .drop('type')
                  .explode('strand_id'))
    
    if use_lazy:
        return df
    else:
        return df.collect()

    
    


