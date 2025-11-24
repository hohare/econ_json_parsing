import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import July_2025_TID_utils as julyUtils
#sys.path.append('..')
import econ_json_parsing.plotting_scripts.utilities as utils

marker_cycle = ['v','^','<','>', 'x', '+']

def plot(df, cob, voltage, outpath):
    print(f'Plotting {voltage}V')
    fig, ax = plt.subplots(figsize=(10,5))

    mask = df.voltage==voltage
    mradDose = df.tid[mask]
    automatic_capbank_setting = df.automatic_capbank_setting[mask]
    plt.scatter(mradDose, automatic_capbank_setting, s=4, )#label=str(v)+"V")
    _xlim = ax.get_xlim()
    plt.xlim(-5., _xlim[1]*1.01)
    julyUtils.mark_TID_times(ax, cob, vsTID=True)
    plt.ylabel('Automatic capbank selection')
    plt.xlabel("TID (MRad)")
    plt.xticks(rotation=90)
    ax.set_title(f'{cob} @ {voltage} V')

    plt.legend(fontsize=12)

    voltage = str(voltage).replace('.','p')
    plt.savefig(f'{outpath}/capbankSelection_{cob}_{voltage}V.png', bbox_inches='tight', dpi=300, facecolor="w")
    plt.clf()
    plt.close()

def plot_voltages2(args):
    cob = args.cobs[0]
    voltages = args.voltages
    csv_files = args.csv
    outpath = args.outpath

def plot_voltages(cob, voltages, csv_files, outpath, time=False):
    csv_name = f'{csv_files}/report_summary_{cob}_autoCapbankSelection.csv'
    df = pd.read_csv(csv_name)
    fontsize=16

    maxx = 0
    minn = 511
    fig, ax = plt.subplots(figsize=(8,5))
    for i,volts in enumerate(voltages):
        mask = df.voltage==float(volts)
        mradDose = df.tid[mask]
        automatic_capbank_setting = df.automatic_capbank_setting[mask]
        plt.scatter(mradDose, automatic_capbank_setting, s=5, label=f'{volts} V', 
                    facecolors='none', edgecolor=julyUtils.color_cycle[i], marker=utils.marker_cycle[i])

        if np.min(automatic_capbank_setting)<minn: minn = np.min(automatic_capbank_setting)
        if np.max(automatic_capbank_setting)>maxx: maxx = np.max(automatic_capbank_setting)


    # Update y labels
    yticks = np.arange(np.min(20,minn),np.max(31,maxx+1))
    ax.tick_params(axis='y', which='minor', left=False, right=False)
    ax.set_yticks(yticks, minor=False)
    plt.ylabel('Automatic capbank selection', fontsize=fontsize)
    # Update x labels
    _xlim = ax.get_xlim()
    plt.xlim(-5., _xlim[1]*1.01)
    plt.ylabel('Automatic capbank selection', fontsize=fontsize)
    plt.xlabel("TID (MRad)", fontsize=fontsize)
    plt.xticks(rotation=90)
    ax.tick_params(axis='both', which='major', labelsize=fontsize)
    ax.tick_params(axis='both', which='minor', labelsize=fontsize)
    ax.set_title(cob, fontsize=fontsize)

    tax = julyUtils.mark_TID_times(ax, cob, leg_loc='right', vsTID=True)
    ax.add_artist(tax)
    ax.legend(fontsize=14, ncol=3, frameon=True, loc='lower right')

    if outpath:
        voltage = "_".join([str(v).replace('.','p') for v in voltages])
        plt.savefig(f'{outpath}/capbankSelection_{cob}_{cobs}.png', bbox_inches='tight', dpi=300, facecolor="w")
        plt.clf()
        plt.close()

def plot_cobs(cob_list, voltage, csv_files, vsTID=True, plot50mA=False):
    outpath = None
    fontsize=20
    
    df_dict = {}
    for cob in cob_list:
        csv_name = f'{csv_files}/report_summary_{cob}_autoCapbankSelection.csv'
        df_dict[cob] = pd.read_csv(csv_name)

    fig, ax = plt.subplots(figsize=(8,5))
    maxx = 31
    minn = 20
    for i,cob in enumerate(df_dict):
        mask = df_dict[cob].voltage==float(voltage)
        if vsTID:
            x = df_dict[cob].tid[mask]
        else:
            x = [np.datetime64(t) for t in df_dict[cob].timestamp[mask]] 
           
        automatic_capbank_setting = df_dict[cob].automatic_capbank_setting[mask]
        plt.scatter(x, automatic_capbank_setting+0.05*i, s=20, label=cob, 
                    marker=utils.marker_cycle[i], color=julyUtils.color_cycle[i], )#alpha=0.5)

        if np.min(automatic_capbank_setting)<minn: minn = np.min(automatic_capbank_setting)
        if np.max(automatic_capbank_setting)>maxx: maxx = np.max(automatic_capbank_setting)

    # Update y labels
    yticks = np.arange(minn, maxx)
    ax.tick_params(axis='y', which='minor', left=False, right=False)
    ax.set_yticks(yticks, minor=False)
    plt.ylabel('Automatic capbank selection', fontsize=fontsize)
    # Update x labels
    _xlim = ax.get_xlim()
    if vsTID:
        plt.xlim(-5., _xlim[1]*1.01)
        plt.xlabel("TID (MRad)", fontsize=16)
        plt.xticks(rotation=90)
    else:
        plt.xticks(rotation=45, ha='right')
    ax.tick_params(axis='both', which='major', labelsize=fontsize)
    
    ax.set_title(f'{voltage} V', fontsize=fontsize)
    # Apply xray lines lines and legend
    utils.plot_TID_end(ax, cob_list, plot50mA=plot50mA)
    handles, labels = ax.get_legend_handles_labels()
    handles = handles[:len(cob_list)]
    if plot50mA: handles.append(Line2D([0], [0], color='k', ls='dotted',lw=2, label='X-ray on 50 mA'))
    handles.append(Line2D([0], [0], color='k', ls='dashed',lw=2, label='X-rays Off'))
    plt.legend(handles=handles, fontsize=12, frameon=True)

    if outpath:
        voltage = str(voltage).replace('.','p')
        cobs = "_".join(cob_list)
        plt.savefig(f'{outpath}/capbankSelection_{voltage}V_{cobs}.png', bbox_inches='tight', dpi=300, facecolor="w")
        plt.clf()
        plt.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--cobs', nargs="+", default = 'COB-10Pct-1-3')
    parser.add_argument('--voltages', nargs="+", default=None)
    parser.add_argument('--csv', type = str, default="/eos/user/h/hohare/ECONs/summary_csv_TID_July2025", help='Path to the csv file') 
    parser.add_argument('--outpath', default="/eos/user/h/hohare/ECONs/SanityPlots")
    args = parser.parse_args()

    if len(args.cobs)==1 and len(args.voltages)==1:
        cob = args.cobs[0]
        
        args.outpath = f'{args.outpath}/{cob}/autoCapbankSelection'
        os.makedirs(args.outpath, exist_ok=True)
        
        df = pd.read_csv(f'{args.csv}/report_summary_{cob}_autoCapbankSelection.csv')
        if not args.voltages: args.voltages = df.voltage.unique()
        for volts in args.voltages:
            plot(df, cob, volts, args.outpath)
    elif len(args.cobs)==1:
        args.outpath = f'{args.outpath}/autoCapbankSelection'
        os.makedirs(args.outpath, exist_ok=True)
        plot_cobs(args)
    elif len(args.cobs)==1:
        args.outpath = f'{args.outpath}/autoCapbankSelection'
        os.makedirs(args.outpath, exist_ok=True)
        plot_voltages(args)
