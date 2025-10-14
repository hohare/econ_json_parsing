import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
args = parser.parse_args()
odir = args.odir + '/eTxPhaseWidth2DHist'
if not os.path.isdir(odir):
    os.makedirs(odir)
def plot_delayscan_2D(voltage,delay_width,ymin,ymax,N,ECON_type,io_type,odir):
    if(io_type=='eRx'):
        Nrow,Ncol = 3,4
        Nchannel = 12
    elif (io_type=='eTx' and ECON_type=='ECONT'):
        Nrow,Ncol = 3,5
        Nchannel = 13
    elif (io_type=='eTx' and ECON_type=='ECOND'):
        Nrow,Ncol = 2,3
        Nchannel = 6
    else:
        raise Exception("check io and ECON_type")  

    plt.figure(figsize=(16,16))
    fig, axs = plt.subplots(Nrow,Ncol,layout='constrained')
    for i in range(Nchannel):
        yrange=[i-0.5 for i in range(ymin,ymax+2)]
        axs[int(i/Ncol),i%Ncol].text(1.2, 5/6*ymin+1/5*ymax,
                                     f'{io_type}{i}', 
                                     horizontalalignment='center', 
                                     verticalalignment='center', 
                                     color='#ff7700')
        b=axs[int(i/Ncol),i%Ncol].hist2d(voltage[i],
                                         delay_width[i],
                                         [[1.02,1.14,1.26,1.38],yrange],
                                         weights=[1/N]*3*N,
                                         vmax=1,vmin=0,
                                         cmin=1e-6)
        axs[int(i/Ncol),i%Ncol].set_xticks([1.08,1.20,1.32])
        axs[int(i/Ncol),i%Ncol].set_yticks(range(ymin,ymax+1))
        axs[int(i/Ncol),i%Ncol].tick_params(axis='both', which='major', labelsize=10)
    pcm = b[3]
    fig.colorbar(pcm, ax=axs, location='right')
    if (io_type=='eTx' and ECON_type=='ECONT'):
        axs[2,3].remove()
        axs[2,4].remove()
    fig.savefig(f'{odir}/eRxPhaseScan2D_{ECON_type}.png', facecolor='w', dpi=300)

mongo_d = Database(args.dbaddress,client='econdDB')
mongo_t = Database(args.dbaddress,client='econtDB')



etxPhase1p08 = mongo_d.etxMaxWidthPlot(voltage='1p08', econType = 'ECOND')
etxPhase1p2 = mongo_d.etxMaxWidthPlot(voltage='1p2', econType = 'ECOND')
etxPhase1p32 = mongo_d.etxMaxWidthPlot(voltage='1p32', econType = 'ECOND')
N = len(etxPhase1p08)
voltages = []
widths = []
for i in range(6):
    width = []
    voltage = []
    for j in range(N):
        width.append(etxPhase1p08[j][i])
        width.append(etxPhase1p2[j][i])
        width.append(etxPhase1p32[j][i])
        voltage.append(1.08)
        voltage.append(1.2)
        voltage.append(1.32)
    voltages.append(voltage)
    widths.append(width)

plot_delayscan_2D(voltages,widths,0,19,N,'ECOND','eTx', odir)
    
etxPhase1p08 = mongo_t.etxMaxWidthPlot(voltage='1p08', econType = 'ECONT')
etxPhase1p2 = mongo_t.etxMaxWidthPlot(voltage='1p2', econType = 'ECONT')
etxPhase1p32 = mongo_t.etxMaxWidthPlot(voltage='1p32', econType = 'ECONT')
N = len(etxPhase1p08)
voltages = []
widths = []
for i in range(13):
    width = []
    voltage = []
    for j in range(N):
        width.append(etxPhase1p08[j][i])
        width.append(etxPhase1p2[j][i])
        width.append(etxPhase1p32[j][i])
        voltage.append(1.08)
        voltage.append(1.2)
        voltage.append(1.32)
    voltages.append(voltage)
    widths.append(width)

plot_delayscan_2D(voltages,widths,0,19,N,'ECONT','eTx', odir)




