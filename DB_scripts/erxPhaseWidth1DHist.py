import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
import datetime
from datetime import timedelta

parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './')
args = parser.parse_args()
odir = args.odir + '/test_io'

if not os.path.isdir(odir):
    os.makedirs(odir)
currentDate = datetime.datetime.now()

def plot_eRxPhaseWidth(array,voltage,ECON_type,odir, perDay=None):
    plt.hist(array.flatten(), 
             bins= np.arange(0,9,1)-0.5,
             color='b',
             alpha=0.5,
             label=f"eRx Phase width \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}")

    underflow = np.sum(array < 0)
    overflow = np.sum(array > 9)
    legend_text = f'Underflow: {underflow}, Overflow: {overflow}'
    data = array.flatten()
    numFailed = len(data[data < 3])
    fracFailed = np.round((numFailed/len(array)),3)

    if perDay is not None:
        formatted_dt = perDay.strftime('%Y-%m-%d_%H-%M-%S')
        odir = odir +'/perDay' +f'/{formatted_dt}'
        if not os.path.isdir(odir):
            os.makedirs(odir)
        plt.title(f"{ECON_type} eRx width [{voltage}] - {formatted_dt}")
    if perDay is None:
        plt.title(f"{ECON_type} eRx width [{voltage}]")
        
   
    plt.axvline(x=3,
                color='black', 
                alpha=0.5, 
                label="Thresold = 3", 
                linestyle='--')

    plt.grid(color='black', linestyle='--', linewidth=.05)
    plt.gca().xaxis.set_minor_locator(plt.NullLocator())
    plt.legend([f"N Chips: {len(array)} \neRx Phase width \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}",
                f"Thresold = 3 \nFrac Failed: {fracFailed}",
               legend_text],
               loc="upper left",fontsize='15')

    plt.ylabel('Number of eRx')
    plt.xlabel('Phase width')

    plt.savefig(f'{odir}/Phase_width__of_all_eRx_{ECON_type} [{voltage}].png', dpi=300, facecolor = "w")

    plt.clf()
    return plt

mongo_d = Database(args.dbaddress,client = 'econdDB')
mongo_t = Database(args.dbaddress,client = 'econtDB')


temp = [['1p08', '1p2', '1p32'], [1.08, 1.2, 1.32]]
for i in range(3):
    plot_eRxPhaseWidth(mongo_d.prbsMaxWidthPlot(voltage=temp[0][i], econType = 'ECOND'), voltage = temp[1][i], ECON_type='ECON-D', odir= odir)
    plot_eRxPhaseWidth(mongo_t.prbsMaxWidthPlot(voltage=temp[0][i], econType = 'ECONT'), voltage = temp[1][i], ECON_type='ECON-T', odir= odir)

for i in range(3):
    try:
        plot_eRxPhaseWidth(mongo_d.prbsMaxWidthPlot(voltage=temp[0][i], econType = 'ECOND', perDay=currentDate), voltage = temp[1][i], ECON_type='ECON-D', odir= odir, perDay=currentDate)
    except:
        print(f"No data for ECON-D taken within: {(currentDate - timedelta(days=1)).strftime('%Y-%m-%d_%H-%M-%S')} to {currentDate.strftime('%Y-%m-%d_%H-%M-%S')}")

for i in range(3):
    try:
        plot_eRxPhaseWidth(mongo_t.prbsMaxWidthPlot(voltage=temp[0][i], econType = 'ECONT', perDay=currentDate), voltage = temp[1][i], ECON_type='ECON-T', odir= odir, perDay=currentDate)
    except:
        print(f"No data for ECON-T taken within: {(currentDate - timedelta(days=1)).strftime('%Y-%m-%d_%H-%M-%S')} to {currentDate.strftime('%Y-%m-%d_%H-%M-%S')}")
