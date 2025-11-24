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
    value = metadata[valuename]
    if isinstance(value, list):
        entry = [timestamp, tid, voltage] + value
    else:
        entry = [timestamp, tid, voltage, value]
    return entry

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--jsons', type = str,  default="/eos/user/d/dnoonan/July_2025_TID_Data/merged_jsons", help='Path to test jsons') 
    parser.add_argument('--output', type = str, default='/eos/user/h/hohare/ECONs/summary_csv_TID_July2025',help='Path to output csvs') 
    parser.add_argument('--cobs', nargs="+", default = "COB-10Pct-1-3")
    args = parser.parse_args()

    for cob in args.cobs:
        json_list = glob.glob(f"{args.jsons}/report_TID_chip_{cob}*.json")
        # extract info per json
        PLLCapbankWidth = []
        PLLCapbankWidth_columns = ['timestamp','tid','voltage','pll_capbank_width']
        PLLAutoLock = []
        PLLAutoLock_columns = ['timestamp','tid','voltage','auto_locks']
    
        for fnum in track(range(len(json_list))):
            with open(json_list[fnum], 'r') as f:
                data = json.load(f)
            
            for t in range(len(data['tests'])):
                if data['tests'][t]['outcome']=='skipped': continue
                if 'metadata' in data['tests'][t]:
                    if f"test_pll_capbank_width" in data['tests'][t]['nodeid']:
                        PLLCapbankWidth.append(get_entry(data['tests'][t]['metadata'], 'pll_capbank_width', cob))
                    if f"test_pllautolock" in data['tests'][t]['nodeid']:
                        PLLAutoLock.append(get_entry(data['tests'][t]['metadata'], 'auto_locks' , cob))
                        columns = ["auto_lock_{val:n}".format(val=i) for i in range(len(data['tests'][t]['metadata']['auto_locks']))]

        
        if len(PLLCapbankWidth)>0:
            df_PllCapbankWidth = pd.DataFrame(PLLCapbankWidth, columns=PLLCapbankWidth_columns)
            df_PllCapbankWidth.to_csv(f'{args.output}/report_summary_{cob}_pllCapbankWidth.csv', index=False)
        else:
            print(f'No PLL Capbank Width data exists for {cob}')
    
        if len(PLLAutoLock)>0:
            PLLAutoLock_columns =  ['timestamp','tid','voltage'] + columns
            df_PLLAutoLock = pd.DataFrame(PLLAutoLock, columns=PLLAutoLock_columns)
            df_PLLAutoLock.to_csv(f'{args.output}/report_summary_{cob}_pllAutolock.csv', index=False)
        else:
            print(f'No PLL Autolock data exists for {cob}')
