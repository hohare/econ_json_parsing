import pymongo
import numpy as np
import pandas as pd
from datetime import timedelta

def constructQueryPipeline(query_map, econType='ECOND', lowerLim = None, upperLim=None, chipNum=None, perDay=None):
    match_stage = {
        "$match": {
            "ECON_type": econType
        }
    }
    if lowerLim is not None and upperLim is not None:
        match_stage["$match"]["chip_number"] = {"$lt": upperLim, "$gt": lowerLim}
    if chipNum is not None:
         match_stage["$match"]["chip_number"] = chipNum
    if perDay is not None:
        match_stage["$match"]["Timestamp"] = {"$lt": perDay, "$gt":perDay - timedelta(days=1)}
    pipeline = [
            match_stage,
            {
                "$project": {
                    "chip_number": 1,
                    "Timestamp": 1,
                    "data": {field: f"${query_map[field]}" for field in query_map}
                }
            },
            {
                "$match": {
                    "data": {"$ne": None}  # Filter out documents with None width
                }
            },
            {
                "$sort": {
                    "Timestamp": -1  # Sort by Timestamp in descending order
                }
            },
            {
                "$group": {
                    "_id": "$chip_number",  # Group by chip_number
                    "latest_data": {"$first": "$data"},  # Get the latest width
                    "latest_timestamp": {"$first": "$Timestamp"}  # Get the latest timestamp
                }
            }
        ]
    return pipeline

class Database:
    def __init__(self, ip, client):
        ## this connects to the database
        self.client = pymongo.MongoClient('localhost',ip)
        self.session = self.client.start_session()
        self.db = self.client[client] ## this name will probably change when we decide on an official name

    def pllCapbankWidthPlot(self, lowerLim=None, upperLim=None, perDay=None, voltage = '1p2', econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT
        voltage_field_map = {
        '1p08': {'capbankwidth':'test_info.test_pll_capbank_width_1_08.metadata.pll_capbank_width'},
        '1p2': {'capbankwidth':'test_info.test_pll_capbank_width_1_2.metadata.pll_capbank_width'},
        '1p32': {'capbankwidth':'test_info.test_pll_capbank_width_1_32.metadata.pll_capbank_width'},
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim, perDay=perDay)
        cursor = self.db['testPLLInfo'].aggregate(pipeline)
        capbankwidth = np.array([doc['latest_data']['capbankwidth'] for doc in cursor if doc.get('latest_data') is not None and 'capbankwidth' in doc['latest_data'].keys()])
        return capbankwidth


    def prbsMaxWidthPlot(self, lowerLim=None, upperLim=None, perDay=None, voltage = '1p2', econType = 'ECOND'):
        #This function makes a plot of the PRBS Max Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT
        voltage_field_map = {
        '1p08': {'maxwidth':'test_info.test_ePortRXPRBS_1_08.metadata.maxwidth'},
        '1p2': {'maxwidth':'test_info.test_ePortRXPRBS_1_2.metadata.maxwidth'},
        '1p32': {'maxwidth':'test_info.test_ePortRXPRBS_1_32.metadata.maxwidth'}
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim, perDay=perDay)
        cursor = self.db['testIOInfo'].aggregate(pipeline)
        maxwidth = np.array([doc['latest_data']['maxwidth'] for doc in cursor if doc.get('latest_data') is not None and 'maxwidth' in doc['latest_data'].keys()])
        return maxwidth


    def etxMaxWidthPlot(self, lowerLim=None, upperLim=None, perDay=None, voltage = '1p2', econType = 'ECOND'):
        #This function makes a plot of the eTX Delay scan Max Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT
        voltage_field_map = {
        '1p08': {'maxwidth':'test_info.test_eTX_delayscan_1_08.metadata.max_width'},
        '1p2': {'maxwidth':'test_info.test_eTX_delayscan_1_2.metadata.max_width'},
        '1p32': {'maxwidth':'test_info.test_eTX_delayscan_1_32.metadata.max_width'}
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim, perDay=perDay)
        cursor = self.db['testIOInfo'].aggregate(pipeline)
        maxwidth = np.array([doc['latest_data']['maxwidth'] for doc in cursor if doc.get('latest_data') is not None and 'maxwidth' in doc['latest_data'].keys()])
        return maxwidth


    def getVoltageAndCurrent(self, lowerLim=None, upperLim=None, perDay=None, econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT

        #note this test does not run at different voltages but I wanted to just have something there so the format of all the functions are uniform
        voltage_field_map = {
            'None': {
                    'current':'test_info.test_currentdraw_1p2V.metadata.current',
                    'voltage':'test_info.test_currentdraw_1p2V.metadata.voltage',
                    'current_during_hardreset':'test_info.test_currentdraw_1p2V.metadata.current_during_hardreset',
                    'current_after_hardreset':'test_info.test_currentdraw_1p2V.metadata.current_after_hardreset',
                    'current_during_softreset':'test_info.test_currentdraw_1p2V.metadata.current_during_softreset',
                    'current_after_softreset':'test_info.test_currentdraw_1p2V.metadata.current_after_softreset',
                    'current_runbit_set':'test_info.test_currentdraw_1p2V.metadata.current_runbit_set',
                    },
        }

        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim, perDay=perDay)
        cursor = self.db['testPowerInfo'].aggregate(pipeline)
        documents = list(cursor)
        #main measurements
        current = np.array([
            doc['latest_data']['current'] for doc in documents
            if doc.get('latest_data') is not None and 'current' in doc['latest_data'].keys()
        ])

        voltage = np.array([
            doc['latest_data']['voltage'] for doc in documents
            if doc.get('latest_data') is not None and 'voltage' in doc['latest_data'].keys()
        ])

        current_during_hardreset = np.array([
                doc['latest_data']['current_during_hardreset'] for doc in documents
                if doc.get('latest_data') is not None and 'current_during_hardreset' in doc['latest_data'].keys()
            ])
        current_after_hardreset = np.array([
            doc['latest_data']['current_after_hardreset'] for doc in documents
            if doc.get('latest_data') is not None and 'current_after_hardreset' in doc['latest_data'].keys()
        ])
        current_during_softreset = np.array([
            doc['latest_data']['current_during_softreset'] for doc in documents
            if doc.get('latest_data') is not None and 'current_during_softreset' in doc['latest_data'].keys()
        ])
        current_after_softreset = np.array([
            doc['latest_data']['current_after_softreset'] for doc in documents
            if doc.get('latest_data') is not None and 'current_after_softreset' in doc['latest_data'].keys()
        ])
        current_runbit_set = np.array([
            doc['latest_data']['current_runbit_set'] for doc in documents
            if doc.get('latest_data') is not None and 'current_runbit_set' in doc['latest_data'].keys()
        ])
        return current, voltage, current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set

    def getBISTInfo(self, lowerLim=None, upperLim=None, perDay=None, econType='ECOND',tray_number = None):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT

        voltage_field_map = {
            'None': {
                    'first_failure':'test_info.test_bist.metadata.first_failure',
                    'bist_result':'test_info.test_bist.metadata.bist_results',
                    },
        }

        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim, perDay=perDay)
        cursor = self.db['testBistInfo'].aggregate(pipeline)
        documents = list(cursor)

        if tray_number is not None:
            documents = self.filter_by_tray(documents, tray_number)

        first_failure = np.array([
            doc['latest_data']['first_failure'] for doc in documents
            if doc.get('latest_data') is not None and 'first_failure' in doc['latest_data'].keys()
        ])

        bist_result = [
            doc['latest_data']['bist_result'] for doc in documents
            if doc.get('latest_data') is not None and 'bist_result' in doc['latest_data'].keys()
        ]
        return first_failure, bist_result

    def phaseScan2DPlot(self, chipNum, econType = 'ECOND', voltage = '1p2'):
        #returns the information needed to make the phase scan 2d plot
        #for a given chip number
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT

        voltage_field_map = {
        '1p08': {'eRX_errcounts':'test_info.test_ePortRXPRBS_1_08.metadata.eRX_errcounts'},
        '1p2': {'eRX_errcounts':'test_info.test_ePortRXPRBS_1_2.metadata.eRX_errcounts'},
        '1p32': {'eRX_errcounts':'test_info.test_ePortRXPRBS_1_32.metadata.eRX_errcounts'}
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, chipNum=chipNum)
        cursor = self.db['testIOInfo'].aggregate(pipeline)
        eRX_errcounts = np.array([doc['latest_data']['eRX_errcounts'] for doc in cursor if doc.get('latest_data') is not None and 'eRX_errcounts' in doc['latest_data'].keys()])
        return eRX_errcounts


    def delayScan2DPlot(self, chipNum, econType = 'ECOND', voltage = '1p2'):
        #returns the information needed to make the delay scan 2d plot
        #for a given chip number
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT
        voltage_field_map = {
        '1p08': {
                'eTX_bitcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_bitcounts',
                'eTX_errcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_errcounts',
                },
        '1p2': {
                'eTX_bitcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_bitcounts',
                'eTX_errcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_errcounts',
                },
        '1p32': {
               'eTX_bitcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_bitcounts',
                'eTX_errcounts':'test_info.test_eTX_delayscan_1_08.metadata.eTX_errcounts',
                }
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, chipNum=chipNum)
        cursor = self.db['testIOInfo'].aggregate(pipeline)
        documents = list(cursor)
        #print(documents)
        eTX_bitcounts = np.array([
            doc['latest_data']['eTX_bitcounts'] for doc in documents
            if doc.get('latest_data') is not None and 'eTX_bitcounts' in doc['latest_data'].keys()
        ])

        eTX_errcounts = [
            doc['latest_data']['eTX_errcounts'] for doc in documents
            if doc.get('latest_data') is not None and 'eTX_errcounts' in doc['latest_data'].keys()
        ]
        return eTX_bitcounts, eTX_errcounts


    def getFractionOfTestsPassed(self, econType = 'ECOND', perDay=None, tray_number = None):
        #This function grabs the fraction of tests that passed
        #So what this does is first count the number of tests that got skipped
        #And subtracts this from the total number of tests that were collected
        #This should give the total number of tests performed for either ECOND or ECONT
        #Then it just returns the total fraction of tests that pass for a given chip by
        #Dividing the total number of tests passed over the total number of tests performed
        #please use the econType argument to specify ECOND or ECONT and it expects a string input
        voltage_field_map = {
            'None': {
                    'outcome':'individual_test_outcomes',
                    'passed':'summary.passed',
                    'total': 'summary.total'
                    },
        }
        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, perDay=perDay)
        cursor = self.db['TestSummary'].aggregate(pipeline)
        x = list(cursor)

        if tray_number is not None:
            x = self.filter_by_tray(x, tray_number)
        frac_passed = []
        # Extract outcomes, passed, and total
        outcomes = np.array([doc['latest_data']['outcome'] for doc in x])
        passed = np.array([doc['latest_data']['passed'] for doc in x])
        total = np.array([doc['latest_data']['total'] for doc in x])
        chip_numbers = np.array([doc['_id']for doc in x])

        # Iterate over each outcome to compute fractions
        for i in range(len(outcomes)):
            tot_econt = np.array([key for key in outcomes[i] if outcomes[i][key] == -2])
            denominator = total[i] - len(tot_econt)

            # Handle division by zero
            if denominator > 0:
                frac = passed[i] / denominator
            else:
                frac = 0  # or np.nan, depending on how you want to handle it

            frac_passed.append(frac)

        # Convert to NumPy array
        return np.array(frac_passed), chip_numbers

    def getTestingSummaries(self, econType = 'ECOND', perDay=None, tray_number = None):
        #This function returns a dataframe for the testing summary plots prepared by Marko
        #Please use the econType argument to specify ECOND or ECONT and the function expects a string for this argument
        voltage_field_map = {
            'None': {
                    'individual_test_outcomes':'individual_test_outcomes',
                    },
        }
        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, perDay=perDay)
        cursor = self.db['TestSummary'].aggregate(pipeline)
        outcomes = list(cursor)

        #for el in outcomes:
        #    print(el.keys())

        if tray_number is not None:
            outcomes = self.filter_by_tray(outcomes, tray_number)

        # Prepare a counter array for 'passed', 'failed', 'error', 'skipped'
        maps = ['passed', 'failed','error','skipped']
        counters = {}
        total = 0
        for obj in outcomes:
            for key, value in obj['latest_data']['individual_test_outcomes'].items():
                if value == 1:
                    if key in counters.keys():
                        counters[key][0]+=1
                    else:
                        counters[key] = [1,0,0,0]
                elif value == 0:
                    if key in counters.keys():
                        counters[key][1]+=1
                    else:
                        counters[key] = [0,1,0,0]
                elif value == -1:
                    if key in counters.keys():
                        counters[key][2] += 1
                    else:
                        counters[key] = [0,0,1,0]
                elif value == -2:
                    if key in counters.keys():
                        counters[key][3] += 1
                    else:
                        counters[key] = [0,0,0,1]

            total += 1
        df = pd.DataFrame(counters, index=maps)
        df = df.T
        df = df/total
        return df
    def getDuration(self, econType='ECOND', perDay=None, tray_number = None):
        durations = self.db['NonTestingInfo'].find({},{'created':'$created', 'duration':'$duration', 'chip_number':'$chip_number', '_id':0})

        if tray_number is not None:
            durations = self.filter_by_tray(durations, tray_number)
        return np.array([chip['duration'] for chip in list(durations)])

    def filter_by_tray(self, documents, tray_number, perDay=None):
    # Filter documents by tray number
        filtered_docs = []
        label = 'chip_number'
        try:
            if 'chip_number' not in documents[0].keys():
                label = '_id'
        except: label = '_id'
        #print(documents)
        for doc in documents:
            chip_number = doc.get(label)
            if chip_number and str(chip_number).startswith(str(tray_number)):
                filtered_docs.append(doc)
            #print(chip_number)
        return filtered_docs

    def getTrayNumbers(self, econType='ECOND', perDay=None):
        field_map = {'chip_number': '$chip_number', '_id':0}
        trays = self.db['NonTestingInfo'].find({},field_map)

        trays = [str(chip['chip_number'])[:2] for chip in trays]
        return sorted(list(set(trays)))

    def testOBErrorInfo(self, econType = 'ECOND', voltage = '0p99', perDay=None, tray_number = None):
        #Returns info from the OB error test
        #This returns DAQ_asic, DAQ_emu, DAQ_counter, and word_err_cnt
        #This is done for the voltages 0.99, 1.03, and 1.08
        #specify which voltage you want when calling the function
        # 0p99 for 0.99, 1p03 for 1.03, and 1p08 for 1.08V

        voltage_field_map = {
        '0p99': {
                #'DAQ_asic':'test_info.test_streamCompareLoop_0_99.metadata.DAQ_asic',
                #'DAQ_emu':'test_info.test_streamCompareLoop_0_99.metadata.DAQ_emu',
                #'DAQ_counter':'test_info.test_streamCompareLoop_0_99.metadata.DAQ_counter',
                'word_err_count':'test_info.test_streamCompareLoop_0_99.metadata.word_err_count',
                },
        '1p03': {
                #'DAQ_asic':'test_info.test_streamCompareLoop_1_03.metadata.DAQ_asic',
                #'DAQ_emu':'test_info.test_streamCompareLoop_1_03.metadata.DAQ_emu',
                #'DAQ_counter':'test_info.test_streamCompareLoop_1_03.metadata.DAQ_counter',
                'word_err_count':'test_info.test_streamCompareLoop_1_03.metadata.word_err_count',
                },
        '1p08': {
                #'DAQ_asic':'test_info.test_streamCompareLoop_1_08.metadata.DAQ_asic',
                #'DAQ_emu':'test_info.test_streamCompareLoop_1_08.metadata.DAQ_emu',
                #'DAQ_counter':'test_info.test_streamCompareLoop_1_08.metadata.DAQ_counter',
                'word_err_count':'test_info.test_streamCompareLoop_1_08.metadata.word_err_count',
                },
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, perDay=perDay)
        cursor = self.db['testOBError'].aggregate(pipeline)
        documents = list(cursor)

        if tray_number is not None:
            documents = self.filter_by_tray(documents, tray_number)


        #DAQ_asic = ([
        #    doc['latest_data']['DAQ_asic'] for doc in documents
        #    if doc.get('latest_data') is not None and 'DAQ_asic' in doc['latest_data'].keys()
        #])

        #DAQ_emu = ([
        #    doc['latest_data']['DAQ_emu'] for doc in documents
        #    if doc.get('latest_data') is not None and 'DAQ_emu' in doc['latest_data'].keys()
        #])
        #DAQ_counter = ([
        #    doc['latest_data']['DAQ_counter'] for doc in documents
        #    if doc.get('latest_data') is not None and 'DAQ_counter' in doc['latest_data'].keys()
        #])
        word_err_count = ([
            doc['latest_data']['word_err_count'] for doc in documents
            if doc.get('latest_data') is not None and 'word_err_count' in doc['latest_data'].keys()
        ])
#        chip_number = ([
#            doc['_id'] for doc in documents
#            if doc.get('latest_data') is not None and 'word_err_count' in doc['latest_data'].keys()
#        ])


        return word_err_count

    def getPassFailResults(self, econType = 'ECOND',tray_number = None, perDay=None):
        #This function returns a dataframe for the testing summary plots prepared by Marko
        #Please use the econType argument to specify ECOND or ECONT and the function expects a string for this argument
        voltage_field_map = {
            'None': {
                    'individual_test_outcomes':'individual_test_outcomes',
                    'chipNum':"chip_number",
                    'Timestamp':'Timestamp',
                    'IP': 'FPGA-hexa-IP'
                    },
        }
        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, perDay=perDay)
        cursor = self.db['TestSummary'].aggregate(pipeline)
        documents = list(cursor)
        testOutcomes = ([
            doc['latest_data']['individual_test_outcomes'] for doc in documents
            if doc.get('latest_data') is not None and 'individual_test_outcomes' in doc['latest_data'].keys()
        ])
        chipNums = ([
            doc['latest_data']['chipNum'] for doc in documents
            if doc.get('latest_data') is not None and 'chipNum' in doc['latest_data'].keys()
        ])
        Timestamp = ([
            doc['latest_data']['Timestamp'] for doc in documents
            if doc.get('latest_data') is not None and 'Timestamp' in doc['latest_data'].keys()
        ])
        IP = ([
            doc['latest_data']['IP'] for doc in documents
            if doc.get('latest_data') is not None and 'IP' in doc['latest_data'].keys()
        ])
        return testOutcomes, chipNums, Timestamp, IP

    def retrieveTestPacketInfo(self, lowerLim=None, upperLim=None, perDay=None, econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT

        #note this test does not run at different voltages but I wanted to just have something there so the format of all the functions are uniform
        voltage_field_map = {
            'None': {
                    'test_single_fcsequence_counter_100-None-fc_sequence0-eTx-0-errcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence0-eTx-0.metadata.sc_err_count',
                    'test_single_fcsequence_counter_100-None-fc_sequence0-eTx-0-wordcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence0-eTx-0.metadata.sc_word_count',
                    'test_single_fcsequence_counter_100-None-fc_sequence1-eTx-01-errcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence1-eTx-01.metadata.sc_err_count',
                    'test_single_fcsequence_counter_100-None-fc_sequence1-eTx-01-wordcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence1-eTx-01.metadata.sc_word_count',
                    'test_single_fcsequence_counter_100-None-fc_sequence2-eTx-012-errcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence2-eTx-012.metadata.sc_err_count',
                    'test_single_fcsequence_counter_100-None-fc_sequence2-eTx-012-wordcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence2-eTx-012.metadata.sc_word_count',
                    'test_single_fcsequence_counter_100-None-fc_sequence3-eTx-0123-errcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence3-eTx-0123.metadata.sc_err_count',
                    'test_single_fcsequence_counter_100-None-fc_sequence3-eTx-0123-wordcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence3-eTx-0123.metadata.sc_word_count',
                    'test_single_fcsequence_counter_100-None-fc_sequence4-eTx-01234-errcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence4-eTx-01234.metadata.sc_err_count',
                    'test_single_fcsequence_counter_100-None-fc_sequence4-eTx-01234-wordcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence4-eTx-01234.metadata.sc_word_count',
                    'test_single_fcsequence_counter_100-None-fc_sequence5-eTx-012345-errcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence5-eTx-012345.metadata.sc_err_count',
                    'test_single_fcsequence_counter_100-None-fc_sequence5-eTx-012345-wordcnt': 'test_info.test_single_fcsequence_counter_100-None-fc_sequence5-eTx-012345.metadata.sc_word_count',
                    'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence6-ZS_c_i_1-errcnt': 'test_info.test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence6-ZS_c_i_1.metadata.sc_err_count',
                    'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence6-ZS_c_i_1-wordcnt': 'test_info.test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence6-ZS_c_i_1.metadata.sc_word_count',
                    'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence7-ZS_37-errcnt': 'test_info.test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence7-ZS_37.metadata.sc_err_count',
                    'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence7-ZS_37-wordcnt': 'test_info.test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence7-ZS_37.metadata.sc_word_count',
                    'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence8-ZS_37-errcnt': 'test_info.test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence8-ZS_37.metadata.sc_err_count',
                    'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence8-ZS_37-wordcnt': 'test_info.test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence8-ZS_37.metadata.sc_word_count',
                    'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence9-ZS_37-errcnt': 'test_info.test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence9-ZS_37.metadata.sc_err_count',
                    'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence9-ZS_37-wordcnt': 'test_info.test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence9-ZS_37.metadata.sc_word_count',
                    'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence10-pass_thru-errcnt': 'test_info.test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence10-pass_thru.metadata.sc_err_count',
                    'test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence10-pass_thru-wordcnt': 'test_info.test_single_fcsequence_None-__econd_testvectors_exampleData_testVectorInputs_Random_csv-fc_sequence10-pass_thru.metadata.sc_word_count',
                    'test_fill_buffer-errcnt0': 'test_info.test_fill_buffer.metadata.sc_err_count_0',
                    'test_fill_buffer-wordcnt0': 'test_info.test_fill_buffer.metadata.sc_word_count_0',
                    'test_fill_buffer-errcnt1': 'test_info.test_fill_buffer.metadata.sc_err_count_1',
                    'test_fill_buffer-wordcnt1': 'test_info.test_fill_buffer.metadata.sc_word_count_1',
                    'test_fill_buffer-errcnt2': 'test_info.test_fill_buffer.metadata.sc_err_count_2',
                    'test_fill_buffer-wordcnt2': 'test_info.test_fill_buffer.metadata.sc_word_count_2',
                    'chipNum':"chip_number"

                },
        }

        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim=lowerLim, upperLim=upperLim, perDay=perDay)
        cursor = self.db['testPacketsInfo'].aggregate(pipeline)
        documents = list(cursor)
        # Initialize a dictionary to hold results dynamically
        result_dict = {}
        test_single_fcsequence_counter_100_None_fc_sequence0_eTx_0_errcnt = np.array([
            doc['latest_data']['test_single_fcsequence_counter_100-None-fc_sequence0-eTx-0-errcnt'] if doc.get('latest_data') is not None and 'test_single_fcsequence_counter_100-None-fc_sequence0-eTx-0-errcnt' in doc['latest_data'].keys() else None for doc in documents
        ])
        # Loop over each field in the query_map
        for field_key, field_value in query_map.items():
            # Extract the relevant field from the documents (handling None and missing keys)
            result_dict[field_key] = np.array([
                doc['latest_data'].get(field_key, None) if doc.get('latest_data') else None
                for doc in documents
            ])

        return result_dict
    def retrieveTestAlgorithmInfo(self, lowerLim=None, upperLim=None, perDay=None, econType = 'ECONT'):
        voltage_field_map = {
            'None': {
                        'test_algorithm_compression_emu___econt_testvectors_counterPatternInTC_RPT_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_counterPatternInTC_RPT_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_counterPatternInTC_RPT_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_counterPatternInTC_RPT_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_randomPatternExpInTC_TS_Thr100_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_randomPatternExpInTC_TS_Thr100_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_randomPatternExpInTC_TS_Thr100_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_randomPatternExpInTC_TS_Thr100_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_counterPatternInTC_TS_Thr47_13eTx_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_counterPatternInTC_TS_Thr47_13eTx_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_counterPatternInTC_TS_Thr47_13eTx_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_counterPatternInTC_TS_Thr47_13eTx_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx5_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx5_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx5_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx5_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx4_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx4_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx4_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx4_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx3_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx3_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx3_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx3_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx2_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx2_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx2_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx2_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx1_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx1_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx1_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type0_eTx1_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type1_eTx2_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type1_eTx2_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type1_eTx2_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type1_eTx2_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type1_eTx1_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type1_eTx1_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type1_eTx1_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type1_eTx1_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx3_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx3_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx3_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx3_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx2_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx2_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx2_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx2_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx1_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx1_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx1_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type2_eTx1_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx1_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx1_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx1_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx1_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx2_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx2_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx2_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx2_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx3_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx3_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx3_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx3_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx4_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx4_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx4_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type3_eTx4_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx1_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx1_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx1_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx1_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx2_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx2_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx2_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx2_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx3_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx3_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx3_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx3_.metadata.sc_word_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx4_-errcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx4_.metadata.sc_err_count',
                        'test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx4_-wordcnt': 'test_info.test_algorithm_compression_emu___econt_testvectors_mcDataset_STC_type4_eTx4_.metadata.sc_word_count',
                        'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_RPT_-errcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_RPT_.metadata.sc_err_count',
                        'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_RPT_-wordcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_RPT_.metadata.sc_word_count',
                        'test_algorithm_compression_bypass___econt_testvectors_mcDataset_RPT_13eTx_-errcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_mcDataset_RPT_13eTx_.metadata.sc_err_count',
                        'test_algorithm_compression_bypass___econt_testvectors_mcDataset_RPT_13eTx_-wordcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_mcDataset_RPT_13eTx_.metadata.sc_word_count',
                        'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_10eTx_-errcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_10eTx_.metadata.sc_err_count',
                        'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_10eTx_-wordcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_10eTx_.metadata.sc_word_count',
                        'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_5eTx_-errcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_5eTx_.metadata.sc_err_count',
                        'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_5eTx_-wordcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_5eTx_.metadata.sc_word_count',
                        'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_1eTx_-errcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_1eTx_.metadata.sc_err_count',
                        'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_1eTx_-wordcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_BC_1eTx_.metadata.sc_word_count',
                        'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_TS_Thr47_13eTx_-errcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_TS_Thr47_13eTx_.metadata.sc_err_count',
                        'test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_TS_Thr47_13eTx_-wordcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_counterPatternInTC_by2_TS_Thr47_13eTx_.metadata.sc_word_count',
                        'test_algorithm_compression_bypass___econt_testvectors_mcDataset_AE-errcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_mcDataset_AE.metadata.sc_err_count',
                        'test_algorithm_compression_bypass___econt_testvectors_mcDataset_AE-wordcnt': 'test_info.test_algorithm_compression_bypass___econt_testvectors_mcDataset_AE.metadata.sc_word_count',
                        'test_fill_buffer-errcnt': 'test_info.test_fill_buffer.metadata.sc_err_count',
                        'test_fill_buffer-wordcnt': 'test_info.test_fill_buffer.metadata.sc_word_count',
                        'chipNum':"chip_number"
            },
        }
        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim=lowerLim, upperLim=upperLim, perDay=perDay)
        cursor = self.db['testPacketsInfo'].aggregate(pipeline)
        documents = list(cursor)
        # Initialize a dictionary to hold results dynamically
        result_dict = {}
        # Loop over each field in the query_map
        for field_key, field_value in query_map.items():
            # Extract the relevant field from the documents (handling None and missing keys)
            result_dict[field_key] = np.array([
                doc['latest_data'].get(field_key, None) if doc.get('latest_data') else None
                for doc in documents
            ])

        return result_dict
        
    def retrieveTestMuxInfo(self, lowerLim=None, upperLim=None, perDay=None, econType = 'ECONT'):
        voltage_field_map = {
            'None': {
                'test_mux-errcnt': 'test_info.test_mux.metadata.error_counts',
                'test_mux-wordcnt': 'test_info.test_mux.metadata.word_counts',
                'test_float_to_fix-errcnt': 'test_info.test_float_to_fix.metadata.error_counts',
                'test_float_to_fix-wordcnt': 'test_info.test_float_to_fix.metadata.word_counts',
                'test_calibrations-errcnt': 'test_info.test_calibrations.metadata.error_counts',
                'test_calibrations-wordcnt': 'test_info.test_calibrations.metadata.word_counts', 
                'chipNum':"chip_number"
            },
        }
        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim=lowerLim, upperLim=upperLim, perDay=perDay)
        cursor = self.db['testMuxCalibInfo'].aggregate(pipeline)
        documents = list(cursor)
        # Initialize a dictionary to hold results dynamically
        result_dict = {}
        # Loop over each field in the query_map
        for field_key, field_value in query_map.items():
            # Extract the relevant field from the documents (handling None and missing keys)
            result_dict[field_key] = ([
                doc['latest_data'].get(field_key, None) if doc.get('latest_data') else None
                for doc in documents
            ])

        return result_dict
        
    def retrieveI2Cerrcnts(self, lowerLim=None, upperLim=None, perDay=None, econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT

        #note this test does not run at different voltages but I wanted to just have something there so the format of all the functions are uniform
        voltage_field_map = {
            'None': {
                    'chipNum':"chip_number",
                    'n_read_errors_asic':'test_info.test_check_error_counts.metadata.n_read_errors_asic',
                    'n_read_errors_emulator':'test_info.test_check_error_counts.metadata.n_read_errors_emulator',
                    'n_write_errors_asic':'test_info.test_check_error_counts.metadata.n_write_errors_asic',
                    'n_write_errors_emulator':'test_info.test_check_error_counts.metadata.n_write_errors_emulator',

                },
        }

        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim=lowerLim, upperLim=upperLim)
        cursor = self.db['testI2CInfo'].aggregate(pipeline)
        documents = list(cursor)
        chipNum = np.array([
            doc['latest_data']['chipNum'] if doc.get('latest_data') is not None and 'chipNum' in doc['latest_data'].keys() else None for doc in documents
        ])

        n_read_errors_asic = np.array([
            doc['latest_data']['n_read_errors_asic'] if doc.get('latest_data') is not None and 'n_read_errors_asic' in doc['latest_data'].keys() else None for doc in documents
        ])

        n_read_errors_emulator = np.array([
            doc['latest_data']['n_read_errors_emulator'] if doc.get('latest_data') is not None and 'n_read_errors_emulator' in doc['latest_data'].keys() else None for doc in documents
        ])
        n_write_errors_asic = np.array([
            doc['latest_data']['n_write_errors_asic'] if doc.get('latest_data') is not None and 'n_write_errors_asic' in doc['latest_data'].keys() else None for doc in documents
        ])
        n_write_errors_emulator = np.array([
            doc['latest_data']['n_write_errors_emulator'] if doc.get('latest_data') is not None and 'n_write_errors_emulator' in doc['latest_data'].keys() else None for doc in documents
        ])

        return chipNum, n_read_errors_asic, n_read_errors_emulator, n_write_errors_asic, n_write_errors_emulator


    def testStreamComparison(self, econType = 'ECOND', perDay=None, tray_number = None):
            #Returns info from the OB error test
            #This returns DAQ_asic, DAQ_emu, DAQ_counter, and word_err_cnt
            #This is done for the voltages 0.99, 1.03, and 1.08
            #specify which voltage you want when calling the function
            # 0p99 for 0.99, 1p03 for 1.03, and 1p08 for 1.08V

            voltage_field_map = {
                'None': {
                        'word_err_count_0p99':'test_info.test_streamCompareLoop_0_99.metadata.word_err_count',
                        'word_err_count_1p03':'test_info.test_streamCompareLoop_1_03.metadata.word_err_count',
                        'word_err_count_1p08':'test_info.test_streamCompareLoop_1_08.metadata.word_err_count',
                        'word_err_count_1p20':'test_info.test_streamCompareLoop_1_2.metadata.word_err_count',
                        'chipNum':"chip_number",

                }
            }

            query_map = voltage_field_map['None']
            pipeline = constructQueryPipeline(query_map, econType=econType, perDay=perDay)
            cursor = self.db['testOBError'].aggregate(pipeline)
            documents = list(cursor)

            if tray_number is not None:
                documents = self.filter_by_tray(documents, tray_number)

            chipNum = np.array([
            doc['latest_data']['chipNum'] if doc.get('latest_data') is not None and 'chipNum' in doc['latest_data'].keys() else None for doc in documents
            ])
            word_err_count_0p99 = ([
            doc['latest_data']['word_err_count_0p99'] if doc.get('latest_data') is not None and 'word_err_count_0p99' in doc['latest_data'].keys() else None for doc in documents
            ])
            word_err_count_1p03 = ([
            doc['latest_data']['word_err_count_1p03'] if doc.get('latest_data') is not None and 'word_err_count_1p03' in doc['latest_data'].keys() else None for doc in documents
            ])
            word_err_count_1p08 = ([
            doc['latest_data']['word_err_count_1p08'] if doc.get('latest_data') is not None and 'word_err_count_1p08' in doc['latest_data'].keys() else None for doc in documents
            ])
            word_err_count_1p20 = ([
            doc['latest_data']['word_err_count_1p20'] if doc.get('latest_data') is not None and 'word_err_count_1p20' in doc['latest_data'].keys() else None for doc in documents
            ])
            return word_err_count_0p99, word_err_count_1p03, word_err_count_1p08, word_err_count_1p20, chipNum



    def getBISTInfoFull(self, lowerLim=None, upperLim=None, econType='ECOND', perDay=None, tray_number = None):
            #This function makes a plot of the PLL Capbank Width
            #if the user provides a range it will plot only over that range
            #if not it plots the capbank width over the whole dataset
            #for different voltages use the name argument and please provide a string
            # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
            #Also use the ECON type argument to make request info for ECOND vs ECONT

            voltage_field_map = {
                'None': {
                        'voltages':'test_info.test_bist_full.metadata.voltages',
                        'bist_results':'test_info.test_bist_full.metadata.bist_results',
                        'chipNum':'chip_number',
                        },
            }

            query_map = voltage_field_map['None']
            pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim, perDay=perDay)
            cursor = self.db['testBistInfo'].aggregate(pipeline)
            documents = list(cursor)

            if tray_number is not None:
                documents = self.filter_by_tray(documents, tray_number)
            voltages = ([
                doc['latest_data']['voltages'] if doc.get('latest_data') is not None and 'voltages' in doc['latest_data'].keys() else None for doc in documents
            ])
            bist_results = ([
                doc['latest_data']['bist_results'] if doc.get('latest_data') is not None and 'bist_results' in doc['latest_data'].keys() else None for doc in documents
            ])
            chipNum = ([
                doc['latest_data']['chipNum'] if doc.get('latest_data') is not None and 'chipNum' in doc['latest_data'].keys() else None for doc in documents
            ])

            return voltages, bist_results, chipNum

    def getVoltageAndCurrentCSV(self, lowerLim=None, upperLim=None, perDay=None, econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT

        #note this test does not run at different voltages but I wanted to just have something there so the format of all the functions are uniform
        voltage_field_map = {
            'None': {
                    'current':'test_info.test_currentdraw_1p2V.metadata.current',
                    'voltage':'test_info.test_currentdraw_1p2V.metadata.voltage',
                    'current_during_hardreset':'test_info.test_currentdraw_1p2V.metadata.current_during_hardreset',
                    'current_after_hardreset':'test_info.test_currentdraw_1p2V.metadata.current_after_hardreset',
                    'current_during_softreset':'test_info.test_currentdraw_1p2V.metadata.current_during_softreset',
                    'current_after_softreset':'test_info.test_currentdraw_1p2V.metadata.current_after_softreset',
                    'current_runbit_set':'test_info.test_currentdraw_1p2V.metadata.current_runbit_set',
                    'temperature':'test_info.test_currentdraw_1p2V.metadata.zynqTemp',
                    'chipNum':"chip_number"
                    },
        }

        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim, perDay=perDay)
        cursor = self.db['testPowerInfo'].aggregate(pipeline)
        documents = list(cursor)
        #main measurements
        current = np.array([
            doc['latest_data']['current'] if doc.get('latest_data') is not None and 'current' in doc['latest_data'].keys() else None for doc in documents
        ])

        voltage = np.array([
            doc['latest_data']['voltage'] if doc.get('latest_data') is not None and 'voltage' in doc['latest_data'].keys() else None for doc in documents
        ])

        current_during_hardreset = np.array([
            doc['latest_data']['current_during_hardreset'] if doc.get('latest_data') is not None and 'current_during_hardreset' in doc['latest_data'].keys() else None for doc in documents
        ])
        current_after_hardreset = np.array([
            doc['latest_data']['current_after_hardreset'] if doc.get('latest_data') is not None and 'current_after_hardreset' in doc['latest_data'].keys() else None for doc in documents
        ])
        current_during_softreset = np.array([
            doc['latest_data']['current_during_softreset'] if doc.get('latest_data') is not None and 'current_during_softreset' in doc['latest_data'].keys() else None for doc in documents
        ])
        current_after_softreset = np.array([
            doc['latest_data']['current_after_softreset'] if doc.get('latest_data') is not None and 'current_after_softreset' in doc['latest_data'].keys() else None for doc in documents
        ])
        current_runbit_set = np.array([
            doc['latest_data']['current_runbit_set'] if doc.get('latest_data') is not None and 'current_runbit_set' in doc['latest_data'].keys() else None for doc in documents
        ])
        temperature = np.array([
            doc['latest_data']['temperature'] if doc.get('latest_data') is not None and 'temperature' in doc['latest_data'].keys() else None for doc in documents
        ])
        chipNum = np.array([
            doc['latest_data']['chipNum'] for doc in documents
            if doc.get('latest_data') is not None and 'chipNum' in doc['latest_data'].keys()
        ])
        return current, voltage, current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set, temperature, chipNum

    def getFirstFailureCSV(self, lowerLim=None, upperLim=None, econType='ECOND', perDay=None, tray_number = None):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        # 1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT

        voltage_field_map = {
            'None': {
                    'first_failure':'test_info.test_bist.metadata.first_failure',
                    'chipNum':'chip_number',
                    },
        }

        query_map = voltage_field_map['None']
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim, perDay=perDay)
        cursor = self.db['testBistInfo'].aggregate(pipeline)
        documents = list(cursor)

        if tray_number is not None:
            documents = self.filter_by_tray(documents, tray_number)

        first_failure = ([
                doc['latest_data']['first_failure'] if doc.get('latest_data') is not None and 'first_failure' in doc['latest_data'].keys() else None for doc in documents
            ])
        chipNum = ([
                doc['latest_data']['chipNum'] if doc.get('latest_data') is not None and 'chipNum' in doc['latest_data'].keys() else None for doc in documents
            ])

        return first_failure, chipNum


    def testIoCSV(self, lowerLim=None, upperLim=None, perDay=None, voltage = 'None', econType = 'ECOND'):
        #This function makes a plot of the eTX Delay scan Max Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT
        voltage_field_map = {
             'None':{
            'delayscan_maxwidth_1p08':'test_info.test_eTX_delayscan_1_08.metadata.max_width',
            'delayscan_maxwidth_1p2':'test_info.test_eTX_delayscan_1_2.metadata.max_width',
            'delayscan_maxwidth_1p32':'test_info.test_eTX_delayscan_1_32.metadata.max_width',
            'phasescan_maxwidth_1p08':'test_info.test_ePortRXPRBS_1_08.metadata.maxwidth',
            'phasescan_maxwidth_1p2':'test_info.test_ePortRXPRBS_1_2.metadata.maxwidth',
            'phasescan_maxwidth_1p32':'test_info.test_ePortRXPRBS_1_32.metadata.maxwidth',
            'chipNum':'chip_number',}
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim)
        cursor = self.db['testIOInfo'].aggregate(pipeline)
        documents = list(cursor)
        delayscan_maxwidth_1p08 = ([
            doc['latest_data']['delayscan_maxwidth_1p08'] if doc.get('latest_data') is not None and 'delayscan_maxwidth_1p08' in doc['latest_data'].keys() else None for doc in documents
        ])
        delayscan_maxwidth_1p2 = ([
            doc['latest_data']['delayscan_maxwidth_1p2'] if doc.get('latest_data') is not None and 'delayscan_maxwidth_1p2' in doc['latest_data'].keys() else None for doc in documents
        ])
        delayscan_maxwidth_1p32 = ([
            doc['latest_data']['delayscan_maxwidth_1p32'] if doc.get('latest_data') is not None and 'delayscan_maxwidth_1p32' in doc['latest_data'].keys() else None for doc in documents
        ])

        phasescan_maxwidth_1p08 = ([
            doc['latest_data']['phasescan_maxwidth_1p08'] if doc.get('latest_data') is not None and 'phasescan_maxwidth_1p08' in doc['latest_data'].keys() else None for doc in documents
        ])
        phasescan_maxwidth_1p2 = ([
            doc['latest_data']['phasescan_maxwidth_1p2'] if doc.get('latest_data') is not None and 'phasescan_maxwidth_1p2' in doc['latest_data'].keys() else None for doc in documents
        ])
        phasescan_maxwidth_1p32 = ([
            doc['latest_data']['phasescan_maxwidth_1p32'] if doc.get('latest_data') is not None and 'phasescan_maxwidth_1p32' in doc['latest_data'].keys() else None for doc in documents
        ])

        chipNum = ([
                doc['latest_data']['chipNum'] if doc.get('latest_data') is not None and 'chipNum' in doc['latest_data'].keys() else None for doc in documents
            ])
        return delayscan_maxwidth_1p08, delayscan_maxwidth_1p2, delayscan_maxwidth_1p32, phasescan_maxwidth_1p08, phasescan_maxwidth_1p2, phasescan_maxwidth_1p32, chipNum

    def testPllCSV(self, lowerLim=None, upperLim=None, voltage = 'None', econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT
        voltage_field_map = {
            'None': {
                    'capbankwidth_1p08':'test_info.test_pll_capbank_width_1_08.metadata.pll_capbank_width',
                    'capbankwidth_1p2':'test_info.test_pll_capbank_width_1_2.metadata.pll_capbank_width',
                    'capbankwidth_1p32':'test_info.test_pll_capbank_width_1_32.metadata.pll_capbank_width',
                    'chipNum':'chip_number',
                    'minFreq_1p08':'test_info.test_pllautolock_1_08.metadata.min_freq',
                    'maxFreq_1p08':'test_info.test_pllautolock_1_08.metadata.max_freq',
                    'minFreq_1p2':'test_info.test_pllautolock_1_2.metadata.min_freq',
                    'maxFreq_1p2':'test_info.test_pllautolock_1_2.metadata.max_freq',
                    'minFreq_1p32':'test_info.test_pllautolock_1_32.metadata.min_freq',
                    'maxFreq_1p32':'test_info.test_pllautolock_1_32.metadata.max_freq',
            },
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim)
        cursor = self.db['testPLLInfo'].aggregate(pipeline)
        documents = list(cursor)
        chipNum = ([
                doc['latest_data']['chipNum'] if doc.get('latest_data') is not None and 'chipNum' in doc['latest_data'].keys() else None for doc in documents
            ])
        ########################################################################################################################
        capbankwidth_1p08 = ([
                doc['latest_data']['capbankwidth_1p08'] if doc.get('latest_data') is not None and 'capbankwidth_1p08' in doc['latest_data'].keys() else None for doc in documents
            ])
        capbankwidth_1p2 = ([
                doc['latest_data']['capbankwidth_1p2'] if doc.get('latest_data') is not None and 'capbankwidth_1p2' in doc['latest_data'].keys() else None for doc in documents
            ])
        capbankwidth_1p32 = ([
                doc['latest_data']['capbankwidth_1p32'] if doc.get('latest_data') is not None and 'capbankwidth_1p32' in doc['latest_data'].keys() else None for doc in documents
            ])
         ########################################################################################################################
        minFreq_1p08 = ([
                doc['latest_data']['minFreq_1p08'] if doc.get('latest_data') is not None and 'minFreq_1p08' in doc['latest_data'].keys() else None for doc in documents
            ])
        minFreq_1p2 = ([
                doc['latest_data']['minFreq_1p2'] if doc.get('latest_data') is not None and 'minFreq_1p2' in doc['latest_data'].keys() else None for doc in documents
            ])
        minFreq_1p32 = ([
                doc['latest_data']['minFreq_1p32'] if doc.get('latest_data') is not None and 'minFreq_1p32' in doc['latest_data'].keys() else None for doc in documents
            ])
         ########################################################################################################################
        maxFreq_1p08 = ([
                doc['latest_data']['maxFreq_1p08'] if doc.get('latest_data') is not None and 'maxFreq_1p08' in doc['latest_data'].keys() else None for doc in documents
            ])
        maxFreq_1p2 = ([
                doc['latest_data']['maxFreq_1p2'] if doc.get('latest_data') is not None and 'maxFreq_1p2' in doc['latest_data'].keys() else None for doc in documents
            ])
        maxFreq_1p32 = ([
                doc['latest_data']['maxFreq_1p32'] if doc.get('latest_data') is not None and 'maxFreq_1p32' in doc['latest_data'].keys() else None for doc in documents
            ])
         ########################################################################################################################
        return chipNum, capbankwidth_1p08, capbankwidth_1p2, capbankwidth_1p32, minFreq_1p08, minFreq_1p2, minFreq_1p32, maxFreq_1p08, maxFreq_1p2, maxFreq_1p32

    def minMaxFrequencyPlot(self, lowerLim=None, upperLim=None, perDay=None, voltage = 'None', econType = 'ECOND'):
        #This function makes a plot of the PLL Capbank Width
        #if the user provides a range it will plot only over that range
        #if not it plots the capbank width over the whole dataset
        #for different voltages use the name argument and please provide a string
        #1p08 for 1.08V, 1p2 for 1.2V, 1p32 for 1.32V
        #Also use the ECON type argument to make request info for ECOND vs ECONT
        voltage_field_map = {
            'None': {
                    'minFreq_1p08':'test_info.test_pllautolock_1_08.metadata.min_freq',
                    'maxFreq_1p08':'test_info.test_pllautolock_1_08.metadata.max_freq',
                    'minFreq_1p2':'test_info.test_pllautolock_1_2.metadata.min_freq',
                    'maxFreq_1p2':'test_info.test_pllautolock_1_2.metadata.max_freq',
                    'minFreq_1p32':'test_info.test_pllautolock_1_32.metadata.min_freq',
                    'maxFreq_1p32':'test_info.test_pllautolock_1_32.metadata.max_freq',
            },
        }
        if voltage not in voltage_field_map:
            raise ValueError("Invalid voltage specified. Choose from '1p08', '1p2', '1p32'.")
        query_map = voltage_field_map[voltage]
        pipeline = constructQueryPipeline(query_map, econType=econType, lowerLim = lowerLim, upperLim=upperLim, perDay=perDay)
        cursor = self.db['testPLLInfo'].aggregate(pipeline)
        documents = list(cursor)

         ########################################################################################################################
        minFreq_1p08 = ([
                doc['latest_data']['minFreq_1p08'] if doc.get('latest_data') is not None and 'minFreq_1p08' in doc['latest_data'].keys() else None for doc in documents
            ])
        minFreq_1p2 = ([
                doc['latest_data']['minFreq_1p2'] if doc.get('latest_data') is not None and 'minFreq_1p2' in doc['latest_data'].keys() else None for doc in documents
            ])
        minFreq_1p32 = ([
                doc['latest_data']['minFreq_1p32'] if doc.get('latest_data') is not None and 'minFreq_1p32' in doc['latest_data'].keys() else None for doc in documents
            ])
         ########################################################################################################################
        maxFreq_1p08 = ([
                doc['latest_data']['maxFreq_1p08'] if doc.get('latest_data') is not None and 'maxFreq_1p08' in doc['latest_data'].keys() else None for doc in documents
            ])
        maxFreq_1p2 = ([
                doc['latest_data']['maxFreq_1p2'] if doc.get('latest_data') is not None and 'maxFreq_1p2' in doc['latest_data'].keys() else None for doc in documents
            ])
        maxFreq_1p32 = ([
                doc['latest_data']['maxFreq_1p32'] if doc.get('latest_data') is not None and 'maxFreq_1p32' in doc['latest_data'].keys() else None for doc in documents
            ])
         ########################################################################################################################
        return minFreq_1p08, minFreq_1p2, minFreq_1p32, maxFreq_1p08, maxFreq_1p2, maxFreq_1p32
