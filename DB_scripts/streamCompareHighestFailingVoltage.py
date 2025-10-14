import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
args = parser.parse_args()
odir = args.odir + '/streamCompare'
if not os.path.isdir(odir):
    os.makedirs(odir)

mongo_d = Database(args.dbaddress,client='econdDB')


#the tempXXXX contains the info 'date', word count, error count so I am putting them into a temporary variable
#to retrieve only the error count
temp0p99 = mongo_d.testOBErrorInfo(econType = 'ECOND', voltage = '0p99')
temp1p03 = mongo_d.testOBErrorInfo(econType = 'ECOND', voltage = '1p03')
temp1p08 = mongo_d.testOBErrorInfo(econType = 'ECOND', voltage = '1p08')

err_cnt_0p99 = []
err_cnt_1p03 = []
err_cnt_1p08 = []

#This loop will grab the total number of streamcomparison errors for a given run/voltage
for i in range(len(temp0p99)):
    err_cnt_0p99.append(temp0p99[i][-1][-1])
    err_cnt_1p03.append(temp1p03[i][-1][-1])
    err_cnt_1p08.append(temp1p08[i][-1][-1])

err_cnt_0p99 = np.array(err_cnt_0p99)
err_cnt_1p03 = np.array(err_cnt_1p03)
err_cnt_1p08 = np.array(err_cnt_1p08)

# Create boolean arrays for fail conditions (error count > 0 is considered "fail")
fail_array_0p99 = err_cnt_0p99 > 0
fail_array_1p03 = err_cnt_1p03 > 0
fail_array_1p08 = err_cnt_1p08 > 0

# Create masks based on different conditions
highest1p08 = fail_array_0p99 & fail_array_1p03 & fail_array_1p08
highest1p03 = fail_array_0p99 & fail_array_1p03 & ~fail_array_1p08
highest0p99 = fail_array_0p99 & ~fail_array_1p03 & ~fail_array_1p08
highestpass = ~fail_array_0p99 & ~fail_array_1p03 & ~fail_array_1p08

# Calculate the number of items matching each condition
passAll = np.sum(highestpass)
fail0p99 = np.sum(highest0p99)
fail1p03 = np.sum(highest1p03)
fail1p08 = np.sum(highest1p08)

# Store the results in a list and print them
values = [passAll, fail0p99, fail1p03, fail1p08]

##making the bar chart
categories = ['pass all', '0.99 V', '1.03V', '1.08V']
# Create the bar chart
bars = plt.bar(categories, values, color='skyblue')

# Add title and labels
plt.title('Highest Failing Voltage (SC)')
plt.xlabel('Voltages')
plt.ylabel('Number of chips')

# Add labels on top of the bars
for bar in bars:
    yval = bar.get_height()  # Get the height of the bar
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5,  # Position the text
             str(yval) + ', ' + str(np.round((yval/len(err_cnt_0p99))*100,2)) +'%', ha='center', va='bottom', fontsize=10)  # Add the text label

# Show the chart
plt.savefig(f'{odir}/highest_failing_voltage.png',dpi=300, facecolor='w')
