import os

def main(args):
    to_run = [
        #'TID_scripts/parse_capbankSelection.py',
        #'TID_scripts/parse_phaseScan.py',
        #'TID_scripts/parse_delayScan.py',
        'TID_scripts/parse_pll.py',
        ]
    
    cmd = 'python %s --jsons %s --cobs %s --output %s'
    for s in to_run:
        cobs = "_".join(args.cob)
        runcmd = cmd%(s, args.jsons, cobs, args.output)
        if "delay" in runcmd: runcmd = runcmd + ' --econd'
        print(runcmd)
        os.system(runcmd)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--jsons', type=str, 
                        default = "/eos/user/d/dnoonan/July_2025_TID_Data/merged_jsons",
                        help='Path to test jsons') 
    parser.add_argument('--output', type = str,
                        default = '/eos/user/h/hohare/ECONs/summary_csv_TID_July2025',
                        help='Path to output csvs') 
    parser.add_argument('--cob', nargs="+", help="Which COB")
    args = parser.parse_args()
    
    main(args)