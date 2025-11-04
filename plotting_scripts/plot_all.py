import os

def main(args):
    to_run = [
        'plotting_scripts/plot_PhaseScan.py',
        'plotting_scripts/plot_DelayScan.py',
        'plotting_scripts/plot_PLLAutoLock.py',
        'plotting_scripts/plot_PLLCapbankWidth.py',
        ]
    
    cmd = 'python %s --csv %s --cob %s --outpath %s'
    for s in to_run:
        runcmd = cmd%(s, args.csv, args.cob, args.outpath)
        if "Delay" in runcmd: runcmd = runcmd + ' --econd'
        print(runcmd)
        os.system(runcmd)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--csv', type = str, default="/Users/suzannehare/Desk/econ_testing/TID_sanity_checks/csv_files", help='Path to the csv file') 
    parser.add_argument('--cob', help="Which COB")
    parser.add_argument('--outpath', default="/Users/suzannehare/Desk/econ_testing/plots")
    args = parser.parse_args()

    main(args)