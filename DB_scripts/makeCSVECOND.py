import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
import pandas as pd
from collections import defaultdict
import datetime

timestampStr = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './CSV')
args = parser.parse_args()

odir = args.odir + '/econdCSV'
if not os.path.isdir(odir):
    os.makedirs(odir)

def convertChipNumsToInt(chipNums):
    return [int(x) for x in chipNums]


db = Database(args.dbaddress, client = 'econdDB')
chip_results = defaultdict(lambda: defaultdict(float))
##TO DO: if there are multiple assert statements remove from the list and query the metadata from the table 
keysForPassFail = ['test_read_current_start',
 'test_pllautolock_1_08',
 'test_pll_capbank_width_1_08',
 'test_pll_lock_1_08',
 'test_pllautolock_1_32',
 'test_pll_capbank_width_1_32',
 'test_pll_lock_1_32',
 'test_pllautolock_1_2',
 'test_pll_capbank_width_1_2',
 'test_pll_lock_1_2',
 'test_currentdraw_1p2V',
 'test_fc_lock',
 'test_rw_allregisters_0',
 'test_rw_allregisters_255',
 'test_hard_reset_i2c_allregisters',
 'test_soft_reset_i2c_allregisters',
 'test_wrong_reg_address',
 'test_alladdresses_0',
 'test_alladdresses_1',
 'test_alladdresses_2',
 'test_alladdresses_3',
 'test_alladdresses_4',
 'test_alladdresses_5',
 'test_alladdresses_6',
 'test_alladdresses_7',
 'test_alladdresses_8',
 'test_alladdresses_9',
 'test_alladdresses_10',
 'test_alladdresses_11',
 'test_alladdresses_12',
 'test_alladdresses_13',
 'test_alladdresses_14',
 'test_alladdresses_15',
 'test_wrong_i2c_address',
 'test_hold_hard_reset',
 'test_hold_soft_reset',
 'test_chip_sync',
 'test_ePortRXPRBS_1_08',
 'test_eTX_delayscan_1_08',
 'test_eTx_PRBS7_1_08',
 'test_ePortRXPRBS_1_32',
 'test_eTX_delayscan_1_32',
 'test_eTx_PRBS7_1_32',
 'test_ePortRXPRBS_1_2',
 'test_eTX_delayscan_1_2',
 'test_eTx_PRBS7_1_2',
 'test_alignment_erx',
 'test_alignment_etx',
 'test_common_mode_erx_route',
 'test_errBit_roc_errin_1',
 'test_errBit_roc_errin_0',
 'test_input_aligner_shift_shift0',
 'test_reset_requests_setup',
 'test_reset_requests_watchdogs',
 'test_reset_requests_alert_limits',
 'test_reset_requests_bits',
 'test_clearing_fc',
 'test_serializer',
 'test_zs_zsm1_pass_mask',
 'test_zs_zsm1_sampling',
 'test_single_fcsequence_counter_100-None-fc_sequence0-eTx-0',
 'test_single_fcsequence_counter_100-None-fc_sequence1-eTx-01',
 'test_single_fcsequence_counter_100-None-fc_sequence2-eTx-012',
 'test_single_fcsequence_counter_100-None-fc_sequence3-eTx-0123',
 'test_single_fcsequence_counter_100-None-fc_sequence4-eTx-01234',
 'test_single_fcsequence_counter_100-None-fc_sequence5-eTx-012345',
 'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence6-ZS_c_i_1',
 'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence7-ZS_37',
 'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence8-ZS_37',
 'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence9-ZS_37',
 'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence10-pass_thru',
 'test_check_error_counts',
 'test_bist',
 'test_streamCompareLoop_0_99',
 'test_streamCompareLoop_1_03',
 'test_streamCompareLoop_1_08']


def stringReplace(word):
    if "[" in word:
        word = word.replace("[","_")
    if ".." in word:
        word = word.replace("..","_")
    if "/" in word:
        word = word.replace("/","_")
    if "]" in word:
        word = word.replace("]", "")
    if "." in word:
        word = word.replace(".","p")
    return word

print('Gathering all data')
## Get bist results
voltages, bist_results, chipNumBIST = db.getBISTInfoFull()
goodIdx = 0
for i, volt in enumerate(voltages):
    if volt != None:
        goodIdx = i
        break
## Get Pass/fail results
outcomes, chipNums, Timestamp, IP = db.getPassFailResults()
chipNums = convertChipNumsToInt(chipNums)
socket = replaced_arr = ['B' if x == '46' else 'A' for x in IP]
updatedTimestamp = [
    datetime.datetime.strptime('2024-11-01','%Y-%m-%d') if date.year==1970 else date for date in Timestamp
#    date.replace(year=2025) if date.year == 1970 else date for date in Timestamp
]

## get streamCompare results
word_err_count_0p99, word_err_count_1p03, word_err_count_1p08, word_err_count_1p20, chipNumSC = db.testStreamComparison()
chipNumSC = convertChipNumsToInt(chipNumSC)
## get current reading and temperature results
current, voltage, current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set, temperature, chipNumCurrent = db.getVoltageAndCurrentCSV()
chipNumCurrent = convertChipNumsToInt(chipNumCurrent)
## get results from teat_packets
results = db.retrieveTestPacketInfo()
chipNumsPacket = results['chipNum']
results = {key: value for key, value in results.items() if key != 'chipNum'}
chipNumsPacket = convertChipNumsToInt(chipNumsPacket)
## get results from I2C read/write errors
chipNumI2C, n_read_errors_asic, n_read_errors_emulator, n_write_errors_asic, n_write_errors_emulator= db.retrieveI2Cerrcnts()
chipNumI2C = convertChipNumsToInt(chipNumI2C)
## get pll results
chipNumPLL, capbankwidth_1p08, capbankwidth_1p2, capbankwidth_1p32, minFreq_1p08, minFreq_1p2, minFreq_1p32, maxFreq_1p08, maxFreq_1p2, maxFreq_1p32= db.testPllCSV()
chipNumPLL = convertChipNumsToInt(chipNumPLL)
## get io results
delayscan_maxwidth_1p08, delayscan_maxwidth_1p2, delayscan_maxwidth_1p32, phasescan_maxwidth_1p08, phasescan_maxwidth_1p2, phasescan_maxwidth_1p32, chipNumIO = db.testIoCSV()
chipNumIO = convertChipNumsToInt(chipNumIO)
## get first failure results
firstFailure, chipNumFF = db.getFirstFailureCSV()
chipNumFF = convertChipNumsToInt(chipNumFF)

print('writing data to csv')
## write results to a dictionary
## Add in pass/fail results and the timestamp
for i, chipNum in enumerate(chipNums):
    # Initialize 'Pass/Fail' if not already present
    if 'Pass/Fail' not in chip_results[chipNum]:
        chip_results[chipNum]['Pass/Fail'] = 'Pass'

    # Loop through keys in keysForPassFail
    for key in keysForPassFail:
        try:
            chip_results[chipNum][key] = outcomes[i][key]
            if outcomes[i][key] != 1:
                chip_results[chipNum]['Pass/Fail'] = 'Fail'
        except KeyError:
            chip_results[chipNum][key] = None
    chip_results[chipNum]['†est_bist_full'] = outcomes[i]['test_bist_full']
    chip_results[chipNum]['Timestamp'] = updatedTimestamp[i]
    chip_results[chipNum]['Socket'] = socket[i]
    chip_results[chipNum]['Tray'] = str(chipNum)[:2]
    
    ## initializing these because some chips were not run on the streamCompare test
    chip_results[chipNum]['SCTestWordCount0p99V'] = None
    chip_results[chipNum]['SCTestErrCount0p99V'] = None
    chip_results[chipNum]['SCTestWordCount1p03V'] = None
    chip_results[chipNum]['SCTestErrCount1p03V'] = None
    chip_results[chipNum]['SCTestWordCount1p08V'] = None
    chip_results[chipNum]['SCTestErrCount1p08V'] = None
    chip_results[chipNum]['SCTestWordCount1p20V'] = None
    chip_results[chipNum]['SCTestErrCount1p20V'] = None
    

## add in results from current draw plus the temperature
for i, chipNum in enumerate(chipNumCurrent):
    chip_results[chipNum]['current'] = current[i]
    chip_results[chipNum]['current_during_hardreset'] = current_during_hardreset[i]
    chip_results[chipNum]['current_after_hardreset'] = current_after_hardreset[i]
    chip_results[chipNum]['current_during_softreset'] = current_during_softreset[i]
    chip_results[chipNum]['current_after_softreset'] = current_after_softreset[i]
    chip_results[chipNum]['current_runbit_set'] = current_runbit_set[i]
    chip_results[chipNum]['temperature'] = temperature[i]
## add in results for read/write errors of I2C test
for i, chipNum in enumerate(chipNumI2C):
    chip_results[chipNum]['n_read_errors_asic'] = n_read_errors_asic[i]
    chip_results[chipNum]['n_read_errors_emulator'] = n_read_errors_emulator[i]
    chip_results[chipNum]['n_write_errors_asic'] = n_write_errors_asic[i]
    chip_results[chipNum]['n_write_errors_emulator'] = n_write_errors_emulator[i]
## add in results for test packets
for i, chipNum in enumerate(chipNumsPacket):
    for key in results.keys():
        chip_results[chipNum][key] = results[key][i]
## add in results for SC test
for i, chipNum in enumerate(chipNumSC):
    ## These if/else statements are necessary because if there was a read error the query will return None since metadata does not exist
    ## but the standard data format looks like [timestamp, word count, error count] which will throw an error if the query returns None
    if word_err_count_0p99[i] == None:
        chip_results[chipNum]['SCTestWordCount0p99V'] = None
        chip_results[chipNum]['SCTestErrCount0p99V'] = None
    else:
        chip_results[chipNum]['SCTestWordCount0p99V'] = word_err_count_0p99[i][-1][1]
        chip_results[chipNum]['SCTestErrCount0p99V'] = word_err_count_0p99[i][-1][-1]
    if word_err_count_1p03[i] == None:
        chip_results[chipNum]['SCTestWordCount1p03V'] = None
        chip_results[chipNum]['SCTestErrCount1p03V'] = None
    else:
        chip_results[chipNum]['SCTestWordCount1p03V'] = word_err_count_1p03[i][-1][1]
        chip_results[chipNum]['SCTestErrCount1p03V'] = word_err_count_1p03[i][-1][-1]
    if word_err_count_1p08[i] == None:
        chip_results[chipNum]['SCTestWordCount1p08V'] = None
        chip_results[chipNum]['SCTestErrCount1p08V'] = None
    else:
        chip_results[chipNum]['SCTestWordCount1p08V'] = word_err_count_1p08[i][-1][1]
        chip_results[chipNum]['SCTestErrCount1p08V'] = word_err_count_1p08[i][-1][-1]
    if word_err_count_1p20[i] == None:
        chip_results[chipNum]['SCTestWordCount1p20V'] = None
        chip_results[chipNum]['SCTestErrCount1p20V'] = None
    else:
        chip_results[chipNum]['SCTestWordCount1p20V'] = word_err_count_1p20[i][-1][1]
        chip_results[chipNum]['SCTestErrCount1p20V'] = word_err_count_1p20[i][-1][-1]
        
## add bist results
for i, chipNum in enumerate(chipNumBIST):
    for j, volt in enumerate(voltages[goodIdx]):
        ## The if/else statement logic is the same as above 
        if bist_results[i] == None:
             chip_results[chipNum][f'OBTest_1_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'OBTest_2_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'OBTest_3_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'OBTest_4_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'PPTest_1_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'PPTest_2_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'PPTest_3_Result_{stringReplace(str(volt))}V'] = None
             chip_results[chipNum][f'PPTest_4_Result_{stringReplace(str(volt))}V'] = None
        else:
            chip_results[chipNum][f'OBTest_1_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][0]
            chip_results[chipNum][f'OBTest_2_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][1]
            chip_results[chipNum][f'OBTest_3_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][2]
            chip_results[chipNum][f'OBTest_4_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][3]
            chip_results[chipNum][f'PPTest_1_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][4]
            chip_results[chipNum][f'PPTest_2_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][5]
            chip_results[chipNum][f'PPTest_3_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][6]
            chip_results[chipNum][f'PPTest_4_Result_{stringReplace(str(volt))}V'] = bist_results[i][j][7]



## Adding in Test_IO info
for i, chipNum in enumerate(chipNumIO):
    for etx in range(6):
        if delayscan_maxwidth_1p08[i] == None: 
            chip_results[chipNum][f'delayscan_madwidth_1p08_etx_{etx}'] = None
        else:
            chip_results[chipNum][f'delayscan_madwidth_1p08_etx_{etx}'] = delayscan_maxwidth_1p08[i][etx]
            
        if delayscan_maxwidth_1p2[i] == None: 
            chip_results[chipNum][f'delayscan_madwidth_1p2_etx_{etx}'] = None
        else:
            chip_results[chipNum][f'delayscan_madwidth_1p2_etx_{etx}'] = delayscan_maxwidth_1p2[i][etx]

        if delayscan_maxwidth_1p32[i] == None: 
            chip_results[chipNum][f'delayscan_madwidth_1p32_etx_{etx}'] = None
        else:
            chip_results[chipNum][f'delayscan_madwidth_1p32_etx_{etx}'] = delayscan_maxwidth_1p32[i][etx]
    for erx in range(12):
        if phasescan_maxwidth_1p08[i] == None: 
            chip_results[chipNum][f'phasescan_madwidth_1p08_etx_{erx}'] = None
        else:
            chip_results[chipNum][f'phasescan_madwidth_1p08_etx_{erx}'] = phasescan_maxwidth_1p08[i][erx]
            
        if phasescan_maxwidth_1p2[i] == None: 
            chip_results[chipNum][f'phasescan_madwidth_1p2_etx_{erx}'] = None
        else:
            chip_results[chipNum][f'phasescan_madwidth_1p2_etx_{erx}'] = phasescan_maxwidth_1p2[i][erx]

        if phasescan_maxwidth_1p32[i] == None: 
            chip_results[chipNum][f'phasescan_madwidth_1p32_erx_{etx}'] = None
        else:
            chip_results[chipNum][f'phasescan_madwidth_1p32_erx_{etx}'] = phasescan_maxwidth_1p32[i][erx]

## Adding in Test_PLL info
for i, chipNum in enumerate(chipNumPLL):
    chip_results[chipNum]['capbankwidth_1p08'] = capbankwidth_1p08[i]
    chip_results[chipNum]['capbankwidth_1p2'] = capbankwidth_1p2[i]
    chip_results[chipNum]['capbankwidth_1p32'] = capbankwidth_1p32[i]
    chip_results[chipNum]['minFreq_1p08'] = minFreq_1p08[i]
    chip_results[chipNum]['minFreq_1p2'] = minFreq_1p2[i]
    chip_results[chipNum]['minFreq_1p32'] = minFreq_1p32[i]
    chip_results[chipNum]['maxFreq_1p08'] = minFreq_1p08[i]
    chip_results[chipNum]['maxFreq_1p2'] = minFreq_1p2[i]
    chip_results[chipNum]['maxFreq_1p32'] = minFreq_1p32[i]

## Adding in BIST first failure
for i, chipNum in enumerate(chipNumFF):
    chip_results[chipNum]['first_failure'] = firstFailure[i]

# Now, convert the defaultdict into a pandas DataFrame
# The outer dictionary (chip names) becomes the columns, and the inner dictionary keys (test names) become rows
df = pd.DataFrame.from_dict(chip_results, orient='index')

# Save the DataFrame to a CSV file
df.to_csv(f'{odir}/econd_chip_test_results_{timestampStr}.csv')

print('Done!')
