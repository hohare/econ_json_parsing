import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
args = parser.parse_args()
odir = args.odir + '/pllCapbank2D'
if not os.path.isdir(odir):
    os.makedirs(odir)
def plot_pllCapbankWidth_2D(voltage,pll_capbank_width,ymin,ymax,N,econType,odir):
    ymin, ymax = 0,15
    yrange=[i-0.5 for i in range(ymin,ymax+2)]
    plt.hist2d(voltage,
        pll_capbank_width,
        [[1.02,1.14,1.26,1.38],yrange],
        weights=[1/N]*3*N,
        vmax=1,vmin=0,
        cmin=1e-6)
    plt.xticks([1.08,1.20,1.32])
    plt.yticks(range(ymin,ymax+1))
    plt.colorbar()
    plt.xlabel('Operating voltage [V]')
    plt.ylabel('Width of capbank')
    plt.savefig(f'{odir}/pllCapbankWidth2DHist_{econType}.png',facecolor='w',dpi=300)
    plt.clf()

mongo_d = Database(args.dbaddress,client='econdDB')
mongo_t = Database(args.dbaddress,client='econtDB')

numchips = (len((mongo_d.pllCapbankWidthPlot(voltage='1p08', econType = 'ECOND'))))
econd1p08capwidth = mongo_d.pllCapbankWidthPlot(voltage='1p08', econType = 'ECOND')
econd1p2capwidth = mongo_d.pllCapbankWidthPlot(voltage='1p2', econType = 'ECOND')
econd1p32capwidth = mongo_d.pllCapbankWidthPlot(voltage='1p32', econType = 'ECOND')
capbank_width = []
voltage = []

for i in range((numchips)):
    voltage.append(1.08)
    voltage.append(1.2)
    voltage.append(1.32)
    capbank_width.append(econd1p08capwidth[i])
    capbank_width.append(econd1p2capwidth[i])
    capbank_width.append(econd1p32capwidth[i])
            
N = numchips
plot_pllCapbankWidth_2D(voltage,capbank_width,0,15,N,econType='ECOND',odir= args.odir + '/pllCapbank2D')

numchips = (len((mongo_t.pllCapbankWidthPlot(voltage='1p08', econType = 'ECONT'))))
econt1p08capwidth = mongo_t.pllCapbankWidthPlot(voltage='1p08', econType = 'ECONT')
econt1p2capwidth = mongo_t.pllCapbankWidthPlot(voltage='1p2', econType = 'ECONT')
econt1p32capwidth = mongo_t.pllCapbankWidthPlot(voltage='1p32', econType = 'ECONT')
capbank_width = []
voltage = []

for i in range((numchips)):
    voltage.append(1.08)
    voltage.append(1.2)
    voltage.append(1.32)
    capbank_width.append(econt1p08capwidth[i])
    capbank_width.append(econt1p2capwidth[i])
    capbank_width.append(econt1p32capwidth[i])

N = numchips
plot_pllCapbankWidth_2D(voltage,capbank_width,0,15,N,econType='ECONT',odir= args.odir + '/pllCapbank2D')
