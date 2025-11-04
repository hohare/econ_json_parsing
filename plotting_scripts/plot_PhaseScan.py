import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot(df, cob, eRXnum, voltage, outpath):
    fig, ax = plt.subplots(figsize=(5,5))

    df.sort_values('timestamp', inplace=True)

    Vmask = df.voltage==voltage
    mradDose = df.tid[Vmask]
    settings = np.arange(15)

    a, b = np.meshgrid(mradDose, settings)
    z = df[Vmask].drop(['timestamp','tid','voltage'], axis=1).to_numpy()
    z = np.reshape(z, shape=(z.shape[0], 12, 15))[:,eRXnum,:].T.flatten()
    ax.set_yticks(settings)

    ybins = np.arange(0,16,1)
    h = plt.hist2d(a.flatten(), b.flatten(), weights=z, bins=(mradDose, ybins), cmap='RdYlBu_r', cmax=255)
    cb=fig.colorbar(h[3])
    cb.set_label(label='Data transmission errors in PRBS', size=16)
    cb.ax.set_yscale('linear')

    plt.xlabel('TID (Mrad)',  fontsize=16)
    plt.ylabel('Phase Select Setting', fontsize=16)
    plt.title(f"eRx {eRXnum} at {voltage}V");

    voltage = str(voltage).replace('.','p')
    xlim = ax.get_xlim()
    if xlim[1]>0:
        plt.savefig(f'{outpath}/phaseScan_{cob}_eRXnum{eRXnum}_{voltage}V.png', dpi=300, facecolor="w")
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

    args.outpath = f'{args.outpath}/{args.cob}/phasescans'
    os.makedirs(args.outpath, exist_ok=True)

    df = pd.read_csv(f'{args.csv}/report_summary_{args.cob}_phasescan.csv')
    

    if not args.voltages:
        voltages = df.voltage.unique()
    for eRXnum in range(12):
        print(f'Plotting for eRXnum {eRXnum}')
        for volts in voltages:
            plot(df, args.cob, eRXnum, volts, args.outpath)
