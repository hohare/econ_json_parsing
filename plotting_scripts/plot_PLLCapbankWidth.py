import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
sys.path.append('..')
import July_2025_TID_utils as julyUtils
import econ_json_parsing.plotting_scripts.utilities as utils

fontsize = 16

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

    if outpath:
        voltage = str(voltage).replace('.','p')
        plt.savefig(f'{outpath}/capbankWidth_{cob}_{voltage}V.png', dpi=300, facecolor="w", bbox_inches='tight')
        plt.clf()
        plt.close()

def plot_voltages(cob, voltages, csv_files, outpath, vsTID=True):
    csv_name = f'{csv_files}/report_summary_{cob}_pllCapbankWidth.csv'
    df = pd.read_csv(csv_name)
    fig, ax = plt.subplots(figsize=(8,5))

    print(pd.unique(df.voltage))

    minn = 0.
    maxx = 20.
    for i,volts in enumerate(voltages):
        mask = df.voltage==volts
        if vsTID: x = df.tid[mask]
        else: x = x = [np.datetime64(t) for t in df.timestamp[mask]]
        pll_capbank_width = df.pll_capbank_width[mask]
        plt.scatter(x, pll_capbank_width+0.05*i, s=10, label=str(volts)+"V",  marker=utils.marker_cycle[i])
        if np.min(pll_capbank_width)<minn: minn = np.min(pll_capbank_width)
        if np.max(pll_capbank_width)>maxx: maxx = np.max(pll_capbank_width)

    # Update y labels
    yticks = np.arange(minn, maxx+1)
    ax.tick_params(axis='y', which='minor', left=False, right=False)
    ax.set_yticks(yticks, minor=False)
    plt.ylabel('PllCapbankWidth', fontsize=fontsize)
    if vsTID:
        _xlim = ax.get_xlim()
        plt.xlim(-5., _xlim[1]*1.01)
        plt.xlabel("TID (MRad)", fontsize=fontsize)
        plt.xticks(rotation=90, fontsize=fontsize)
    else:
        plt.xticks(rotation=60, fontsize=fontsize, ha='right')
    
    ax.set_title(f'{cob}', fontsize=fontsize)
    tax = julyUtils.mark_TID_times(ax, cob, vsTID=vsTID)
    
    plt.legend(fontsize=fontsize, ncols=3,frameon=True);

def plot_cobs(cobs, voltage, csv_files, outpath, vsTID=False, plot50mA=False):
    fontsize=16
    fig, ax = plt.subplots(figsize=(8,5))

    minn = 0.
    maxx = 20.
    for i,cob in enumerate(cobs):
        csv_name = f'{csv_files}/report_summary_{cob}_pllCapbankWidth.csv'
        df = pd.read_csv(csv_name)
        #print(pd.unique(df.voltage))
    
        mask = df.voltage==voltage
        if vsTID: x = df.tid[mask]
        else: x = [np.datetime64(t) for t in df.timestamp[mask]]
        pll_capbank_width = df.pll_capbank_width[mask]
        plt.scatter(x, pll_capbank_width+0.05*i, s=10, label=cob, alpha=0.6, marker=utils.marker_cycle[i])

        if np.min(pll_capbank_width)<minn: minn = np.min(pll_capbank_width)
        if np.max(pll_capbank_width)>maxx: maxx = np.max(pll_capbank_width)

    # Update y labels
    yticks = np.arange(minn, maxx+1)
    ax.tick_params(axis='y', which='minor', left=False, right=False)
    ax.set_yticks(yticks, minor=False)
    plt.ylabel('PllCapbankWidth', fontsize=fontsize)
        
    if vsTID:
        _xlim = ax.get_xlim()
        plt.xlim(-5., _xlim[1]*1.01)
        plt.xticks(rotation=90, fontsize=fontsize)
        plt.xlabel("TID (MRad)", fontsize=fontsize)
    else:
        plt.xticks(rotation=60, fontsize=fontsize, ha='right')
    #tax = julyUtils.mark_TID_times(ax, cob, vsTID=True)

    # Apply xray lines lines and legend
    utils.plot_TID_end(ax, cobs, plot50mA=plot50mA)
    handles, labels = ax.get_legend_handles_labels()
    handles = handles[:len(cobs)]
    if plot50mA: handles.append(Line2D([0], [0], color='k', ls='dotted',lw=2, label='X-ray on 50 mA'))
    handles.append(Line2D([0], [0], color='k', ls='dashed',lw=2, label='X-rays Off'))
    plt.legend(handles=handles, fontsize=12, frameon=True, loc='lower right')
    
    ax.set_title(f'{voltage} V', fontsize=fontsize)
    

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



