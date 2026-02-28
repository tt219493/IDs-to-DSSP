# IDs To DSSP 
## Secondary Structure and Protein Sequence Retriever

### 
Simple Python package to provide labeled secondary structure and protein sequence data when given a file containing IDs from the Protein Data Bank (PDB).

___
To retrieve secondary structure from the file (TSV or Parquet) containing IDs, it gets unique IDs from the file and uses those IDs to make GET calls to 
[`https://pdb-redo.eu/dssp/db/{pdb_id}/mmcif`](https://pdb-redo.eu/dssp/)  
(implementation by Hekkelman et al. in the Perrakis group @ NKI Research)

With the data returned from the calls, it retrieves relevant secondary sequence and asym ID/strand ID information.

To retrieve protein sequence data from the IDs, it queries using the `rcsb-api` for Python to retrieve relevant sequence data and asym/strand ID.

The sequencing and secondary structure data can be combined and outputted as a `Polars` LazyFrame or DataFrame which can then be written to a file.
___
Thanks to Hekkelman ML et al. (2025) for `mkdssp`, cheng_shizhuo for `rs_dssp` and Piehl et al. (2025) and Rose et al. (2020) for the RCSB API. 

Getting Started
---
(Currently only tested in Google Colab so this package may not work locally)
```
git clone https://github.com/tt219493/ids-to-dssp.git
cd ids-to-dssp
pip install .
```
and in Python
```Python
import ids-to-dssp

import ids_to_dssp.processing
import ids_to_dssp.pdb
import ids_to_dssp.mkdssp_api
import ids_to_dssp.pipeline
```
(Might need to add directory to PATH if not working)
___
### Colab Specific Requirements
After using `pip` to install
```Python
import sys
sys.path.append('/content/ids-to-dssp/src')
```
___

Recent Changes and Improvements
---
* Implemented `mkdssp_api` over `rs_dssp` and [`mkdssp`](https://github.com/PDB-REDO/dssp)
    * Utilizes GET calls to retrieve information from 
    [mkdssp website](https://pdb-redo.eu/dssp/)
    * Relies on internet speeds but personally takes ~27 min for 6000+ files
    * No need for installation or local downloads
    * Utilized in `pipeline`

* `rs_dssp` has fastest processing (~3 min for 6000+ files)
    * Requires pip install
    * Requires download of all necessary mmCif files
    * Stated to have 97% accuracy
    * Returns`seq_id` data from the author, 
    which need to be correctly aligned with `seq_id` from PDB
        * Requires `Bio` to parse all files to get proper alignments (~22 min)

* `mkdssp` might be best if already installed (installation documentation in branch)
    * Requires download of all necessary mmCif files
    * ~15 min for processing 6000+ files

   

Limitations
---
* Currently only tested in Colab
* Unfortunately, all methods are somewhat slow
    * `mkdssp_api` requires the least preparation and doesn't require download to local storage, so I believe this is the current best

    * Fastest and most accurate would probably be having local access to DSSP files, but this package is supposed to provide a workaround


Future Expansions
--- 
* Potentially find another way to get DSSP files but I believe these are currently the best options
* Support for more file inputs/outputs
* Upload to PyPI after polishing

References
--- 
>Hekkelman ML, Salmoral DÁ, Perrakis A, Joosten RP DSSP 4: FAIR annotation of protein secondary structure. Protein Science. 2025; 34(8):e70208. 

>Kabsch W, Sander C. Dictionary of protein secondary structure: pattern recognition of hydrogen-bonded and geometrical features. Biopolymers 1983; 22:2577-2637. 

>Dennis W. Piehl, Brinda Vallat, Ivana Truong, Habiba Morsy, Rusham Bhatt, Santiago Blaumann, Pratyoy Biswas, Yana Rose, Sebastian Bittrich, Jose M. Duarte, Joan Segura, Chunxiao Bi, Douglas Myers-Turnbull, Brian P. Hudson, Christine Zardecki, Stephen K. Burley. rcsb-api: Python Toolkit for Streamlining Access to RCSB Protein Data Bank APIs, Journal of Molecular Biology, 2025. DOI: 10.1016/j.jmb.2025.168970

>Yana Rose, Jose M. Duarte, Robert Lowe, Joan Segura, Chunxiao Bi, Charmi Bhikadiya, Li Chen, Alexander S. Rose, Sebastian Bittrich, Stephen K. Burley, John D. Westbrook. RCSB Protein Data Bank: Architectural Advances Towards Integrated Searching and Efficient Access to Macromolecular Structure Data from the PDB Archive, Journal of Molecular Biology, 2020. DOI: 10.1016/j.jmb.2020.11.003
