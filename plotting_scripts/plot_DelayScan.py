import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot(df, cob, eTXnum, voltage, outpath):
    shape = (6, 63)

    fig, ax = plt.subplots(figsize=(5,5))

    df.sort_values('timestamp', inplace=True)

    Vmask = df.voltage==voltage
    mradDose = df.tid[Vmask]
    settings = np.arange(shape[1])

    a, b = np.meshgrid(mradDose, settings)
    z = df[Vmask].drop(['timestamp','tid','voltage'], axis=1).to_numpy()
    z = np.reshape(z, shape=(z.shape[0], shape[0], shape[1]))[:,eTXnum,:].T.flatten()

    ybins = np.arange(0, shape[1], 1)
    h = plt.hist2d(a.flatten(), b.flatten(), weights=z, bins=(mradDose, ybins), cmap='RdYlBu_r', vmin=0., vmax=1.0)
    cb=fig.colorbar(h[3])
    cb.set_label(label='ransmission error rate', size=16)
    cb.ax.set_yscale('linear')

    plt.xlabel('TID (Mrad)',  fontsize=16)
    plt.ylabel('Phase Select Setting', fontsize=16)
    plt.title(f"eTx {eTXnum} at {voltage}V")

    voltage = str(voltage).replace('.','p')
    plt.savefig(f'{outpath}/delayScan_{cob}_eTXnum{eTXnum}_{voltage}V.png', dpi=300, facecolor="w")
    plt.clf()
    plt.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--cob', default = 'COB-10Pct-1-3')
    parser.add_argument('--voltages', nargs="+", default = None)
    parser.add_argument('--csv', type = str, default="/Users/suzannehare/Desk/econ_testing/TID_sanity_checks/csv_files", help='Path to the csv file') 
    parser.add_argument('--outpath', default="/Users/suzannehare/Desk/econ_testing/plots")
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
    for eRXnum in range(shape[0]):
        print(f'Plotting for eTXnum {eRXnum}')
        for volts in voltages:
            plot(df, args.cob, eRXnum, volts, args.outpath)