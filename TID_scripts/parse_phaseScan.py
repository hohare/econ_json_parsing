import sys
import glob
import json
import numpy as np
import pandas as pd
from rich.progress import track

from common import get_timestamp
sys.path.append('..')
import July_2025_TID_utils as julyUtils

def get_entry(metadata, valuename, cob):
    timestamp = get_timestamp(metadata['timestamp'])
    tid = julyUtils.getTID(timestamp, cob)
    voltage = metadata['voltage']
    value = np.array(metadata[valuename]).flatten()
    entry = [timestamp, tid, voltage] + list(value)
    columns = ["eRX_errcounts_{select:n}_{val:n}".format(select=i, val=j) for i in range(15) for j in range(12)]
    return entry, columns

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--jsons', type = str, help='Path to test jsons') 
    parser.add_argument('--output', type = str, help='Path to output csvs') 
    parser.add_argument('--cobs', nargs="+", default = ["COB-10Pct-1-3"], help="Which COB")
    args = parser.parse_args()

    columns = ['timestamp','tid','voltage']
    for cob in args.cobs:
        print(f'Parsing cob {cob}')
        json_list = glob.glob(f"{args.jsons}/report_TID_chip_{cob}*.json")
        phasescan = []
    
        for fnum in track(range(len(json_list))):
            with open(json_list[fnum], 'r') as f:
                data = json.load(f)
            
            for t in range(len(data['tests'])):
                if data['tests'][t]['outcome']=='skipped': continue
                if 'metadata' in data['tests'][t]:
                    if f"test_ePortRXPRBS" in data['tests'][t]['nodeid']:
                        entry, newcolumns = get_entry(data['tests'][t]['metadata'], 'eRX_errcounts', cob)
                        phasescan.append(entry)
        df = pd.DataFrame(phasescan, columns=columns+newcolumns)
        df.to_csv(f'{args.output}/report_summary_{args.cob}_phasescan.csv', index=False) 
