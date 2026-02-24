 IDs To DSSP
===
### Secondary Structure and Protein Sequence Retriever
Simple Python package to provide labeled secondary structure and protein sequence data when given a file containing IDs from the Protein Data Bank (PDB).

___
To retrieve secondary structure from the file containing IDs, it utilizes `Biopython` to download mmCif/PDB files from wwPDB.  
Then using those files as input, [dssp](https://github.com/PDB-REDO/dssp) (implementation by Hekkelman et al. in the Perrakis group @ NKI Research) outputs secondary structures.

To retrieve protein sequence data from the IDs, it queries using the `rcsb-api` for Python to retrieve relevant sequence data.

The sequencing and secondary structure data can be combined and outputted as a `Polars` LazyFrame or DataFrame which can then be written to a file.
___
Thanks to Hekkelman ML et al. (2025) for dssp implementation and Piehl et al. (2025) and Rose et al. (2020) for the RCSB API. 

Getting Started
---
(Currently only tested in Google Colab so this package may not work locally)
```
git clone https://github.com/tt219493/ids-to-dssp.git
cd ids-to-dssp
```
### Installing [dssp](https://github.com/PDB-REDO/dssp)
```
git clone https://github.com/PDB-REDO/dssp.git
cd dssp
cmake -S . -B build -DBUILD_PYTHON_MODULE=ON
cmake --build build
cmake --install build
```
After installation of dssp, we can do
```
cd ..
pip install .
```
and in Python
```Python
import sys
sys.path.append('/content/ids-to-dssp/src')

import ids-to-dssp
```

### Colab Specific Requirements
```Python
!pip install Bio
!pip install --upgrade numpy==1.26.4

# For cmake to find numpy directory
!export CFLAGS=/usr/local/lib/python3.12/dist-packages/numpy/core/include

# <format> and std::format do not work with compiler on Colab
# Use <fmt/format.h> and fmt::format instead
!sudo add-apt-repository universe
!sudo apt update
!sudo apt install libfmt-dev
```

**During dssp installation:**  
After cloning and changing directory
```Python
# Manually add #define FMT_HEADER_ONLY to top of file dssp/libdssp/src/dssp-io.cpp
!grep -rl '#include <format>' libdssp/src/dssp-io.cpp | xargs sed -i 's/#include <format>/#include <fmt\/format.h>/g'
!grep -rl 'std::format' libdssp/src/dssp-io.cpp | xargs sed -i 's/std::format/fmt::format/g'
```

After running `cmake -S . -B build-DBUILD_PYTHON_MODULE=ON`
```Python
!grep -rl '#include <format>' build/_deps/ | xargs sed -i 's/#include <format>/#include <fmt\/format.h>/g'
!grep -rl 'std::format' build/_deps/ | xargs sed -i 's/std::format/fmt::format/g'
```

Limitations
---
* Currently only tested in Colab
* Requires download of mmCif/PDB files
    * For reference: 6000 mmCif files ~ 3 GB
* Requires installation of `dssp`
* `dssp` implementation is fairly slow for a large number of files
    * ~0.15 seconds per file
    * [DSSP API](https://pdb-redo.eu/dssp/api-doc) unfortunately does not support batched calls

Future Expansions
--- 
* Implementing support for [DSSP API](https://pdb-redo.eu/dssp/api-doc) for a small number of files
* Utilizing different implementation of DSSP (e.g. [rs-dssp](pypi.org/project/rs-dssp/)) for faster processing (although accuracy might be lower)
* Upload to PyPI after polishing

Citations
--- 
```
Hekkelman ML, Salmoral DÁ, Perrakis A, Joosten RP DSSP 4: FAIR annotation of protein secondary structure. Protein Science. 2025; 34(8):e70208. 

Kabsch W, Sander C. Dictionary of protein secondary structure: pattern recognition of hydrogen-bonded and geometrical features. Biopolymers 1983; 22:2577-2637. 

Dennis W. Piehl, Brinda Vallat, Ivana Truong, Habiba Morsy, Rusham Bhatt, Santiago Blaumann, Pratyoy Biswas, Yana Rose, Sebastian Bittrich, Jose M. Duarte, Joan Segura, Chunxiao Bi, Douglas Myers-Turnbull, Brian P. Hudson, Christine Zardecki, Stephen K. Burley. rcsb-api: Python Toolkit for Streamlining Access to RCSB Protein Data Bank APIs, Journal of Molecular Biology, 2025. DOI: 10.1016/j.jmb.2025.168970

Yana Rose, Jose M. Duarte, Robert Lowe, Joan Segura, Chunxiao Bi, Charmi Bhikadiya, Li Chen, Alexander S. Rose, Sebastian Bittrich, Stephen K. Burley, John D. Westbrook. RCSB Protein Data Bank: Architectural Advances Towards Integrated Searching and Efficient Access to Macromolecular Structure Data from the PDB Archive, Journal of Molecular Biology, 2020. DOI: 10.1016/j.jmb.2020.11.003
```
