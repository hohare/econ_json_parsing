import os

def main(args):
    to_run = [
        'parsing_scripts/parse_phaseScan.py',
        'parsing_scripts/parse_delayScan.py',
        'parsing_scripts/parse_pll.py'
        ]
    
    cmd = 'python %s --jsons %s --cob %s --output %s'
    for s in to_run:
        runcmd = cmd%(s, args.jsons, args.cob, args.output)
        if "delay" in runcmd: runcmd = runcmd + ' --econd'
        print(runcmd)
        os.system(runcmd)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--jsons', type=str, 
                        default = "/Users/suzannehare/Desk/econ_testing/TID_sanity_checks/json_files",
                        help='Path to test jsons') 
    parser.add_argument('--output', type = str,
                        default = '/Users/suzannehare/Desk/econ_testing/TID_sanity_checks/csv_files',
                        help='Path to output csvs') 
    parser.add_argument('--cob', help="Which COB")
    args = parser.parse_args()

    main(args)