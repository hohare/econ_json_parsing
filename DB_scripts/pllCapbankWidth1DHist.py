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
odir = args.odir + '/test_pll'
if not os.path.isdir(odir):
    os.makedirs(odir)

currentDate = datetime.datetime.now()
#A function to plot the capbank width
def plot_pllCapbankWidth(array,voltage,ECON_type,odir, perDay=None):
    plt.hist(array, 
             bins= np.arange(10,18,1)-0.5,
             color='b',
             alpha=0.5,
             label=f"Capbank width \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}")

    underflow = np.sum(array < 10)
    overflow = np.sum(array > 18)
    legend_text = f'Underflow: {underflow}, Overflow: {overflow}'
    numFailed = len(array[array<12])
    fracFailed = np.round((numFailed/len(array)),3)
    if perDay is not None:
        formatted_dt = perDay.strftime('%Y-%m-%d_%H-%M-%S')
        odir = odir +'/perDay' +f'/{formatted_dt}'
        if not os.path.isdir(odir):
            os.makedirs(odir)
        plt.title(f"{ECON_type} Capbank Width [{voltage}] - {formatted_dt}")
    if perDay is None:
        plt.title(f"{ECON_type} Capbank Width [{voltage}]")
    
    plt.axvline(x=12,
                color='black', 
                alpha=0.5, 
                label="Thresold = 12", 
                linestyle='--')

    plt.grid(color='black', linestyle='--', linewidth=.05)
    plt.gca().xaxis.set_minor_locator(plt.NullLocator())
    plt.legend([f"N Chips: {len(array)} \nCapbank width \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}",
                f"Threshold = 12 \nFrac Failed: {fracFailed}",
               legend_text],
               loc="best",fontsize='15')

    plt.ylabel('Count')
    plt.xlabel('Capbank Width')

    plt.savefig(f'{odir}/{ECON_type}_Capbank_Width [{voltage}].png', dpi=300, facecolor = "w")
    plt.clf()
    return plt

mongo_d = Database(args.dbaddress,client='econdDB')
mongo_t = Database(args.dbaddress,client='econtDB')


temp = [['1p08', '1p2', '1p32'], [1.08, 1.2, 1.32]]
for i in range(3):
    plot_pllCapbankWidth(mongo_d.pllCapbankWidthPlot(voltage=temp[0][i], econType = 'ECOND'), voltage = temp[1][i], ECON_type='ECON-D', odir=odir)
    plot_pllCapbankWidth(mongo_t.pllCapbankWidthPlot(voltage=temp[0][i], econType = 'ECONT'), voltage = temp[1][i], ECON_type='ECON-T', odir=odir)

for i in range(3):
    try:
        plot_pllCapbankWidth(mongo_d.pllCapbankWidthPlot(voltage=temp[0][i], econType = 'ECOND', perDay=currentDate), voltage = temp[1][i], ECON_type='ECON-D', odir=odir, perDay=currentDate)
    except:
        print(f"No data for ECON-D taken within: {(currentDate - timedelta(days=1)).strftime('%Y-%m-%d_%H-%M-%S')} to {currentDate.strftime('%Y-%m-%d_%H-%M-%S')}")
for i in range(3):
    try:
        plot_pllCapbankWidth(mongo_t.pllCapbankWidthPlot(voltage=temp[0][i], econType = 'ECONT', perDay=currentDate), voltage = temp[1][i], ECON_type='ECON-T', odir=odir, perDay=currentDate)
    except:
        print(f"No data for ECON-T taken within: {(currentDate - timedelta(days=1)).strftime('%Y-%m-%d_%H-%M-%S')} to {currentDate.strftime('%Y-%m-%d_%H-%M-%S')}")
