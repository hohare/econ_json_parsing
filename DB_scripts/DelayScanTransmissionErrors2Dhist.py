import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="DB address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory for plots", default = './plots')
parser.add_argument("--chipNum", help="chip number", default = 101)
parser.add_argument("--econType", help="ECONT or ECOND as a string", default = 'ECOND')
parser.add_argument("--voltage", help="voltage: use 1p08, 1p2, or 1p32", default = '1p2')
args = parser.parse_args()
odir = args.odir + '/DelayScanErrors'
if not os.path.isdir(odir):
    os.makedirs(odir)
def delay_scan_plots(errcounts,
                     bitcounts,
                     econType,
                     voltage,
                     chipNum,
                     odir):
    x = errcounts
    y = bitcounts
    errorRates = (x/y).T.flatten()
    nBins = x.shape[0]

    a,b=np.meshgrid(np.arange(nBins),np.arange(63))
    fig,ax=plt.subplots()

    plt.hist2d(a.flatten(),b.flatten(),
               weights=errorRates,
               bins=(np.arange(nBins+1)-0.5,np.arange(64)-0.5),
               cmap='RdYlBu_r',
               alpha=errorRates>0,
               figure=fig);

    plt.colorbar().set_label(label='Transmission errors rate')
    plt.title(f'eTx Delay Scan {voltage}V')
    plt.ylabel('Phase Select Setting')
    plt.xlabel('Channel Number')
    plt.savefig(f'{odir}/{econType}_chip_{chipNum}_delayScan_{voltage}.png',dpi=300, facecolor = "w")
   
    plt.close(fig)

    return fig



if args.econType == 'ECOND':
    client = 'econdDB'
else:
    client = 'econdtDB'
mongo = Database(args.dbaddress,client= client)
bitcounts, errcounts = mongo.delayScan2DPlot(args.chipNum, econType = args.econType, voltage = args.voltage)

delay_scan_plots(errcounts, bitcounts, args.econType, args.voltage, args.chipNum, args.odir+'/DelayScanErrors')
