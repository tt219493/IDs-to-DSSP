import asyncio
from typing import List, Dict, Any
from io import StringIO

import httpx
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import polars as pl

BASE_URL = "https://pdb-redo.eu/dssp/db/{pdb_id}/mmcif"


async def fetch_dssp(client: httpx.AsyncClient, pdb_id: str, 
                     semaphore: asyncio.Semaphore, retries: int = 3,
) -> Dict[str, Any]:
    """
    Given a single PDB ID, use httpx GET to fetch DSSP data from "https://pdb-redo.eu/dssp/db/{pdb_id}/mmcif".
    Allows for retries and concurrency control.

    Parameters
    ---
    client : httpx.AsyncClient
        Client from httpx used for concurrent requests
    pdb_id: str
        PDB ID to retrieve DSSP data for
    semaphore: asyncio.Semaphore
        Semaphore from asyncio to limit concurrency calls
    retries : int=3
        Number of retries to do if GET fails

    Returns
    ---
    Dict[str, Any]
        Dictionary containing DSSP information for one ID 

    """
    url = BASE_URL.format(pdb_id=pdb_id.lower())

    async with semaphore:
        for attempt in range(retries):
            try:
                response = await client.get(url)
                response.raise_for_status()

                with StringIO(response.text) as dssp_file:
                    mmcif_dict = MMCIF2Dict(dssp_file)

                return {
                    "id": pdb_id,
                    "asym_id": mmcif_dict.get(
                        "_dssp_struct_summary.label_asym_id", []
                    ),
                    "amino_acid": mmcif_dict.get(
                        "_dssp_struct_summary.label_comp_id", []
                    ),
                    "index": mmcif_dict.get(
                        "_dssp_struct_summary.label_seq_id", []
                    ),
                    "secondary_structure": mmcif_dict.get(
                        "_dssp_struct_summary.secondary_structure", []
                    ),
                    "pdb_asym_id": mmcif_dict.get(
                        "_pdbx_poly_seq_scheme.asym_id", []
                    ),
                    "pdb_amino_acid": mmcif_dict.get(
                        "_pdbx_poly_seq_scheme.mon_id", []
                    ),
                    "pdb_index": mmcif_dict.get(
                        "_pdbx_poly_seq_scheme.seq_id", []
                    ),
                    "pdb_strand_id": mmcif_dict.get(
                        "_pdbx_poly_seq_scheme.pdb_strand_id", []
                    ),
                }

            except Exception as e:
                if attempt == retries - 1:
                    return {"id": pdb_id, "error": str(e)}

                await asyncio.sleep(2 ** attempt)  # exponential backoff


async def fetch_dssp_bulk(pdb_ids: List[str], max_concurrency: int = 50, retries: int = 3
) -> List[Dict[str, Any]]:
    """
    Given a list of PDB IDs, fetches DSSP information in bulk from "https://pdb-redo.eu/dssp/db/{pdb_id}/mmcif".
    Allows for retries and concurrency control.
   
    Parameters
    ---
    pdb_ids: List[str]
        List of PDB IDs to retrieve DSSP data for
    max_concurrency: int = 50
        Max umber of calls to make concurrently
    retries : int=3
        Number of retries to do if GET fails

    Returns
    ---
    List[Dict[str, Any]]
        List of dictionary containing DSSP information for all IDs in the list 

    """
    semaphore = asyncio.Semaphore(max_concurrency)

    limits = httpx.Limits(
        max_connections=max_concurrency,
        max_keepalive_connections=max_concurrency,
    )

    timeout = httpx.Timeout(20.0)

    async with httpx.AsyncClient(
        limits=limits,
        timeout=timeout,
        http2=True,  
    ) as client:

        tasks = [
            fetch_dssp(client, pdb_id, semaphore, retries)
            for pdb_id in pdb_ids
        ]

        results = []

        # Stream results as they complete (lower memory pressure)
        for task in asyncio.as_completed(tasks):
            result = await task
            results.append(result)

        return results

async def ids_to_dssp(id_list: List[str], max_concurrency: int = 50, 
                      retries: int = 3, use_lazy: bool = True
) -> pl.LazyFrame | pl.DataFrame:
    """
    Async function. 
    
    Given a list of PDB IDs, fetches DSSP info from "https://pdb-redo.eu/dssp/db/{pdb_id}/mmcif".
    Returns information in Polars Lazy or DataFrame.

    Contains information about all residues' secondary structures, including chain breaks, and every strand ID
   
    Parameters
    ---
    pdb_ids: List[str]
        List of PDB IDs to retrieve DSSP data for
    max_concurrency: int = 50
        Max umber of calls to make concurrently
    retries : int = 3
        Number of retries to do if GET fails
    use_lazy: bool = True
        Returns LazyFrame if set to True and DataFrame if set to False
    Returns
    ---
    pl.LazyFrame | pl.DataFrame
        Returns Frame with each row containing `id`, `amino_acid`, `index`, `asym_id`, `strand_id`, `secondary_structure`.

        Shows all residues for every strand, including chain breaks. 

    """

    dict_list = await fetch_dssp_bulk(id_list)    
    df = (pl.LazyFrame(dict_list))
    idx_df = (df.select(['id', 'pdb_asym_id', 'pdb_amino_acid', 'pdb_index', 'pdb_strand_id'])
               .explode(['pdb_asym_id', 'pdb_amino_acid', 'pdb_index', 'pdb_strand_id'])
               .rename({'pdb_asym_id': 'asym_id',
                        'pdb_amino_acid' : 'amino_acid',
                        'pdb_index' : 'index',
                        'pdb_strand_id': 'strand_id'})
               )

    df = df.select(['id', 'asym_id', 'amino_acid', 'index', 'secondary_structure']
                   ).explode(['asym_id', 'amino_acid', 'index', 'secondary_structure'])
    
    df = idx_df.join(df, on=['id', 'asym_id', 'amino_acid', 'index'], how='left')
    df = df.with_columns(pl.col('secondary_structure').fill_null(' '))

    if not use_lazy:
        return df.collect()
    else:
        return df


