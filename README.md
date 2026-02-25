 IDs To DSSP
===
### Secondary Structure and Protein Sequence Retriever
Simple Python package to provide labeled secondary structure and protein sequence data when given a file containing IDs from the Protein Data Bank (PDB).

___
To retrieve secondary structure from the file (TSV or Parquet) containing IDs, it utilizes `Biopython` to download mmCif/PDB files from wwPDB.  
Then using those files as input, [`rs_dssp`](https://pypi.org/project/rs-dssp/) (implementation by cheng_shizhuo) outputs secondary structures. 

To retrieve protein sequence data from the IDs, it queries using the `rcsb-api` for Python to retrieve relevant sequence data.

The sequencing and secondary structure data can be combined and outputted as a `Polars` LazyFrame or DataFrame which can then be written to a file.
___
Thanks to cheng_shizhuo for `rs_dssp` and Piehl et al. (2025) and Rose et al. (2020) for the RCSB API. 

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

Recent Improvements
---
* Implemented `rs_dssp` instead of [`mkdssp`](https://github.com/PDB-REDO/dssp) (mkdssp version still available in branch)
    * Can be installed using `pip install`
    * Installation time takes ~2 min instead of ~15 min
    * Running dssp on 6000 files takes ~3 min instead of ~12 min.

Limitations
---
* Currently only tested in Colab
* Requires download of mmCif/PDB files
    * For reference: 6000 mmCif files ~ 3 GB
* Requires installation of `rs-dssp`
 *  `ids-to-dssp.pipeline` is untested 
    * The individual modules that make up `pipeline` are working.

Future Expansions
--- 
* Add Jupyter notebooks with example use.
* Implementing support for [DSSP API](https://pdb-redo.eu/dssp/api-doc) for a small number of files
* Support for more file inputs/outputs
* Upload to PyPI after polishing

Citations
--- 
>Kabsch W, Sander C. Dictionary of protein secondary structure: pattern recognition of hydrogen-bonded and geometrical features. Biopolymers 1983; 22:2577-2637. 

>Dennis W. Piehl, Brinda Vallat, Ivana Truong, Habiba Morsy, Rusham Bhatt, Santiago Blaumann, Pratyoy Biswas, Yana Rose, Sebastian Bittrich, Jose M. Duarte, Joan Segura, Chunxiao Bi, Douglas Myers-Turnbull, Brian P. Hudson, Christine Zardecki, Stephen K. Burley. rcsb-api: Python Toolkit for Streamlining Access to RCSB Protein Data Bank APIs, Journal of Molecular Biology, 2025. DOI: 10.1016/j.jmb.2025.168970

>Yana Rose, Jose M. Duarte, Robert Lowe, Joan Segura, Chunxiao Bi, Charmi Bhikadiya, Li Chen, Alexander S. Rose, Sebastian Bittrich, Stephen K. Burley, John D. Westbrook. RCSB Protein Data Bank: Architectural Advances Towards Integrated Searching and Efficient Access to Macromolecular Structure Data from the PDB Archive, Journal of Molecular Biology, 2020. DOI: 10.1016/j.jmb.2020.11.003
