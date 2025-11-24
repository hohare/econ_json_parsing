import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
map = mpl.colormaps['Reds']#['turbo']#['autumn_r']#['Reds']
newcolors = map(np.linspace(0,1,256))[50:]
newcolors[0, :] = [1., 1., 1., 1.]
newmap = ListedColormap(newcolors)

fontsize=16

def plot(df, cob, eRXnum, voltage, outpath):
    fig, ax = plt.subplots(figsize=(5,5))

    df.sort_values('timestamp', inplace=True)

    Vmask = df.voltage==voltage
    mradDose, idxs = np.unique(df.tid[Vmask].to_numpy(), return_index=True)
    xbins = np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]])
    settings = np.arange(15)

    a, b = np.meshgrid(mradDose, settings)
    z = df[Vmask].drop(['timestamp','tid','voltage'], axis=1).to_numpy()[idxs]
    z = np.reshape(z, (z.shape[0], 15, 12))[:,:,eRXnum].T.flatten()
    plt.set_yticks(settings)

    ybins = np.arange(0,16,1)
    h = plt.hist2d(a.flatten(), b.flatten(), weights=z, bins=(xbins, ybins), cmap=newmap, )#cmax=255)
    plt.set_xlabel('TID (Mrad)',  fontsize=16)
    plt.set_title(f"{cob} eRx {eRXnum} at {voltage}V", fontsize=12);
    
    cb=fig.colorbar(h[3])
    cb.set_label(label='Data transmission errors in PRBS', size=16)
    cb.ax.set_yscale('linear')
    
    plt.set_ylabel('Phase Select Setting', fontsize=16)

    if outpath:
        plt.savefig(f'{outpath}/delayScan_{cob}_eTXnum{eTXnum}_{voltage}V.png', dpi=300, facecolor="w",  bbox_inches='tight')
        plt.clf()
        plt.close()

def plot_voltages(cob, eRXnum, voltages, csv_files, outpath, vsTID=True):
    nVoltages = len(voltages)
    fig, axes = plt.subplots(1,nVoltages, figsize=(4*nVoltages,5), 
                             sharex=True, layout='constrained')
    axes = axes.reshape(-1)
    
    csv_name = f'{csv_files}/report_summary_{cob}_phasescan.csv'
    df = pd.read_csv(csv_name)
    print(pd.unique(df.voltage))

    df.sort_values('timestamp', inplace=True)

    for i, volts in enumerate(voltages):
        Vmask = df.voltage==volts
        mradDose, idxs = np.unique(df.tid[Vmask].to_numpy(), return_index=True)
        xbins = np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]])
        settings = np.arange(15)
    
        a, b = np.meshgrid(mradDose, settings)
        z = df[Vmask].drop(['timestamp','tid','voltage'], axis=1).to_numpy()[idxs]
        z = np.reshape(z, (z.shape[0], 15, 12))[:,:,eRXnum].T.flatten()
        axes[i].set_yticks(settings)
        axes[i].tick_params(axis='both', which='major', labelsize=fontsize)
    
        ybins = np.arange(0,16,1)
        h = axes[i].hist2d(a.flatten(), b.flatten(), weights=z, bins=(xbins, ybins), cmap=newmap, cmax=255)
        axes[i].set_title(f"{volts} V", fontsize=fontsize)
        axes[i].set_xlabel('TID (Mrad)',  fontsize=fontsize)

        # Update y labels
        yticks = np.arange(0, 15)
        axes[i].tick_params(axis='y', which='minor', left=False, right=False)
        axes[i].set_yticks(yticks, minor=False)
        
    cb=fig.colorbar(h[3])
    cb.ax.set_yscale('linear')
            
    fig.suptitle(f'Data transmission errors in PRBS for {cob} at eRX {eRXnum}', fontsize=20)
    axes[0].set_ylabel('Phase Select Setting', fontsize=20)

    if outpath:
        outpath = f'{outpath}/{cob}/phasescans'
        os.makedirs(outpath, exist_ok=True)
        plt.savefig(f'{outpath}/phaseScans_{voltage}V.png', dpi=300, facecolor="w", bbox_inches='tight')
        plt.clf()
        plt.close()

def plot_cobs(cobs, eRXnum, voltage, csv_files, outpath, vsTID=True):
    ncobs = len(cobs)
    #if ncobs>3: nrows=2
    fig, axes = plt.subplots(nrows, ncobs, figsize=(ncobs*4,5), sharey=True, layout='constrained')
    if ncobs==1: axes = [axes]

    for i, cob in enumerate(cobs):
        csv_name = f'{csv_files}/report_summary_{cob}_phasescan.csv'
        df = pd.read_csv(csv_name)

        if i==0: print(pd.unique(df.voltage))
    
        df.sort_values('timestamp', inplace=True)

        Vmask = df.voltage==voltage
        mradDose, idxs = np.unique(df.tid[Vmask].to_numpy(), return_index=True)
        xbins = np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]])
        settings = np.arange(15)
    
        a, b = np.meshgrid(mradDose, settings)
        z = df[Vmask].drop(['timestamp','tid','voltage'], axis=1).to_numpy()[idxs]
        z = np.reshape(z, (z.shape[0], 15, 12))[:,:,eRXnum].T.flatten()
        axes[i].set_yticks(settings)
    
        ybins = np.arange(0,16,1)
        h = axes[i].hist2d(a.flatten(), b.flatten(), weights=z, bins=(xbins, ybins), cmap=newmap, cmax=255)
        axes[i].set_xlabel('TID (Mrad)',  fontsize=16)
        axes[i].set_title(f"{cob} eRx {eRXnum} at {voltage}V", fontsize=12);

        # Update y labels
        yticks = np.arange(0, 15)
        axes[i].tick_params(axis='y', which='minor', left=False, right=False)
        axes[i].set_yticks(yticks, minor=False)
        
    cb=fig.colorbar(h[3])
    cb.set_label(label='Data transmission errors in PRBS', size=16)
    cb.ax.set_yscale('linear')
    
    axes[0].set_ylabel('Phase Select Setting', fontsize=16)

    if outpath:
        outpath = f'{outpath}/{cobs[0]}/phasescans'
        os.makedirs(args.outpath, exist_ok=True)
        plt.savefig(f'{outpath}/phaseScans_{voltage}V.png', dpi=300, facecolor="w", bbox_inches='tight')
        plt.clf()
        plt.close()

def plot_eRXs(cob, voltage, csv_files, outpath, vsTID=True):
    fig, axes = plt.subplots(3, 4, figsize=(10,8), 
                             sharex=True, sharey=True, layout='constrained')
    axes = axes.reshape(-1)
    
    csv_name = f'{csv_files}/report_summary_{cob}_phasescan.csv'
    df = pd.read_csv(csv_name)
    #print(pd.unique(df.voltage))

    df.sort_values('timestamp', inplace=True)

    Vmask = df.voltage==voltage
    mradDose, idxs = np.unique(df.tid[Vmask].to_numpy(), return_index=True)
    xbins = np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]])
    settings = np.arange(15)

    a, b = np.meshgrid(mradDose, settings)
    for eRXnum in range(12):
        z = df[Vmask].drop(['timestamp','tid','voltage'], axis=1).to_numpy()[idxs]
        z = np.reshape(z, (z.shape[0], 15, 12))[:,:, eRXnum].T.flatten()
    
        ybins = np.arange(0,16,1)
        h = axes[eRXnum].hist2d(a.flatten(), b.flatten(), weights=z, bins=(xbins, ybins), cmap=newmap, cmax=255)
        axes[eRXnum].set_yticks(settings)
        axes[eRXnum].tick_params(axis='both', which='major', labelsize=12)
        axes[eRXnum].set_title(f"eRx {eRXnum}", fontsize=10)

        # Update y labels
        yticks = np.arange(0, 15)
        axes[eRXnum].tick_params(axis='y', which='minor', left=False, right=False)
        axes[eRXnum].set_yticks(yticks, minor=False)
        
        if eRXnum in [3,7,11]:
            cb=fig.colorbar(h[3])
            cb.ax.set_yscale('linear')

    fig.suptitle(f'Data transmission errors in PRBS for {cob} at {voltage} V', fontsize=20)
    for i in range(8,12):
        axes[i].set_xlabel('TID (Mrad)',  fontsize=16)
    axes[4].set_ylabel('Phase Select Setting', fontsize=20)

    if outpath:
        outpath = f'{outpath}/{cob}/phasescans'
        os.makedirs(outpath, exist_ok=True)
        plt.savefig(f'{outpath}/phaseScans_{voltage}V.png', dpi=300, facecolor="w", bbox_inches='tight')
        plt.clf()
        plt.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--cob', nargs="+", default = 'COB-10Pct-1-3')
    parser.add_argument('--voltages', nargs="+", default = None)
    parser.add_argument('--csv', type = str, default="/eos/user/h/hohare/ECONs/summary_csv_TID_July2025", help='Path to the csv file') 
    parser.add_argument('--outpath', default="/eos/user/h/hohare/ECONs/SanityPlots")
    args = parser.parse_args()

    if len(args.cob)==1: args.cob=[args.cob]
    print(args.cob)

    for eRXnum in range(12):
        print(f'Plotting for eRXnum {eRXnum}')
        plot_cobs(args.cob, eRXnum, args.voltages, args.csv, args.outpath)