import sys
import glob
import json
import numpy as np
import pandas as pd
from rich.progress import track

from common import get_timestamp
sys.path.append('..')
import July_2025_TID_utils as julyUtils

allowed_cap_bank_vals=np.array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,   10,  11,  12,
                                  13,  14,  15,  24,  25,  26,  27,  28,  29,  30,  31,  56,  57,
                                  58,  59,  60,  61,  62,  63,  120, 121, 122, 123, 124, 125, 126,
                                  127, 248, 249, 250, 251, 252, 253, 254, 255, 504, 505, 506, 507,
                                  508, 509, 510, 511])

def get_entry(metadata, cob):
    timestamp = get_timestamp(metadata['Timestamp'][0])
    tid = julyUtils.getTID(timestamp, cob)
    voltage = metadata['voltage']
    automatic_capbank_setting = allowed_cap_bank_vals.searchsorted(metadata['automatic_capbank_setting'])
    entry = [timestamp, tid, voltage, automatic_capbank_setting] 
    return entry

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--jsons', type = str, default="/eos/user/d/dnoonan/July_2025_TID_Data/merged_jsons", help='Path to test jsons') 
    parser.add_argument('--output', type = str, default='/eos/user/h/hohare/ECONs/summary_csv_TID_July2025', help='Path to output csvs') 
    parser.add_argument('--cobs', nargs="+", default = ["COB-10Pct-1-3"])
    parser.add_argument('--econd', action='store_true')
    parser.add_argument('--econt', action='store_true')
    args = parser.parse_args()

    # Do for each input cobs
    for cob in args.cobs:
        print(f'Parsing cob {cob}')
        json_list = glob.glob(f"{args.jsons}/report_TID_chip_{cob}*.json")
        # extract info per json
        scan = []
        columns = ['timestamp','tid','voltage', 'automatic_capbank_setting']
        # Loop over all the test jsons for this cob
        for fnum in track(range(len(json_list))):
            with open(json_list[fnum], 'r') as f:
                data = json.load(f)
            
            for t in range(len(data['tests'])):
                if data['tests'][t]['outcome']=='skipped': continue
                if 'metadata' in data['tests'][t]:
                    if f"test_streamCompareLoop" in data['tests'][t]['nodeid']:
                        entry = get_entry(data['tests'][t]['metadata'], cob)
                        scan.append(entry)
        if len(scan)>0:
            df = pd.DataFrame(scan, columns=columns)
            df.to_csv(f'{args.output}/report_summary_{cob}_autoCapbankSelection.csv', index=False)
        else:
            print(f'No streamCompareLoop results available for {cob}')