`ids_to_dssp.mkdssp_api` 
===
Fetches data from `https://pdb-redo.eu/dssp/db/{pdb_id}/mmcif`  
Doesn't require any local downloads or installations. 

```Python
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
