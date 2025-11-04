import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('..')
import July_2025_TID_utils as julyUtils

def plot(df, cob, voltage, outpath):
    print(f'Plotting {voltage}V')
    fig, ax = plt.subplots(figsize=(10,5))

    mask = df.voltage==voltage
    mradDose = df.tid[mask]
    pll_capbank_width = df.pll_capbank_width[mask]
    plt.scatter(mradDose, pll_capbank_width, s=4, )#label=str(v)+"V")
    _xlim = ax.get_xlim()
    plt.xlim(-5., _xlim[1]*1.01)
    julyUtils.mark_TID_times(ax, cob, vsTID=True)
    plt.ylabel('PllCapbankWidth')
    plt.xlabel("TID (MRad)")
    plt.xticks(rotation=90)
    ax.set_title(f'{cob} @ {voltage} V')

    plt.legend(fontsize=12);

    voltage = str(voltage).replace('.','p')
    plt.savefig(f'{outpath}/capbankWidth_{cob}_{voltage}V.png', dpi=300, facecolor="w")
    plt.clf()
    plt.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--cob', default = 'COB-10Pct-1-3')
    parser.add_argument('--voltages', nargs="+", default = None)
    parser.add_argument('--csv', type = str, default="/Users/suzannehare/Desk/econ_testing/TID_sanity_checks/csv_files", help='Path to the csv file') 
    parser.add_argument('--outpath', default="/Users/suzannehare/Desk/econ_testing/plots")
    args = parser.parse_args()

    args.outpath = f'{args.outpath}/{args.cob}/pll_capbank_width'
    os.makedirs(args.outpath, exist_ok=True)
    df = pd.read_csv(f'{args.csv}/report_summary_{args.cob}_pllCapbankWidth.csv')

    if not args.voltages:
        voltages = df.voltage.unique()
    for v in voltages:
        plot(df, args.cob, v, args.outpath)



