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
odir = args.odir + '/PhaseScanErrors'
if not os.path.isdir(odir):
    os.makedirs(odir)
def plot_eRx_phaseScan(_fileName=None,dataArray=None,outputFileName=None,title='eRx Phase Scan'):
    if _fileName is not None:
        if 'json' in _fileName:
            data = json.load(open(_fileName))
            for t in data['tests']:
                if 'test_ePortRXPRBS[1.2]' in t['nodeid']:
                    data = np.array(t['metadata']['eRX_errcounts'])
        else:
            if dataArray is None:
                data=np.load(_fileName)
            else:
                data=dataArray
    else:
        data=dataArray

    fig,ax=plt.subplots()

    a,b=np.meshgrid(np.arange(12),np.arange(15))

    h=plt.hist2d(a.flatten(),
                 b.flatten(),
                 weights=data.flatten(),
                 bins=(np.arange(13)-.5,
                       np.arange(16)-.5),
                 cmap='RdYlBu_r',
                 alpha=data>0,
                 figure=fig);
    cb=fig.colorbar(h[3])
    cb.set_label(label='Data transmission errors in PRBS')
    cb.ax.set_yscale('linear')

    plt.ylabel('Phase Select Setting')
    plt.xlabel('Channel Number')
    plt.xticks(np.arange(12))
    plt.yticks(np.arange(15))
    plt.title(title)
    if outputFileName is not None:
        plt.savefig(outputFileName,dpi=300, facecolor = "w")

    plt.close(fig)

    return fig

mongo = Database(args.dbaddress)
data = mongo.phaseScan2DPlot(args.chipNum, econType = args.econType, voltage = args.voltage)
plot_eRx_phaseScan(_fileName=None,dataArray=data,outputFileName= odir + f'/chip_{args.chipNum}_phaseScanErrors_{args.econType}_{args.voltage}',title=f'eRx Phase Scan {args.voltage}V')
