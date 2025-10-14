import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
args = parser.parse_args()

odir = args.odir + '/duration'
if not os.path.isdir(odir):
    os.makedirs(odir)

    
def plot_duration(array,ECON_type,odir,fname):
    
    # Create a histogram plot
    plt.figure(figsize=(10, 6))
    plt.hist(array, bins=10, edgecolor='black')
    plt.xlabel('Duration [s]')
    plt.ylabel('Number of Chips')
    plt.title(f'Results for tray {fname}00')
    plt.grid(True)
    plt.savefig(f"{odir}/duration_{ECON_type}_{fname}.png")


mongo = Database(args.dbaddress, client = 'econdDB')

durations = mongo.getDuration()
plot_duration(durations, ECON_type='ECOND',odir = odir, fname = 'all')

trays = mongo.getTrayNumbers()

for tray in trays:
    durations = mongo.getDuration(tray_number = tray)
    plot_duration(durations, ECON_type='ECOND',odir = odir, fname = tray)

#plot_bistThreshold(first_failure, ECON_type='ECON-D', odir=odir)


