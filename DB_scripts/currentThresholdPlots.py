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

odir = args.odir + '/test_power'
if not os.path.isdir(odir):
    os.makedirs(odir)



mongo_d = Database(args.dbaddress, client = 'econdDB')
mongo_t = Database(args.dbaddress, client = 'econtDB')

currentDate = datetime.datetime.now()
current, voltage,  current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set = mongo_d.getVoltageAndCurrent()


thresholds = {
    'current':[0.235,0.265],
    'current_during_hardreset':[0.270,0.290],
    'current_after_hardreset':[0.240, 0.260],
    'current_during_softreset':[0.250,0.270],
    'current_after_softreset':[0.240, 0.260],
    'current_runbit_set':[0.235, 0.255],                         
}

def plotCurrentAndThresholds(var, stringVar, thresholds,odir=odir, econType='ECON_D', perDay=None):
    lowLim = 0.2
    upLim = 0.37
    max_current = np.max(var)
    underflow_current = np.sum(var < lowLim)
    overflow_current = np.sum(var > upLim)
    values, bins = np.histogram(var, bins= np.arange(lowLim, upLim,0.001))
    lowVals = np.argwhere(bins <= thresholds[0])
    highVals = np.argwhere(bins >= thresholds[1])
    lowFails = np.sum(values[lowVals])
    highFails = np.sum(values[highVals[0][0]:])
    lowFrac = np.round((lowFails/len(var)),3)
    highFrac = np.round((highFails/len(var)),3)
    totalFail = np.sum(values[lowVals]) + np.sum(values[highVals[0][0]:])
    fracFail = np.round((totalFail/len(var)),3)
    legend_text_current = f'Underflow: {underflow_current}, Overflow: {overflow_current}'
    if perDay is not None:
        formatted_dt = perDay.strftime('%Y-%m-%d_%H-%M-%S')
        odir = odir +'/perDay' +f'/{formatted_dt}'
        if not os.path.isdir(odir):
            os.makedirs(odir)
        plt.title(f"{stringVar} - {formatted_dt} - 1.20V")
    if perDay is None:
        plt.title(f'{stringVar} - 1.20V')
    plt.axvline(thresholds[0], color='k', linewidth=2)
    plt.axvline(thresholds[1], color='k', linewidth=2)
    plt.hist(var, bins = np.arange(lowLim, upLim,0.001), label = f'N Chips: {len(var)} \nAvg: {np.round(np.average(var),3)}A \nSt.Dev: {np.round(np.std(var),3)}A \nLow Threshold: {thresholds[0]}A \nHigh Threshold: {thresholds[1]}A \nFrac Failed Low Threshold: {lowFrac} \nFrac Failed High Threshold: {highFrac}')
    plt.yscale('log')
    plt.text(bins[-5], max_current, legend_text_current )
    plt.legend()
    plt.ylim(0.1,3000)
    plt.xlim(0.01,0.7)
    plt.ylabel('Number of chips')
    plt.xlabel('Current (A)')
    plt.savefig(f'{odir}/{stringVar}_{econType}_thresholdPlot.png', dpi=300, facecolor='w')
    plt.clf()

plotCurrentAndThresholds(var=current, stringVar='Current', thresholds = thresholds['current'])
plotCurrentAndThresholds(var=current_during_hardreset, stringVar='current_during_hardreset', thresholds = thresholds['current_during_hardreset'])
plotCurrentAndThresholds(var=current_after_hardreset, stringVar='current_after_hardreset', thresholds = thresholds['current_after_hardreset'])
plotCurrentAndThresholds(var=current_during_softreset, stringVar='current_during_softreset', thresholds = thresholds['current_during_softreset'])
plotCurrentAndThresholds(var=current_after_softreset, stringVar='current_after_softreset', thresholds = thresholds['current_after_softreset'])
plotCurrentAndThresholds(var=current_runbit_set, stringVar='current_runbit_set', thresholds = thresholds['current_runbit_set'])

try:
    current, voltage,  current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set = mongo_d.getVoltageAndCurrent(perDay=currentDate)
    plotCurrentAndThresholds(var=current, stringVar='Current', thresholds = thresholds['current'])
    plotCurrentAndThresholds(var=current_during_hardreset, stringVar='current_during_hardreset', thresholds = thresholds['current_during_hardreset'], perDay=currentDate)
    plotCurrentAndThresholds(var=current_after_hardreset, stringVar='current_after_hardreset', thresholds = thresholds['current_after_hardreset'], perDay=currentDate)
    plotCurrentAndThresholds(var=current_during_softreset, stringVar='current_during_softreset', thresholds = thresholds['current_during_softreset'], perDay=currentDate)
    plotCurrentAndThresholds(var=current_after_softreset, stringVar='current_after_softreset', thresholds = thresholds['current_after_softreset'], perDay=currentDate)
    plotCurrentAndThresholds(var=current_runbit_set, stringVar='current_runbit_set', thresholds = thresholds['current_runbit_set'], perDay=currentDate)
except:
    print(f"No data for ECON-D taken within: {(currentDate - timedelta(days=1)).strftime('%Y-%m-%d_%H-%M-%S')} to {currentDate.strftime('%Y-%m-%d_%H-%M-%S')}")
    

current, voltage,  current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set = mongo_t.getVoltageAndCurrent(econType='ECONT')

thresholds = {
    'current':[0.3,0.33],
    'current_during_hardreset':[0.215,0.235],
    'current_after_hardreset':[0.20, 0.220],
    'current_during_softreset':[0.195,0.215],
    'current_after_softreset':[0.200, 0.220],
    'current_runbit_set':[0.295, 0.325],
}

plotCurrentAndThresholds(var=current, stringVar='Current', thresholds = thresholds['current'], econType='ECON_T')
plotCurrentAndThresholds(var=current_during_hardreset, stringVar='current_during_hardreset', thresholds = thresholds['current_during_hardreset'], econType='ECON_T')
plotCurrentAndThresholds(var=current_after_hardreset, stringVar='current_after_hardreset', thresholds = thresholds['current_after_hardreset'], econType='ECON_T')
plotCurrentAndThresholds(var=current_during_softreset, stringVar='current_during_softreset', thresholds = thresholds['current_during_softreset'], econType='ECON_T')
plotCurrentAndThresholds(var=current_after_softreset, stringVar='current_after_softreset', thresholds = thresholds['current_after_softreset'], econType='ECON_T')
plotCurrentAndThresholds(var=current_runbit_set, stringVar='current_runbit_set', thresholds = thresholds['current_runbit_set'], econType='ECON_T')

try:
    current, voltage,  current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set = mongo_t.getVoltageAndCurrent(econType='ECONT', perDay=currentDate)
    plotCurrentAndThresholds(var=current, stringVar='Current', thresholds = thresholds['current'], econType='ECON_T', perDay=currentDate)
    plotCurrentAndThresholds(var=current_during_hardreset, stringVar='current_during_hardreset', thresholds = thresholds['current_during_hardreset'], econType='ECON_T', perDay=currentDate)
    plotCurrentAndThresholds(var=current_after_hardreset, stringVar='current_after_hardreset', thresholds = thresholds['current_after_hardreset'], econType='ECON_T', perDay=currentDate)
    plotCurrentAndThresholds(var=current_during_softreset, stringVar='current_during_softreset', thresholds = thresholds['current_during_softreset'], econType='ECON_T', perDay=currentDate)
    plotCurrentAndThresholds(var=current_after_softreset, stringVar='current_after_softreset', thresholds = thresholds['current_after_softreset'], econType='ECON_T', perDay=currentDate)
    plotCurrentAndThresholds(var=current_runbit_set, stringVar='current_runbit_set', thresholds = thresholds['current_runbit_set'], econType='ECON_T', perDay=currentDate)
except:
    print(f"No data for ECON-T taken within: {(currentDate - timedelta(days=1)).strftime('%Y-%m-%d_%H-%M-%S')} to {currentDate.strftime('%Y-%m-%d_%H-%M-%S')}")

