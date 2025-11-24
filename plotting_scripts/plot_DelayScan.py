import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import July_2025_TID_utils as julyUtils

import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
map = mpl.colormaps['Reds']#['turbo']#['autumn_r']#['Reds']
newcolors = map(np.linspace(0,1,256))[50:]
newcolors[0, :] = [1., 1., 1., 1.]
newmap = ListedColormap(newcolors)

fontsize=16

def plot(df, cob, eTXnum, voltage, outpath):
    shape = (6, 63)

    fig, ax = plt.subplots(figsize=(5,5))

    df.sort_values('timestamp', inplace=True)

    Vmask = df.voltage==voltage
    #mradDose = df.tid[Vmask]
    mradDose, idxs = np.unique(df.tid[Vmask].to_numpy(), return_index=True)
    xbins = np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]])
    settings = np.arange(shape[1])

    a, b = np.meshgrid(mradDose, settings)
    z = df[Vmask].drop(['timestamp','tid','voltage'], axis=1).to_numpy()[idxs]
    z = np.reshape(z, (z.shape[0], shape[0], shape[1]))[:,eTXnum,:].T.flatten()

    ybins = np.arange(0, shape[1], 1)
    h = plt.hist2d(a.flatten(), b.flatten(), weights=z, bins=(xbins, ybins), cmap=newmap, vmin=0., vmax=1.0)
    cb=fig.colorbar(h[3])
    cb.set_label(label='Transmission error rate', size=16)
    cb.ax.set_yscale('linear')
    
    plt.xlabel('TID (Mrad)',  fontsize=16)
    plt.ylabel('Delay Select Setting', fontsize=16)
    plt.title(f"{cob} eTx {eTXnum} at {voltage}V", fontsize=12)

    tax = julyUtils.mark_TID_times(ax, cob, vsTID=True)
    handles, labels = plt.gca().get_legend_handles_labels()
    ax.legend(handles=handles, ncol=2,  fontsize=8)

    voltage = str(voltage).replace('.','p')
    xlim = ax.get_xlim()
    if outpath:
        if xlim[1]>0:
            plt.savefig(f'{outpath}/delayScan_{cob}_eTXnum{eTXnum}_{voltage}V.png', dpi=300, facecolor="w",  bbox_inches='tight')
        plt.clf()
        plt.close()

def plot_cobs(cobs, eTXnum, voltage, csv_files, outpath, vsTID=True):
    ncobs = len(cobs)
    nrows = 1
    #if ncobs>3: nrows=2
    fig, axes = plt.subplots(nrows, ncobs, figsize=(ncobs*5,nrows*5), 
                             sharey=True, layout='constrained')
    if ncobs==1: axes = [axes]

    shape = (6, 63)

    for i, cob in enumerate(cobs):
        csv_name = f'{csv_files}/report_summary_{cob}_delayscan.csv'
        df = pd.read_csv(csv_name)
        #print(pd.unique(df.voltage))
    
        df.sort_values('timestamp', inplace=True)

        Vmask = df.voltage==voltage
        mradDose, idxs = np.unique(df.tid[Vmask].to_numpy(), return_index=True)
        xbins = np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]])
        settings = np.arange(shape[1])
    
        a, b = np.meshgrid(mradDose, settings)
        z = df[Vmask].drop(['timestamp','tid','voltage'], axis=1).to_numpy()[idxs]
        z = np.reshape(z, (z.shape[0], shape[0], shape[1]))[:,eTXnum,:].T.flatten()
    
        ybins = np.arange(0, shape[1], 1)
        h = axes[i].hist2d(a.flatten(), b.flatten(), weights=z, bins=(xbins, ybins), cmap=newmap, vmin=0., vmax=1.0)

        _xlim = axes[i].get_xlim()
        axes[i].set_xlim(-5., _xlim[1]*1.01)
        
        axes[i].set_xlabel('TID (Mrad)',  fontsize=16)
        axes[i].set_title(f"{cob} eTx {eTXnum} at {voltage}V", fontsize=12)
        tax = julyUtils.mark_TID_times(axes[i], cob, vsTID=vsTID)
        handles, labels = axes[i].get_legend_handles_labels()
        axes[i].legend(handles=handles, ncol=2, fontsize=8)

    axes[0].set_ylabel('Delay Select Setting', fontsize=16)
    cb=fig.colorbar(h[3])
    cb.set_label(label='Transmission error rate', size=16)
    cb.ax.set_yscale('linear')

def plot_voltages(cob, eTXnum, voltages, csv_files, outpath, vsTID=True):
    nVolts = len(voltages)
    fig, axes = plt.subplots(1, nVolts, figsize=(nVolts*4,5), 
                             sharey=True, layout='constrained')

    shape = (6, 63)

    csv_name = f'{csv_files}/report_summary_{cob}_delayscan.csv'
    df = pd.read_csv(csv_name)
    print(pd.unique(df.voltage))
    df.sort_values('timestamp', inplace=True)
    for i, volts in enumerate(voltages):    

        Vmask = df.voltage==volts
        mradDose, idxs = np.unique(df.tid[Vmask].to_numpy(), return_index=True)
        xbins = np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]])
        settings = np.arange(shape[1])
    
        a, b = np.meshgrid(mradDose, settings)
        z = df[Vmask].drop(['timestamp','tid','voltage'], axis=1).to_numpy()[idxs]
        z = np.reshape(z, (z.shape[0], shape[0], shape[1]))[:,eTXnum,:].T.flatten()
    
        ybins = np.arange(0, shape[1], 1)
        h = axes[i].hist2d(a.flatten(), b.flatten(), weights=z, bins=(xbins, ybins), cmap=newmap, vmin=0., vmax=1.0)
        
        axes[i].set_xlabel('TID (Mrad)',  fontsize=16)
        axes[i].set_title(f"eTx {eTXnum} at {volts}V", fontsize=12)

        # Update legend
        tax = julyUtils.mark_TID_times(axes[i], cob, vsTID=vsTID)
        handles, labels = axes[i].get_legend_handles_labels()
        axes[i].legend(handles=handles, ncol=2, fontsize=8)

    axes[0].set_ylabel('Delay Select Setting', fontsize=16)
    fig.suptitle(cob)
    cb=fig.colorbar(h[3])
    cb.set_label(label='Transmission error rate', size=16)
    cb.ax.set_yscale('linear')

def plot_eTXs(cob, voltage, csv_files, outpath, vsTID=True):
    fig, axes = plt.subplots(2, 3, figsize=(10,9), 
                             sharey=True, sharex=True, layout='constrained')
    axes = axes.reshape(-1)
    shape = (6, 63)

    csv_name = f'{csv_files}/report_summary_{cob}_delayscan.csv'
    df = pd.read_csv(csv_name)
    print(pd.unique(df.voltage))
    df.sort_values('timestamp', inplace=True)
    for eTXnum in range(6):    
        Vmask = df.voltage==voltage
        mradDose, idxs = np.unique(df.tid[Vmask].to_numpy(), return_index=True)
        xbins = np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]])
        settings = np.arange(shape[1])
    
        a, b = np.meshgrid(mradDose, settings)
        z = df[Vmask].drop(['timestamp','tid','voltage'], axis=1).to_numpy()[idxs]
        z = np.reshape(z, (z.shape[0], shape[0], shape[1]))[:,eTXnum,:].T.flatten()
    
        ybins = np.arange(0, shape[1], 1)
        h = axes[eTXnum].hist2d(a.flatten(), b.flatten(), weights=z, bins=(xbins, ybins), cmap=newmap, vmin=0., vmax=1.0)
        
        axes[eTXnum].set_title(f"eTx {eTXnum}", fontsize=12)

        if eTXnum in [2,5]:
            cb=fig.colorbar(h[3])
            cb.set_label(label='Transmission error rate', size=12)
            cb.ax.set_yscale('linear')

        # Update legend
        tax = julyUtils.mark_TID_times(axes[eTXnum], cob, vsTID=vsTID)
        handles, labels = axes[eTXnum].get_legend_handles_labels()
        axes[eTXnum].legend(handles=handles, ncol=2, fontsize=8)

    for eTXnum in range(3,6):
        axes[eTXnum].set_xlabel('TID (Mrad)',  fontsize=16)
    for eTXnum in [0,3]:
        axes[eTXnum].set_ylabel('Delay Select Setting', fontsize=16)
    fig.suptitle(f'{cob} at {voltage}V')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--cob', default = 'COB-10Pct-1-3')
    parser.add_argument('--voltages', nargs="+", default = None)
    parser.add_argument('--csv', type = str, default="/eos/user/h/hohare/ECONs/summary_csv_TID_July2025", help='Path to the csv file') 
    parser.add_argument('--outpath', default="/eos/user/h/hohare/ECONs/SanityPlots")
    parser.add_argument('--econd', action='store_true')
    parser.add_argument('--econt', action='store_true')
    args = parser.parse_args()

    if args.econd: shape = (6, 63)
    elif args.econt: shape = (13, 63)
    else:
        print('Must choose econd or econt')

    df = pd.read_csv(f'{args.csv}/report_summary_{args.cob}_delayscan.csv')
    args.outpath = f'{args.outpath}/{args.cob}/delayscans'
    os.makedirs(args.outpath, exist_ok=True)

    if not args.voltages:
        voltages = df.voltage.unique()
    for eTXnum in range(shape[0]):
        print(f'Plotting for eTXnum {eTXnum}')
        for volts in voltages:
            plot(df, args.cob, eTXnum, volts, args.outpath)