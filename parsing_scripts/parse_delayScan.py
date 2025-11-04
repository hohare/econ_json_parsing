import sys
import glob
import json
import numpy as np
import pandas as pd
from rich.progress import track

from utilities import get_timestamp
import July_2025_TID_utils as julyUtils

def get_entry(metadata, cob):
    timestamp = get_timestamp(metadata['timestamp'])
    tid = julyUtils.getTID(timestamp, cob)
    voltage = metadata['voltage']
    errcounts = np.array(metadata['eTX_errcounts']).flatten()
    bitcounts = np.array(metadata['eTX_bitcounts']).flatten()
    errRate = errcounts/bitcounts
    entry = [timestamp, tid, voltage] + list(errRate)
    return entry

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--jsons', type = str, help='Path to test jsons') 
    parser.add_argument('--output', type = str, help='Path to output csvs') 
    parser.add_argument('--cob', default = "COB-10Pct-1-3")
    parser.add_argument('--econd', action='store_true')
    parser.add_argument('--econt', action='store_true')
    args = parser.parse_args()

    json_list = glob.glob(f"{args.jsons}/report_TID_chip_{args.cob}*.json")

    if args.econd: shape = (6, 63)
    elif args.econt: shape = (13, 63)

    scan = []
    columns = ['timestamp','tid','voltage']
    newcolumns = ["eTX_errRate_{select:n}_{val:n}".format(select=i, val=j) for i in range(shape[0]) for j in range(shape[1])]

    for fnum in track(range(len(json_list))):
        with open(json_list[fnum], 'r') as f:
            data = json.load(f)
        
        for t in range(len(data['tests'])):
            if data['tests'][t]['outcome']=='skipped': continue
            if 'metadata' in data['tests'][t]:
                if f"test_eTX_delayscan" in data['tests'][t]['nodeid']:
                    entry = get_entry(data['tests'][t]['metadata'], args.cob)
                    scan.append(entry)
    df = pd.DataFrame(scan, columns=columns+newcolumns)
    df.to_csv(f'{args.output}/report_summary_{args.cob}_delayscan.csv', index=False)