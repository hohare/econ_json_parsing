import sys
import glob
import json
import numpy as np
import pandas as pd
from rich.progress import track

from utilities import get_timestamp
from July_2025_TID_utils import getTID

def get_entry(metadata, valuename, cob):
    timestamp = get_timestamp(metadata['timestamp'])
    tid = getTID(timestamp, cob)
    voltage = metadata['voltage']
    value = metadata[valuename]
    if isinstance(value, list):
        entry = [timestamp, tid, voltage] + value
    else:
        entry = [timestamp, tid, voltage, value]
    return entry

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--jsons', type = str, help='Path to test jsons') 
    parser.add_argument('--output', type = str, help='Path to output csvs') 
    parser.add_argument('--cob', default = "COB-10Pct-1-3")
    args = parser.parse_args()

    json_list = glob.glob(f"{args.jsons}/report_TID_chip_{args.cob}*.json")
    # extract info per json
    PllCapbankWidth = []
    PllCapbankWidth_columns = ['timestamp','tid','voltage','pll_capbank_width']
    PLLAutoLock = []
    PLLAutoLock_columns = ['timestamp','tid','voltage','auto_locks']

    for fnum in track(range(len(json_list))):
        with open(json_list[fnum], 'r') as f:
            data = json.load(f)
        
        for t in range(len(data['tests'])):
            if data['tests'][t]['outcome']=='skipped': continue
            if 'metadata' in data['tests'][t]:
                if f"test_pll_capbank_width" in data['tests'][t]['nodeid']:
                    PllCapbankWidth.append(get_entry(data['tests'][t]['metadata'], 'pll_capbank_width', args.cob))
                if f"test_pllautolock" in data['tests'][t]['nodeid']:
                    PLLAutoLock.append(get_entry(data['tests'][t]['metadata'], 'auto_locks' , args.cob))
                    columns = ["auto_lock_{val:n}".format(val=i) for i in range(len(data['tests'][t]['metadata']['auto_locks']))]

    df_PllCapbankWidth = pd.DataFrame(PllCapbankWidth, columns=PllCapbankWidth_columns)
    df_PllCapbankWidth.to_csv(f'{args.output}/report_summary_{args.cob}_pllCapbankWidth.csv', index=False)  

    PLLAutoLock_columns =  ['timestamp','tid','voltage'] + columns
    df_PLLAutoLock = pd.DataFrame(PLLAutoLock, columns=PLLAutoLock_columns)
    df_PLLAutoLock.to_csv(f'{args.output}/report_summary_{args.cob}_pllAutolock.csv', index=False)
