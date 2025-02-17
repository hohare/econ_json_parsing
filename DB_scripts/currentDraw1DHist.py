import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './')
args = parser.parse_args()

odir = args.odir + '/test_power'
if not os.path.isdir(odir):
    os.makedirs(odir)

def plot_currentDraw(array_v, array_c, ECON_type, odir,tray_number = 'all'):
    fig, hist = plt.subplots(1, 2, figsize=(16,6))

    #Plotting the current of all the tested chips
    hist[0].hist(array_c, log = True, bins= np.arange(0.2,0.37,0.001),color='b',alpha=0.5,label=f"Current \u03BC:{np.mean(array_c):.3f} \u03C3:{np.std(array_c):.3f}")
    
    underflow_current = np.sum(array_c < 0.2)
    overflow_current = np.sum(array_c > 0.37)
    legend_text_current = f'Underflow: {underflow_current}, Overflow: {overflow_current}'
    if tray_number != 'all':
        odir = odir + '/perTray'
    #hist[0].axvline(x=0.24, color='black', alpha=0.5, label="Threshold = 0.24", linestyle='--')
    #hist[0].axvline(x=0.28, color='r', alpha=0.5, label="Max current = 0.28", linestyle='--')
    hist[0].grid(color='black', linestyle='--', linewidth=.05)
    hist[0].xaxis.set_minor_locator(plt.NullLocator())
    hist[0].legend([f"Current \u03BC:{np.mean(array_c):.3f} \u03C3:{np.std(array_c):.3f}",
                   #"Threshold = 0.24",
                   #"Max current = 0.28",
                   legend_text_current],loc="best", fontsize='15')

    hist[0].set_ylabel('Count')
    hist[0].set_xlabel('Current (A)')

    #Plotting the voltage of all the tested chips.
    hist[1].hist(array_v, bins= np.arange(1.15,1.30,0.01),color='b',alpha=0.5,label=f"Voltage \u03BC:{np.mean(array_v):.3f} \u03C3:{np.std(array_v):.3f}")
    
    underflow_voltage = np.sum(array_v < 1.15)
    overflow_voltage = np.sum(array_v > 1.30)
    legend_text_voltage = f'Underflow: {underflow_voltage}, Overflow: {overflow_voltage}'
    
    #hist[1].axvline(x=1.18, color='black', alpha=0.5, label="Threshold = 1.18", linestyle='--')
    #hist[1].axvline(x=1.22, color='r', alpha=0.5, label="Max voltage = 1.22", linestyle='--')
    hist[1].grid(color='black', linestyle='--', linewidth=.05)
    hist[1].xaxis.set_minor_locator(plt.NullLocator())
    hist[1].legend([f"Voltage \u03BC:{np.mean(array_v):.3f} \u03C3:{np.std(array_v):.3f}",
                   #"Threshold = 1.18",
                   #"Max voltage = 1.22",
                   legend_text_voltage], loc="best", fontsize='15')
    hist[1].set_ylabel('Count')
    hist[1].set_xlabel('Voltage (V)')
    plt.tight_layout()
    plt.savefig(f'{odir}/Power_{ECON_type}_{tray_number}.png', dpi=300, facecolor = "w")
    
    return plt

mongo_d = Database(args.dbaddress, client = 'econdDB')
mongo_t = Database(args.dbaddress, client = 'econtDB')


current, voltage, current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set = mongo_d.getVoltageAndCurrent()
plot_currentDraw(voltage, current, ECON_type = 'ECON-D', odir=odir)

current, voltage, current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set = mongo_t.getVoltageAndCurrent(econType = 'ECONT')
plot_currentDraw(voltage, current, ECON_type = 'ECON-T', odir=odir)


