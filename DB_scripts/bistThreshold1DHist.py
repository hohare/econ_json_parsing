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

odir = args.odir + '/test_bist'
if not os.path.isdir(odir):
    os.makedirs(odir)

    
def plot_bistThreshold(array,ECON_type,odir, tray_number='all', perDay=None):
    
    #To plot all the D chips that failed the bist threshold test
    counts, bins, patches = plt.hist(array, bins= np.arange(0.8,1.34,0.02),color='b',alpha=0.5,label=f"Failing Voltage \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}")
    

    underflow_bist = np.sum(array < 0.8)
    overflow_bist = np.sum(array > 1.3)
    legend_text_bist = f'Underflow: {underflow_bist}, Overflow: {overflow_bist}'


    max_failing_voltage = np.max(array)
    q25, q50, q75 = np.percentile(array, [25, 50, 75])
    failedChips = array[array >= 1.01]
    numFailed = len(failedChips)
    fracFailed = np.round((numFailed/len(array)),3)

    total_chips = len(array)

    if tray_number != 'all':
        odir = odir + '/perTray'
    if perDay is not None:
        formatted_dt = perDay.strftime('%Y-%m-%d_%H-%M-%S')
        odir = odir +'/perDay' +f'/{formatted_dt}'
        if not os.path.isdir(odir):
            os.makedirs(odir)
        plt.title(f"{ECON_type} Bist Threshold - {formatted_dt}")
    if perDay is None:
        plt.title(f"{ECON_type} Bist Threshold")
    plt.axvline(x=max_failing_voltage, color='black', alpha=0.5, label=f"Max Failing Voltage = {max_failing_voltage:.2f}", linestyle='--')
    plt.axvline(x=1.01, color = 'orange', alpha=0.5, label="Threshold 1.01V", linestyle='--')
    plt.axvline(x=q25, color='red', alpha=0.5, label=f"25% Quantile = {q25:.2f}", linestyle='--')
    plt.axvline(x=q50, color='green', alpha=0.5, label=f"50% Quantile = {q50:.2f}", linestyle='--')
    plt.axvline(x=q75, color='blue', alpha=0.5, label=f"75% Quantile = {q75:.2f}", linestyle='--')
    plt.grid(color='black', linestyle='--', linewidth=.05)
    plt.gca().xaxis.set_minor_locator(plt.NullLocator())
    plt.legend([f"N Chips: {total_chips} \nFailing Voltage \u03BC:{np.mean(array):.3f} \u03C3:{np.std(array):.3f}", 
                f"Max Failing Voltage = {max_failing_voltage:.2f}",
                f"Threshold 1.01V \nFrac Failed: {fracFailed}",
                f"25% Quantile = {q25:.2f}",
                f"50% Quantile = {q50:.2f}",
                f"75% Quantile = {q75:.2f}", 
                legend_text_bist], loc="best", fontsize='12')



    #plt.legend(loc="best",fontsize='15')
    max_count = max(counts)
    plt.ylim(0, 2.0* max_count)


    plt.ylabel('Count')
    plt.xlabel('Failing Voltage')
    #plt.text(0.9, 1.8 * max_count, f'Total Chips: {total_chips}', fontsize=8, ha='center')
    #plt.text(0.9, 1.7 * max_count, f'Frac Failed: {fracFailed}', fontsize=8, ha='center')
    plt.savefig(f'{odir}/Bist_Threshold_{ECON_type}_{tray_number}.png', dpi=300, facecolor = "w")
    plt.clf()


mongo = Database(args.dbaddress, client = 'econdDB')

tray_numbers = mongo.getTrayNumbers()

first_failure, bist_result = mongo.getBISTInfo()
plot_bistThreshold(first_failure, ECON_type='ECON-D', odir=odir)

try:
    sampleDate = datetime.datetime.now()
    first_failureDate, bist_result = mongo.getBISTInfo(perDay=sampleDate)
    plot_bistThreshold(first_failureDate, ECON_type='ECON-D', odir=odir, perDay=sampleDate)
except:
    print(f"No data for ECON-D taken within: {(sampleDate - timedelta(days=1)).strftime('%Y-%m-%d_%H-%M-%S')} to {sampleDate.strftime('%Y-%m-%d_%H-%M-%S')}")

#for tray_number in tray_numbers:
#    if tray_number in [10,11,12,13,70,71]: continue
#    try:
#        first_failure, bist_result = mongo.getBISTInfo(tray_number = tray_number)
#        plot_bistThreshold(first_failure, ECON_type='ECON-D', odir=odir, tray_number=str(tray_number))
#    except: continue

