import os

allowed_cap_bank_vals=np.array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,   10,  11,  12,
                                  13,  14,  15,  24,  25,  26,  27,  28,  29,  30,  31,  56,  57,
                                  58,  59,  60,  61,  62,  63,  120, 121, 122, 123, 124, 125, 126,
                                  127, 248, 249, 250, 251, 252, 253, 254, 255, 504, 505, 506, 507,
                                  508, 509, 510, 511])
def get_entry_capbankSelection(metadata, cob):
    timestamp = get_timestamp(metadata['Timestamp'][0])
    tid = julyUtils.getTID(timestamp, cob)
    voltage = metadata['voltage']
    automatic_capbank_setting = allowed_cap_bank_vals.searchsorted(metadata['automatic_capbank_setting'])
    entry = [timestamp, tid, voltage, automatic_capbank_setting] 
    return entry
    
def get_entry_phasescan(metadata, valuename, cob):
    timestamp = get_timestamp(metadata['timestamp'])
    tid = julyUtils.getTID(timestamp, cob)
    voltage = metadata['voltage']
    value = np.array(metadata[valuename]).flatten()
    entry = [timestamp, tid, voltage] + list(value)
    columns = ["eRX_errcounts_{select:n}_{val:n}".format(select=i, val=j) for i in range(15) for j in range(12)]
    return entry, columns

def get_entry_delayscan(metadata, cob):
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
    parser.add_argument('--jsons', type=str, 
                        default = "/eos/user/d/dnoonan/July_2025_TID_Data/merged_jsons",
                        help='Path to test jsons') 
    parser.add_argument('--output', type = str,
                        default = '/eos/user/h/hohare/ECONs/summary_csv_TID_July2025',
                        help='Path to output csvs') 
    parser.add_argument('--cobs', nargs="+", help="Which COB")


    if args.econd: delay_shape = (6, 63)
    elif args.econt: delay_shape = (13, 63)
        
    # For each wanted cob
    for cob in args.cobs:
        print(f'Parsing cob {cob}')
        json_list = glob.glob(f"{args.jsons}/report_TID_chip_{args.cob}*.json")

        columns = ['timestamp','tid','voltage']
        selection = []
        phasescan = []
        delay_columns = ["eTX_errRate_{select:n}_{val:n}".format(select=i, val=j) for i in range(delay_shape[0]) for j in range(delay_shape[1])]
    
        for fnum in track(range(len(json_list))):
            with open(json_list[fnum], 'r') as f:
                data = json.load(f)
            
            for t in range(len(data['tests'])):
                if data['tests'][t]['outcome']=='skipped': continue
                elif 'metadata' in data['tests'][t]:
                    # AUTOMATIC CAPBANK SELECTION
                    if f"test_streamCompareLoop" in data['tests'][t]['nodeid']:
                        entry = get_entry_capbankSelection(data['tests'][t]['metadata'], cob)
                        selection.append(entry)
                    # PHASE SCAN
                    if f"test_ePortRXPRBS" in data['tests'][t]['nodeid']:
                        entry, newcolumns = get_entry_phasescan(data['tests'][t]['metadata'], 'eRX_errcounts', args.cob)
                        phasescan.append(entry)
        df = pd.DataFrame(phasescan, columns=columns+newcolumns)
        df.to_csv(f'{args.output}/report_summary_{args.cob}_phasescan.csv', index=False)  