from http import client
import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
from matplotlib import colors
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches


from slack_sdk import WebClient

from matplotlib.ticker import PercentFormatter
import os
import pandas as pd
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
parser.add_argument("--tray", help="tray to run on", default = 26)
parser.add_argument("--econType", help="ECOND or ECONT", default = 'ECOND')
args = parser.parse_args()

odir = args.odir + '/summary'
if not os.path.isdir(odir):
    os.makedirs(odir)

csvdir = odir + '/csv-results/'
if not os.path.isdir(csvdir):
    os.makedirs(csvdir) 


def get_word_error_rate(dict,chip):
    try:
        word_count = dict[chip][0][0]
        count = word_count[2]
        total = word_count[1]

        rate = float(count)/float(total)
    except: 
        rate = -1
    return rate


def build_dict_stream(word_count, chip_number,tray):
    ret = {}
    for i in range(len(word_count)):
        chip = str(int(chip_number[i] - int(tray) * 100))
        ls = [word_count[i]]
        ret[chip] = ls

    return ret


def send_slack(message):
    client = WebClient(token="")

    result = client.chat_postMessage(
            channel = "cms-econ-asic", 
            text = message,
            username = "Bot User")

    return result

def send_slack_image(image_path):
    client = WebClient(token="")

    with open(image_path, "rb") as file_content:
        result = client.files_upload(
        channels="cms-econ-asic",
        file=file_content,
        filename="image.png",
        title="PNG Image"
        )

def trayChipPlot(chip_numbers, results, econType, odir,csvdir,tray_number, d_0p99,d_1p03,d_1p08):
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
    stream_labels = np.full((rows, cols), '', dtype=object)

    counter_best = 0
    counter_medium = 0
    counter_low = 0 
    counter = 0


    f_csv_name = f'results_{econType}_100{tray_number}.csv'
    csv_out = 'econType,chip,fraction,0.99V,1.03V,1.08V,quality\n'

    
    # Fill the tray with results based on chip numbers
    for chip, fraction in zip(chip_numbers, results):
        quality = 'bad'

        row = ( 89 - (chip - 1)) // cols
        col = (89 - (chip - 1)) % cols

        tray[row, col] = fraction
        text_labels[row, col] = f"{fraction:.0%}"  # Convert fraction to percentage
        chip_label = f"{chip}"
        chip_labels[row,col] = chip_label

        rate_0p99 = get_word_error_rate(d_0p99,chip_label)
        rate_1p03 = get_word_error_rate(d_1p03,chip_label)
        rate_1p08 = get_word_error_rate(d_1p08,chip_label)

        if fraction > 0.9999:
            quality = 'pass'
            counter += 1
            if abs(rate_0p99) < 1e-9 : 
                counter_best +=1 
                quality = 'top'
            elif abs(rate_1p03) < 1e-9: 
                counter_medium += 1
                quality = 'high'
            elif abs(rate_1p08) < 1e-9: 
                counter_low += 1
                quality = 'medium'
        stream_labels[row, col] = f"0.99: {rate_0p99:.1e}\n1.03: {rate_1p03:.1e}\n1.08: {rate_1p08:.1e}"

        csv_out += f'{econType},{chip_label},{fraction},{rate_0p99},{rate_1p03},{rate_1p08},{quality}\n'


    print(f"Writing results in {csvdir}/{f_csv_name}")
    with open(csvdir + '/' + f_csv_name,'w') as f:
        f.write(csv_out)
    # Create the figure
    fig, ax = plt.subplots(figsize=(6, 15))  # Adjust figsize for better visualization

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
            ax.text(j, i - 0.2, text_labels[i, j], ha='center', va='center', fontsize=8, color='black')
            ax.text(j+0.1, i-0.1, chip_labels[i, j], ha='center', va='center', fontsize=4, color='black')
            ax.text(j-0.2, i+0.1, stream_labels[i, j], ha='center', va='center', fontsize=4, color='black')


    
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)


    ax.set_title(f"Tray {tray_number} {econType}: pass 0.99 V = {counter_best}, 1.03 V = {counter_medium}, 1.08 V = {counter_low} (Pass = {counter})")
    
    # Add colorbar
    #cbar = fig.colorbar(cax, ax=ax)
    #cbar.set_label("Fraction of Tests Passed")
    # Create custom legend
    legend_patches = [
    mpatches.Patch(color='white', label='No test'),
    mpatches.Patch(color='red', label='Hard fail'),
    mpatches.Patch(color='orange', label='Fail'),
    mpatches.Patch(color='green', label='Pass')
    ]
    ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1), title='Categories')

    # Save the plot
    image_path = f"{odir}/tray_{tray_number}_chip_summary_{econType}.png"
    fig.savefig(image_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return image_path
   
if args.econType == 'ECOND':
    mongo = Database(args.dbaddress, client='econdDB')
elif args.econType == 'ECONT':
    mongo = Database(args.dbaddress, client='econtDB')


tray = args.tray
econdFracPassed, econd_chip_numbers = mongo.getFractionOfTestsPassed(econType=args.econType, tray_number=tray)
econd_chip_numbers = econd_chip_numbers-int(tray)*100

word_count_0p99, chip_number_0p99  = mongo.testOBErrorInfo(econType=args.econType, voltage = '0p99', tray_number=tray)
dic_0p99 = build_dict_stream(word_count_0p99, chip_number_0p99,tray)

word_count_1p03, chip_number_1p03 = mongo.testOBErrorInfo(econType=args.econType, voltage = '1p03', tray_number=tray)
dic_1p03 = build_dict_stream(word_count_1p03, chip_number_1p03,tray)


word_count_1p08, chip_number_1p08 = mongo.testOBErrorInfo(econType=args.econType, voltage = '1p08', tray_number=tray)
dic_1p08 = build_dict_stream(word_count_1p08, chip_number_1p08,tray)


#print(econd_chip_numbers,econdFracPassed)
image_path = trayChipPlot(econd_chip_numbers,econdFracPassed,'ECOND', odir,csvdir,tray,dic_0p99,dic_1p03,dic_1p08)

#send_slack_image(image_path)

