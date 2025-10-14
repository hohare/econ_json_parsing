from http import client
import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches


from matplotlib.ticker import PercentFormatter
import os
import pandas as pd
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
args = parser.parse_args()
odir = args.odir + '/summary'
if not os.path.isdir(odir):
    os.makedirs(odir)

def summaryPlot(results,econType,odir):
    hist = np.array(results)

    fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)

    axs.hist(hist, bins=10)
    axs.set_xlabel('# passed tests / total')
    axs.set_ylabel('Number of chips')
    #axs.set_xlim(0,1)
    axs.axvline(np.percentile(hist, 25), color='red', linestyle='dashed', linewidth=2, label='25th Percentile')
    axs.axvline(np.percentile(hist, 50), color='green', linestyle='dashed', linewidth=2, label='50th Percentile (Median)')
    axs.axvline(np.percentile(hist, 75), color='blue', linestyle='dashed', linewidth=2, label='75th Percentile')
    axs.legend()

    #plt.show()

    fig.savefig(f'{odir}/summary_{econType}.png')
    plt.clf()

def summaryChipPlot(chip_numbers,results,econType,odir):
    hist = np.array(results)

    fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)

    plt.scatter(chip_numbers, results)
    #axs.hist(hist, bins=10)
    axs.set_xlabel('Number of the chip')
    axs.set_ylabel('# passed tests / total')
    #axs.set_xlim(0,1)
    #axs.axvline(np.percentile(hist, 25), color='red', linestyle='dashed', linewidth=2, label='25th Percentile')
    #axs.axvline(np.percentile(hist, 50), color='green', linestyle='dashed', linewidth=2, label='50th Percentile (Median)')
    #axs.axvline(np.percentile(hist, 75), color='blue', linestyle='dashed', linewidth=2, label='75th Percentile')
    axs.legend()

    #plt.show()

    fig.savefig(f'{odir}/summary_chips_{econType}.png')
    plt.clf()


def trayChipPlot(chip_numbers, results, econType, odir,tray_number):
    """
    Generates a 2D plot representing a tray of 6x15 chips with colors indicating test pass fractions.

    Parameters:
        chip_numbers: list of chip numbers (1 to 90)
        results: list of fractions of tests passed (values between 0 and 1)
        econType: string representing the ECON chip type
        odir: output directory to save the plot
    """
    # Define tray dimensions
    rows, cols = 15, 6
    tray = np.full((rows, cols), -1,dtype=float)

    text_labels = np.full((rows, cols), '', dtype=object)
    chip_labels = np.full((rows, cols), '', dtype=object)

    
    # Fill the tray with results based on chip numbers
    for chip, fraction in zip(chip_numbers, results):
        row = ( 89 - (chip - 1)) // cols
        col = (89 - (chip - 1)) % cols

        tray[row, col] = fraction
        text_labels[row, col] = f"{fraction:.0%}"  # Convert fraction to percentage
        chip_labels[row,col] = f"{chip}"
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(6, 15))  # Adjust figsize for better visualization
    #cmap = plt.get_cmap("RdYlGn")  # Red to Green colormap
    #norm = mcolors.Normalize(vmin=0, vmax=1)  # Normalize values between 0 and 1


    #cmap_colors = [
    #    (1, 0, 0),  # Red for 0
    #    (1, 1, 0),  # Yellow for 0.99
    #    (0, 1, 0)   # Green for 1
    #]
    #cmap = mcolors.LinearSegmentedColormap.from_list("custom", cmap_colors, N=256)
    
    # Define normalization: linear scaling up to 0.99, then distinct for 1.0
    #norm = mcolors.Normalize(vmin=0, vmax=1)
    # Plot heatmap

        # Define the colormap with distinct green for 1 and a gradient from red to yellow for <1
    cmap_color = [(1, 1, 1), (1, 0, 0), (1, 0.5, 0), (0, 1, 0)]  # White, Red, Orange, Green
    thresholds = [-1, 0, 0.5, 0.99, 1.0]  # White for -1, Red for 0-0.5, Orange for 0.5-0.99, Green for 1.0

    # Create the colormap and normalization
    cmap = mcolors.LinearSegmentedColormap.from_list("custom", cmap_color, N=256)
    norm = mcolors.BoundaryNorm(thresholds, cmap.N)

    cax = ax.imshow(tray, cmap=cmap, norm=norm, aspect="auto")
    
    # Add text labels
    for i in range(rows):
        for j in range(cols):
            ax.text(j, i, text_labels[i, j], ha='center', va='center', fontsize=8, color='black')
            ax.text(j+0.1, i+ 0.1, chip_labels[i, j], ha='center', va='center', fontsize=4, color='black')

    
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)


    ax.set_title(f"Tray {tray_number} Chip Summary for ECON Type {econType}")
    
    # Add colorbar
    #cbar = fig.colorbar(cax, ax=ax)
    #cbar.set_label("Fraction of Tests Passed")
    # Create custom legend
    legend_patches = [
    mpatches.Patch(color='white', label='-1'),
    mpatches.Patch(color='red', label='0-0.5'),
    mpatches.Patch(color='orange', label='0.5-0.99'),
    mpatches.Patch(color='green', label='1.0')
    ]
    ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1), title='Categories')


    # Save the plot
    fig.savefig(f"{odir}/tray_{tray_number}_chip_summary_{econType}.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def summaryTestPlot(df, econType, odir, tray=None):
    cmap = mcolors.ListedColormap(['green','red','yellow','blue'])
    ax = df.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
    ax.set_yticklabels(df.index, fontsize=5)
    plt.tight_layout()
    ax.invert_yaxis()

    save_name = f'{odir}/summary_tests_{econType}_{tray}.png'
    if tray:
        save_name = f'{odir}/summary_tests_{econType}_{tray}.png'


    plt.savefig(save_name)
    plt.savefig(save_name.replace('.png','.pdf'))


    plt.clf()

    df_non_zero_failed = df[df['failed'] != 0]
    ax = df_non_zero_failed.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
    ax.set_yticklabels(df_non_zero_failed.index, fontsize=5)
    plt.tight_layout()
    ax.invert_yaxis()

    save_name = f'{odir}/summary_tests_failed_{econType}.png'
    if tray:
        save_name = f'{odir}/summary_tests_failed_{econType}_{tray}.png'
    plt.savefig(save_name)
    plt.savefig(save_name.replace('.png','.pdf'))


    plt.clf()

    df_non_zero_passed = df[df['passed'] != 0]
    ax = df_non_zero_passed.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
    ax.set_yticklabels(df_non_zero_passed.index, fontsize=5)
    plt.tight_layout()
    ax.invert_yaxis()

    save_name = f'{odir}/summary_tests_passed_{econType}.png'
    if tray:
        save_name = f'{odir}/summary_tests_passed_{econType}_{tray}.png'
    plt.savefig(save_name)
    plt.savefig(save_name.replace('.png','.pdf'))
    plt.clf()

    df_non_zero_other= df[df['error'] != 0]
    ax = df_non_zero_other.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
    ax.set_yticklabels(df_non_zero_other.index, fontsize=5)
    plt.tight_layout()
    ax.invert_yaxis()


    save_name = f'{odir}/summary_tests_error_{econType}.png'
    if tray:
        save_name = f'{odir}/summary_tests_error_{econType}_{tray}.png'
    plt.savefig(save_name)
    plt.savefig(save_name.replace('.png','.pdf'))
    plt.clf()
    
mongo_d = Database(args.dbaddress, client='econdDB')
mongo_t = Database(args.dbaddress, client='econtDB')

econtFracPassed,econt_chip_numbers = mongo_t.getFractionOfTestsPassed('ECONT')
econdFracPassed, econd_chip_numbers = mongo_d.getFractionOfTestsPassed()


try:
    summaryPlot(econdFracPassed, econType='ECOND', odir=odir)
    summaryChipPlot(econd_chip_numbers,econdFracPassed, econType = 'ECOND', odir = odir)
except:
    print("Issue running ECOND")

try:
    summaryPlot(econtFracPassed, econType='ECONT', odir=odir)
    summaryChipPlot(econt_chip_numbers,econtFracPassed, econType = 'ECONT', odir = odir)


except:
    print("Issue running ECONT")


tray = 26
econdFracPassed, econd_chip_numbers = mongo_d.getFractionOfTestsPassed(tray_number=tray)
econd_chip_numbers = econd_chip_numbers-int(tray)*100
print(econd_chip_numbers,econdFracPassed)
trayChipPlot(econd_chip_numbers,econdFracPassed, econType = 'ECOND', odir = odir, tray_number=tray)


try:
    econdDF = mongo_d.getTestingSummaries()
    summaryTestPlot(econdDF, 'ECOND', odir=odir)
    tray_numbers = mongo_d.getTrayNumbers()

    for tray in tray_numbers:
        econdFracPassed, econd_chip_numbers = mongo_d.getFractionOfTestsPassed(tray_number=tray)
        try:

            if tray in [10,11,70,71] : continue
            econdDF = mongo_d.getTestingSummaries(tray_number=tray)

            print(tray)
            #print(econdDF)
            summaryTestPlot(econdDF, 'ECOND', odir=odir, tray=tray)
            econdFracPassed, econd_chip_numbers = mongo_d.getFractionOfTestsPassed(tray_number=tray)
            econd_chip_numbers = econd_chip_numbers-int(tray)*100
            trayChipPlot(econd_chip_numbers,econdFracPassed, econType = 'ECOND', odir = odir, tray_number=tray)

        except: 
            print("Issue in tray", tray)
            continue
        
except:
    print("Issue running summary for ECOND")
#try:
econtTF = mongo_t.getTestingSummaries('ECONT')
summaryTestPlot(econtTF, 'ECONT', odir=odir)
tray_numbers = mongo_t.getTrayNumbers()
print(tray_numbers)



for tray in tray_numbers:
    econdTF = mongo_t.getTestingSummaries(econType='ECONT',tray_number=tray)

    econtFracPassed,econt_chip_numbers = mongo_t.getFractionOfTestsPassed('ECONT', tray_number=tray)
    econt_chip_numbers = econt_chip_numbers-int(tray)*100
    trayChipPlot(econt_chip_numbers,econtFracPassed, econType = 'ECONT', odir = odir,tray_number = tray)

    print(tray)
    #print(econdTF)
    summaryTestPlot(econdTF, 'ECONT', odir=odir, tray=tray)
#except:
#    print("Issue running summary for ECONT")


# Best ECONT chips 

combined_econt_list = list(zip(econt_chip_numbers, econtFracPassed))

# Combine the lists into a list of tuples
combined_econd_list = list(zip(econd_chip_numbers, econdFracPassed))

# Sort the combined list based on the chip number (first element of the tuple)
sorted_econt_combined_list = sorted(combined_econt_list, key=lambda x: x[0])
sorted_econd_combined_list = sorted(combined_econd_list, key=lambda x: x[0])

# Unzip the sorted list back into two lists
sorted_chip_numbers_econd, sorted_frac_passed_econd = zip(*sorted_econd_combined_list)
sorted_chip_numbers_econt, sorted_frac_passed_econt = zip(*sorted_econt_combined_list)



# Now you can use sorted_chip_numbers and sorted_frac_passed in your code
#econt_f_out = 'econt_minnesota.csv'
#econt_out = 'chip_number,pass_test_rate\n'
#for i in range(len(sorted_frac_passed_econt)):
#    if sorted_frac_passed_econt[i] > 0.975:
#        #print(sorted_frac_passed_econt[i], sorted_chip_numbers_econt[i])
#        econt_out += f'{sorted_chip_numbers_econt[i]},{sorted_frac_passed_econt[i]}\n'

#with open(econt_f_out, 'w') as f:
#    f.write(econt_out)

# Best ECOND ls chips
#econd_f_out = 'econd_minnesota.csv'
#econd_out = 'chip_number,pass_test_rate\n'
#for i in range(len(sorted_frac_passed_econd)):
#    if sorted_frac_passed_econd[i] > 0.972:
#        #print(sorted_frac_passed_econd[i], sorted_chip_numbers_econd[i])
#        econd_out += f'{sorted_chip_numbers_econd[i]},{sorted_frac_passed_econd[i]}\n'

#with open(econd_f_out, 'w') as f:
#    f.write(econd_out)


