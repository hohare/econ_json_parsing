import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
import pandas as pd
from collections import defaultdict
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './CSV')
args = parser.parse_args()

def convertChipNumsToInt(chipNums):
    return [int(x) for x in chipNums]

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
odir = args.odir + '/econtCSV'
if not os.path.isdir(odir):
    os.makedirs(odir)

db = Database(args.dbaddress, client = 'econtDB')
chip_results = defaultdict(lambda: defaultdict(float))

keysForPassFail = [
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
     'test_input_aligner_shift_shift0',
     'test_mux',
     'test_float_to_fix',
     'test_calibrations',
     'test_serializer',
     'test_algorithm_compression_emu___econt_testvectors_counterPatternInTC_RPT_',
     'test_algorithm_compression_emu___econt_testvectors_randomPatternExpInTC_TS_Thr100_',
     'test_algorithm_compression_emu___econt_testvectors_counterPatternInTC_TS_Thr47_13eTx_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx5_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx4_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx3_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx2_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx1_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type1_eTx2_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type1_eTx1_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx3_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx2_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx1_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx1_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx2_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx3_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx4_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx1_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx2_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx3_',
     'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx4_',
     'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_RPT_',
     'test_algorithm_compression_bypass___econt_testvectors_mcDataset_RPT_13eTx_',
     'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_10eTx_',
     'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_5eTx_',
     'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_1eTx_',
     'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_TS_Thr47_13eTx_',
     'test_algorithm_compression_bypass___econt_testvectors_mcDataset_AE',
     'test_fill_buffer',
     'test_check_error_counts'
]

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

## Get Pass/fail results
outcomes, chipNums, Timestamp, IP = db.getPassFailResults(econType='ECONT')
chipNums = convertChipNumsToInt(chipNums)
socket = replaced_arr = ['B' if x == '46' else 'A' for x in IP]
updatedTimestamp = [
    datetime.datetime.strptime('2024-11-01','%Y-%m-%d') if date.year==1970 else date for date in Timestamp
    # date.replace(year=2025) if date.year == 1970 else date for date in Timestamp
]

## get current reading and temperature results
current, voltage, current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set, temperature, chipNumCurrent = db.getVoltageAndCurrentCSV(econType='ECONT')
chipNumCurrent = convertChipNumsToInt(chipNumCurrent)
## get results from I2C read/write errors
chipNumI2C, n_read_errors_asic, n_read_errors_emulator, n_write_errors_asic, n_write_errors_emulator= db.retrieveI2Cerrcnts(econType='ECONT')

## get pll results
chipNumPLL, capbankwidth_1p08, capbankwidth_1p2, capbankwidth_1p32, minFreq_1p08, minFreq_1p2, minFreq_1p32, maxFreq_1p08, maxFreq_1p2, maxFreq_1p32= db.testPllCSV(econType='ECONT')
chipNumPLL = convertChipNumsToInt(chipNumPLL)
## get io results
delayscan_maxwidth_1p08, delayscan_maxwidth_1p2, delayscan_maxwidth_1p32, phasescan_maxwidth_1p08, phasescan_maxwidth_1p2, phasescan_maxwidth_1p32, chipNumIO = db.testIoCSV(econType='ECONT')
chipNumIO = convertChipNumsToInt(chipNumIO)
## Test algorithm info 
results = db.retrieveTestAlgorithmInfo()
chipNumsPacket = results['chipNum']
results = {key: value for key, value in results.items() if key != 'chipNum'}
chipNumsPacket = convertChipNumsToInt(chipNumsPacket)

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
    
    chip_results[chipNum]['Timestamp'] = updatedTimestamp[i]
    chip_results[chipNum]['Socket'] = socket[i]
    chip_results[chipNum]['Tray'] = str(chipNum)[:2]
    
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

## Adding in Test_IO info
for i, chipNum in enumerate(chipNumIO):
    for etx in range(13):
        if delayscan_maxwidth_1p08[i] == None: 
            chip_results[chipNum][f'delayscan_maxwidth_1p08_etx_{etx}'] = None
        else:
            chip_results[chipNum][f'delayscan_maxwidth_1p08_etx_{etx}'] = delayscan_maxwidth_1p08[i][etx]
            
        if delayscan_maxwidth_1p2[i] == None: 
            chip_results[chipNum][f'delayscan_maxwidth_1p2_etx_{etx}'] = None
        else:
            chip_results[chipNum][f'delayscan_maxwidth_1p2_etx_{etx}'] = delayscan_maxwidth_1p2[i][etx]

        if delayscan_maxwidth_1p32[i] == None: 
            chip_results[chipNum][f'delayscan_maxwidth_1p32_etx_{etx}'] = None
        else:
            chip_results[chipNum][f'delayscan_maxwidth_1p32_etx_{etx}'] = delayscan_maxwidth_1p32[i][etx]
    for erx in range(12):
        if phasescan_maxwidth_1p08[i] == None: 
            chip_results[chipNum][f'phasescan_maxwidth_1p08_etx_{erx}'] = None
        else:
            chip_results[chipNum][f'phasescan_maxwidth_1p08_etx_{erx}'] = phasescan_maxwidth_1p08[i][erx]
            
        if phasescan_maxwidth_1p2[i] == None: 
            chip_results[chipNum][f'phasescan_maxwidth_1p2_etx_{erx}'] = None
        else:
            chip_results[chipNum][f'phasescan_maxwidth_1p2_etx_{erx}'] = phasescan_maxwidth_1p2[i][erx]

        if phasescan_maxwidth_1p32[i] == None: 
            chip_results[chipNum][f'phasescan_maxwidth_1p32_erx_{etx}'] = None
        else:
            chip_results[chipNum][f'phasescan_maxwidth_1p32_erx_{etx}'] = phasescan_maxwidth_1p32[i][erx]

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

## adding in test_algorithm info 
for i, chipNum in enumerate(chipNumsPacket):
    for key in results.keys():
        chip_results[chipNum][key] = results[key][i]

# Now, convert the defaultdict into a pandas DataFrame
# The outer dictionary (chip names) becomes the columns, and the inner dictionary keys (test names) become rows
df = pd.DataFrame.from_dict(chip_results, orient='index')
# Save the DataFrame to a CSV file
df.to_csv(f'{odir}/econt_chip_test_results_{timestamp}.csv')

print('Done!')
