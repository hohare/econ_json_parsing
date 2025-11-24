import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
sys.path.append('..')
import July_2025_TID_utils as julyUtils

fontsize=16

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

def plot_cobs(cobs, voltage, csv_files, outpath, vsTID):
    ncobs = len(cobs)
    nrows = 1
    #if ncobs>3: nrows=2
    fig, axes = plt.subplots(nrows, ncobs, figsize=(ncobs*5,nrows*5))
    if ncobs==1: axes = [axes]
    
    freqs = np.arange(35, 50+(1/8), (1/8))
    binary_cmap = ListedColormap(['white','#08306b'])
    for i, cob in enumerate(cobs):
        csv_name = f'{csv_files}/report_summary_{cob}_pllAutolock.csv'
        df = pd.read_csv(csv_name)
        print(pd.unique(df.voltage))
        
        df.sort_values('timestamp', inplace=True)
        Vmask = (df.voltage==voltage)
        locks = [c for c in df.columns if c.startswith('auto_lock')]
        mradDose = df.tid[Vmask]
        
        x, y = np.meshgrid(mradDose, freqs)
        z = df[locks][Vmask].to_numpy().T

        h = axes[i].hist2d(x.flatten(), y.flatten(), weights=z.flatten(), bins=(x[0,:], y[:,0]),
                           cmap=binary_cmap, vmin=0, vmax=1)

        axes[i].set_title(f'{cob} @ {voltage}V', fontsize=18);
        axes[i].set_ylabel("Frequency (MHz)", fontsize=fontsize)
        axes[i].yaxis.get_major_locator().set_params(integer=True)
        axes[i].set_xlabel("TID (MRad)", fontsize=fontsize)
        
        handles, labels = plt.gca().get_legend_handles_labels()
        patch = mpatches.Patch(color='#08306b', label='PLL Locked')
        handles.append(patch)
        axes[i].legend(handles=handles, loc='upper right', fontsize=fontsize)
        #tax = julyUtils.mark_TID_times(axes[i], cob, vsTID=vsTID)

def plot_voltages(cob, voltages, csv_files, outpath, vsTID):
    ncols = len(voltages)
    fig, axes = plt.subplots(1, ncols, figsize=(ncols*5,5), sharey=True)
    if ncols==1: axes = [axes]

    csv_name = f'{csv_files}/report_summary_{cob}_pllAutolock.csv'
    df = pd.read_csv(csv_name)
    print(pd.unique(df.voltage))
    
    freqs = np.arange(35, 50+(1/8), (1/8))
    binary_cmap = ListedColormap(['white','#08306b'])
    for i, volts in enumerate(voltages):
        
        df.sort_values('timestamp', inplace=True)
        Vmask = (df.voltage==volts)
        locks = [c for c in df.columns if c.startswith('auto_lock')]
        mradDose = df.tid[Vmask]
        
        x, y = np.meshgrid(mradDose, freqs)
        z = df[locks][Vmask].to_numpy().T

        h = axes[i].hist2d(x.flatten(), y.flatten(), weights=z.flatten(), bins=(x[0,:], y[:,0]),cmap=binary_cmap, vmin=0, vmax=1)

        axes[i].set_title(f'{cob} @ {volts}V', fontsize=18);
        axes[i].yaxis.get_major_locator().set_params(integer=True)
        axes[i].set_xlabel("TID (MRad)", fontsize=fontsize)
        handles, labels = plt.gca().get_legend_handles_labels()
        patch = mpatches.Patch(color='#08306b', label='PLL Locked')
        handles.append(patch)
    
        axes[i].legend(handles=handles, loc='upper right', fontsize=fontsize)

    axes[0].set_ylabel("Frequency (MHz)", fontsize=fontsize)


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



