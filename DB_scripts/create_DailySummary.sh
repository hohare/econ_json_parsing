#!/bin/bash

. /fasic_home/dnoonan/.slack_token

cd /fasic_home/dnoonan/WD_ECON_Testing/dnoonan/econ_json_parsing/DB_scripts/

python /fasic_home/dnoonan/WD_ECON_Testing/dnoonan/econ_json_parsing/DB_scripts/makeCSVECOND.py
python /fasic_home/dnoonan/WD_ECON_Testing/dnoonan/econ_json_parsing/DB_scripts/makeCSVECONT.py
python /fasic_home/dnoonan/WD_ECON_Testing/dnoonan/econ_json_parsing/DB_scripts/DailySummary.py
