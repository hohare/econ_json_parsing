# TID scripts from July 2025 TID test at CERN
This section is out of date.

Setup of the framework: relies on a JSON Github repository:

https://github.com/mstamenk/tid-july-2024

# Setting up
This section is out of date.

```
git clone git@github.com:dnoonan08/econ_json_parsing.git
git submodule add git@github.com:mstamenk/tid-july-2024.git
```

Setting up the environment

```
source setup.sh # sets MYROOT bash variable as well as PYTHONPATH
```

# Structure

```
- common.py # all script needed for all plotting scripts
- current_tid.py # plot current vs TID - creates repo with plots current_vs_tid
- parse_pll.py # parse jsons TID and pll test info and save into a csv
- parse_phaseScan.py # parse jsons TID and eRX test info and save into a csv
- parse_delayScan.py # parse jsons TID and eTX test info and save into a csv
- parse_capbankSelection.py # parse jsons TID automatic capbank selection and save into a csv
```

# Parsing
Each parsing script can parse multiple cobs, but if you want to parse for multiple tests use `parse_all.py` on a single cob.
