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
currentDate= datetime.datetime.now()

#A function to plot the capbank width
def plot_histograms(data1, data2, title1='Minimum Locking Frequency', title2='Maximum Locking Frequency', ECON_Type='ECOND', odir = '',vlines1=(None, None), vlines2=(None, None), voltage = '', perDay=None):
    # Create a figure with two subplots (1 row, 2 columns)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    binsMin = np.arange(33,44,(1/8))
    binsMax = np.arange(35,46, (1/8))
    underflowMin = np.sum(data1 < 33)
    overflowMin = np.sum(data1 > 44)
    underflowMax = np.sum(data2 < 35)
    overflowMax = np.sum(data2 > 46)

    numFailedMinLow = len(data1[data1 < vlines1[0]])
    numFailedMinHigh = len(data1[data1 > vlines1[1]])
    fracFailedMinLow = np.round((numFailedMinLow/len(data1)),3)
    fracFailedMinHigh = np.round((numFailedMinHigh/len(data1)),3)

    numFailedMaxLow = len(data2[data2 < vlines2[0]])
    numFailedMaxHigh = len(data2[data2 > vlines2[1]])
    fracFailedMaxLow = np.round((numFailedMaxLow/len(data2)),3)
    fracFailedMaxHigh =	np.round((numFailedMaxHigh/len(data2)),3)
    if perDay is not None:
        formatted_dt = perDay.strftime('%Y-%m-%d_%H-%M-%S')
        odir = odir +'/perDay' +f'/{formatted_dt}'
        if not os.path.isdir(odir):
            os.makedirs(odir)
        
    # Plot first histogram on the first subplot
    axes[0].hist(data1, bins=binsMin, color='blue', alpha=0.7, label=f'N Chips: {len(data1)} \nAverage: {np.round((np.average(data1)),3)} \nSt. Dev: {np.round((np.std(data1)),3)} \nOverFlow: {overflowMin} \nUnderFlow: {underflowMin}')
    axes[0].set_title(title1)
    axes[0].axvline(x=vlines1[0], color='red', linestyle='--', label=f'Min Low: {vlines1[0]} \nFrac Failed Min Low: {fracFailedMinLow}')
    axes[0].axvline(x=vlines1[1], color='orange', linestyle='--', label=f'Min High: {vlines1[1]} \nFrac Failed Min High: {fracFailedMinHigh}')
    axes[0].set_xlabel('Frequency [Hz]')
    axes[0].set_ylabel('Counts')
    
    # Plot second histogram on the second subplot
    axes[1].hist(data2, bins=binsMax, color='green', alpha=0.7, label=f'N Chips: {len(data2)} \nAverage: {np.round((np.average(data1)),2)} \nSt. Dev: {np.round((np.std(data2)),3)} \nOverFlow: {overflowMax} \nUnderFlow: {underflowMax}')
    axes[1].set_title(title2)
    axes[1].set_xlabel('Frequency [Hz]')
    axes[1].set_ylabel('Counts')
    axes[1].axvline(x=vlines2[0], color='purple', linestyle='--', label=f'Max Low: {vlines2[0]} \nFrac Failed Max Low: {fracFailedMaxLow}')
    axes[1].axvline(x=vlines2[1], color='brown', linestyle='--', label=f'Max High: {vlines2[1]} \nFrac Failed Max High: {fracFailedMaxHigh}')
    # Add legends for the vertical lines
    axes[0].legend()
    axes[1].legend()
    # Adjust layout for better spacing
    plt.tight_layout()
    plt.savefig(f'{odir}/{ECON_Type}_{voltage}_minMaxLockingFrequency.png', dpi=300, facecolor='w')
    
mongo_d = Database(args.dbaddress,client='econdDB')
mongo_t = Database(args.dbaddress,client='econtDB')

econdMinThresholds = [35, 43.5]
econdMaxThresholds = [36.5, 45]

minFreq_1p08, minFreq_1p2, minFreq_1p32, maxFreq_1p08, maxFreq_1p2, maxFreq_1p32 = mongo_d.minMaxFrequencyPlot()
minFreq_1p08 = np.array([val for val in minFreq_1p08 if val is not None])
maxFreq_1p08 = np.array([val for val in maxFreq_1p08 if val is not None])
plot_histograms(data1=minFreq_1p08, data2=maxFreq_1p08, title1='Minimum Locking Frequency - 1.08V', title2='Maximum Locking Frequency - 1.08V', ECON_Type='ECOND', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage = '1p08')

minFreq_1p2 = np.array([val for val in minFreq_1p2 if val is not None])
maxFreq_1p2 = np.array([val for val in maxFreq_1p2 if val is not None])
plot_histograms(data1=minFreq_1p2, data2=maxFreq_1p2, title1='Minimum Locking Frequency - 1.2V', title2='Maximum Locking Frequency - 1.2V', ECON_Type='ECOND', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage = '1p2')

minFreq_1p32 = np.array([val for val in minFreq_1p32 if val is not None])
maxFreq_1p32 = np.array([val for val in maxFreq_1p32 if val is not None])
plot_histograms(data1=minFreq_1p32, data2=maxFreq_1p32, title1='Minimum Locking Frequency - 1.32V', title2='Maximum Locking Frequency - 1.32V', ECON_Type='ECOND', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage = '1p32')

try:
    minFreq_1p08, minFreq_1p2, minFreq_1p32, maxFreq_1p08, maxFreq_1p2, maxFreq_1p32 = mongo_d.minMaxFrequencyPlot(perDay=currentDate)
    minFreq_1p08 = np.array([val for val in minFreq_1p08 if val is not None])
    maxFreq_1p08 = np.array([val for val in maxFreq_1p08 if val is not None])
    plot_histograms(data1=minFreq_1p08, data2=maxFreq_1p08, title1='Minimum Locking Frequency - 1.08V', title2='Maximum Locking Frequency - 1.08V', ECON_Type='ECOND', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage = '1p08', perDay=currentDate)

    minFreq_1p2 = np.array([val for val in minFreq_1p2 if val is not None])
    maxFreq_1p2 = np.array([val for val in maxFreq_1p2 if val is not None])
    plot_histograms(data1=minFreq_1p2, data2=maxFreq_1p2, title1='Minimum Locking Frequency - 1.2V', title2='Maximum Locking Frequency - 1.2V', ECON_Type='ECOND', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage ='1p2', perDay=currentDate)

    minFreq_1p32 = np.array([val for val in minFreq_1p32 if val is not None])
    maxFreq_1p32 = np.array([val for val in maxFreq_1p32 if val is not None])
    plot_histograms(data1=minFreq_1p32, data2=maxFreq_1p32, title1='Minimum Locking Frequency - 1.32V', title2='Maximum Locking Frequency - 1.32V', ECON_Type='ECOND', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage = '1p32', perDay=currentDate)

except:
    print(f"No data for ECON-D taken within: {(currentDate - timedelta(days=1)).strftime('%Y-%m-%d_%H-%M-%S')} to {currentDate.strftime('%Y-%m-%d_%H-%M-%S')}")







minFreq_1p08, minFreq_1p2, minFreq_1p32, maxFreq_1p08, maxFreq_1p2, maxFreq_1p32 = mongo_t.minMaxFrequencyPlot(econType='ECONT')
minFreq_1p08 = np.array([val for val in minFreq_1p08 if val is not None])
maxFreq_1p08 = np.array([val for val in maxFreq_1p08 if val is not None])
plot_histograms(data1=minFreq_1p08, data2=maxFreq_1p08, title1='Minimum Locking Frequency - 1.08V', title2='Maximum Locking Frequency - 1.08V', ECON_Type='ECONT', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage = '1p08')

minFreq_1p2 = np.array([val for val in minFreq_1p2 if val is not None])
maxFreq_1p2 = np.array([val for val in maxFreq_1p2 if val is not None])
plot_histograms(data1=minFreq_1p2, data2=maxFreq_1p2, title1='Minimum Locking Frequency - 1.2V', title2='Maximum Locking Frequency - 1.2V', ECON_Type='ECONT', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage = '1p2')

minFreq_1p32 = np.array([val for val in minFreq_1p32 if val is not None])
maxFreq_1p32 = np.array([val for val in maxFreq_1p32 if val is not None])
plot_histograms(data1=minFreq_1p32, data2=maxFreq_1p32, title1='Minimum Locking Frequency - 1.32V', title2='Maximum Locking Frequency - 1.32V', ECON_Type='ECONT', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage = '1p32')


try:
    minFreq_1p08, minFreq_1p2, minFreq_1p32, maxFreq_1p08, maxFreq_1p2, maxFreq_1p32 = mongo_t.minMaxFrequencyPlot(econType='ECONT', perDay=currentDate)
    minFreq_1p08 = np.array([val for val in minFreq_1p08 if val is not None])
    maxFreq_1p08 = np.array([val for val in maxFreq_1p08 if val is not None])
    plot_histograms(data1=minFreq_1p08, data2=maxFreq_1p08, title1='Minimum Locking Frequency - 1.08V', title2='Maximum Locking Frequency - 1.08V', ECON_Type='ECONT', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage = '1p08', perDay=currentDate)

    minFreq_1p2 = np.array([val for val in minFreq_1p2 if val is not None])
    maxFreq_1p2 = np.array([val for val in maxFreq_1p2 if val is not None])
    plot_histograms(data1=minFreq_1p2, data2=maxFreq_1p2, title1='Minimum Locking Frequency - 1.2V', title2='Maximum Locking Frequency - 1.2V', ECON_Type='ECONT', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage = '1p2', perDay=currentDate)

    minFreq_1p32 = np.array([val for val in minFreq_1p32 if val is not None])
    maxFreq_1p32 = np.array([val for val in maxFreq_1p32 if val is not None])
    plot_histograms(data1=minFreq_1p32, data2=maxFreq_1p32, title1='Minimum Locking Frequency - 1.32V', title2='Maximum Locking Frequency - 1.32V', ECON_Type='ECONT', odir = odir, vlines1=econdMinThresholds, vlines2=econdMaxThresholds, voltage = '1p32', perDay=currentDate)

except:
    print(f"No data for ECON-T taken within: {(currentDate - timedelta(days=1)).strftime('%Y-%m-%d_%H-%M-%S')} to {currentDate.strftime('%Y-%m-%d_%H-%M-%S')}")
