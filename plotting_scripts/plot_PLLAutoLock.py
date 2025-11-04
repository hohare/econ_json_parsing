import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap

def plot(df, cob, voltage, outpath):
    print(f'Plotting {voltage}V')
    fig, ax = plt.subplots(figsize=(6,5))

    df.sort_values('timestamp', inplace=True)
    Vmask = (df.voltage==voltage)
    locks = [c for c in df.columns if c.startswith('auto_lock')]
    mradDose = df.tid[Vmask]
    freqs = np.arange(35, 50+(1/8), (1/8))
    x, y = np.meshgrid(mradDose, freqs)
    z = df[locks][Vmask].to_numpy().T

    binary_cmap = ListedColormap(['white','#08306b'])
    h = plt.hist2d(x.flatten(), y.flatten(), weights=z.flatten(), bins=(x[0,:], y[:,0]),cmap=binary_cmap, vmin=0, vmax=1)
    ax.set_ylabel("Frequency (MHz)")
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.set_xlabel("TID (MRad)")
    handles, labels = plt.gca().get_legend_handles_labels()
    patch = mpatches.Patch(color='#08306b', label='PLL Locked')
    handles.append(patch)

    ax.set_title(f'{cob} @ {voltage}V', fontsize=20);
    ax.legend(handles=handles, loc='upper right', fontsize=16)

    voltage = str(voltage).replace('.','p')
    plt.savefig(f'{outpath}/lockingFreq_{voltage}V.png', dpi=300, facecolor="w")
    plt.clf()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--cob', default = 'COB-10Pct-1-3')
    parser.add_argument('--voltages', nargs="+", default = None)
    parser.add_argument('--csv', type = str, default="/Users/suzannehare/Desk/econ_testing/TID_sanity_checks/csv_files", help='Path to the csv file') 
    parser.add_argument('--outpath', default="/Users/suzannehare/Desk/econ_testing/plots")
    args = parser.parse_args()

    args.outpath = f'{args.outpath}/{args.cob}/pll_frequency'
    os.makedirs(args.outpath, exist_ok=True)
    df = pd.read_csv(f'{args.csv}/report_summary_{args.cob}_pllAutolock.csv')

    if not args.voltages:
        voltages = df.voltage.unique()
    for v in voltages:
        plot(df, args.cob, v, args.outpath)



