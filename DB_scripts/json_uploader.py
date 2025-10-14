# Functions to upload files in database


import pymongo
from pymongo import MongoClient, InsertOne
import numpy as np
import glob
import json
from datetime import datetime

def selector(input):
    if input == 'passed':
        return int(1)
    elif input == 'failed':
        return int(0)
    ## This is for a test that was skipped
    elif input == 'error':
        return int(-1)
    else:
        return int(-2)

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
        word = word.replace(".","_")
    return word

def grabFailureInfo(test):
    result = {"failure_information":{
                        "failure_mode": test['call']['traceback'][0]['message'] if test['call']['traceback'][0]['message'] != '' else test['call']['crash']['message'],
                        "failure_cause": test['call']['crash']['message'],
                        "failure_code_line": test["call"]["crash"]["lineno"],
                } if 'failed' in test['outcome'] else None,}
    return result
def convert_values_to_string(d):
    # Check if the dictionary is empty
    if not d:
        return d  # Return the empty dictionary if it's empty
    
    # Convert all values to strings if the dictionary is not empty
    return {key: str(value) for key, value in d.items()}


def jsonFileUploader(fname, mydatabase):
    ## open the JSON File
    with open(fname) as jsonfile:
        data = json.load(jsonfile)
    non_testing_keys = []
    for key in data.keys():
        if 'summary' not in key:
            if 'tests' not in key:
                non_testing_keys.append(key)
    
    non_testing_info = {
        key: data[key] for key in non_testing_keys
    }

    for test in data['tests']:
        if 'stream' in test['nodeid']:
            try:
                test['metadata']['snapshots'] = str(test['metadata']['snapshots'])
            except:
                print(f'No metadata in {test["nodeid"]}')
        if 'test_soft_reset_i2c_allregisters' in test['nodeid']:
            test['metadata']['mismatch_dict'] = convert_values_to_string(test['metadata']['mismatch_dict'])
        if 'test_hard_reset_i2c_allregisters' in test['nodeid']:
            test['metadata']['mismatch_dict'] = convert_values_to_string(test['metadata']['mismatch_dict'])
        if 'test_rw_allregisters[0]' in test['nodeid']:
            test['metadata']['mismatch_dict'] = convert_values_to_string(test['metadata']['mismatch_dict'])
        if 'test_rw_allregisters[255]' in test['nodeid']:
            test['metadata']['mismatch_dict'] = convert_values_to_string(test['metadata']['mismatch_dict'])
        if 'test_chip_sync' in test['nodeid']:
            test['metadata']['mismatch_dict'] = convert_values_to_string(test['metadata']['mismatch_dict'])
        
    testingSummary = {
            "summary": {'passed': data['summary']['passed'], 'total':data['summary']['total'], 'collected':data['summary']['collected']},
            "individual_test_outcomes": {
                 f"{stringReplace(test['nodeid'].split('::')[1])}": selector(test['outcome']) for test in data['tests']
             },
            "chip_number": data['chip_number'],
            "branch": data['branch'],
            'commit_hash': data['commit_hash'],
            'remote_url': data['remote_url'],
            'FPGA-hexa-IP': data['FPGA-hexa-IP'],
            'status': data['status'],
            'firmware_name': data['firmware_name'],
            'firmware_git_desc': data['firmware_git_desc'],
            'filename': fname,
            'duration': data['duration'],
            'ECON_type':(fname.split("report"))[1].split("_")[1],
            'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
            }
    
    i2c_info = {
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_i2c' in test['nodeid']}
    }
    power_info = {
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_power' in test['nodeid']},
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
    }
    testfc_info = {
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_fc' in test['nodeid']},
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
    }
    testio_info = {
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_io' in test['nodeid']},
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
    }
    testbist_info = {
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_bist' in test['nodeid']},
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
    }
    testcommonmode_info = {
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_common' in test['nodeid']},
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
    }
    testerrin_info = {
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_errin' in test['nodeid']},
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
    }

    testinputaligner_info = {
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_input_aligner' in test['nodeid']},
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
    }
    try:
        testmuxcalib_info = {
            'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                               'outcome': test['outcome'],
                                                               'keywords': test['keywords'],
                                                               'setup':test['setup'] if 'setup' in test else None,
                                                               'call':test['call'] if 'call' in test else None,
                                                               'teardown':test['teardown'] if 'teardown' in test else None,
                                                               'failure_information':grabFailureInfo(test),
                                                               } for test in data['tests'] if 'test_mux_fix' in test['nodeid']},
            "chip_number": data["chip_number"],
            "branch": data['branch'],
            'commit_hash': data['commit_hash'],
            'remote_url': data['remote_url'],
            'FPGA-hexa-IP': data['FPGA-hexa-IP'],
            'status': data['status'],
            'firmware_name': data['firmware_name'],
            'firmware_git_desc': data['firmware_git_desc'],
            'filename': fname,
            'ECON_type':(fname.split("report"))[1].split("_")[1],
            'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
        }
        mydatabase['testMuxCalibInfo'].insert_one(testmuxcalib_info)
    except:
        testmuxcalib_info = {
            'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {
                                                               'outcome': test['outcome'],
                                                               'keywords': test['keywords'],
                                                               'setup':test['setup'] if 'setup' in test else None,
                                                               'call':test['call'] if 'call' in test else None,
                                                               'teardown':test['teardown'] if 'teardown' in test else None,
                                                               'failure_information':grabFailureInfo(test),
                                                               } for test in data['tests'] if 'test_mux_fix' in test['nodeid']},
            "chip_number": data["chip_number"],
            "branch": data['branch'],
            'commit_hash': data['commit_hash'],
            'remote_url': data['remote_url'],
            'FPGA-hexa-IP': data['FPGA-hexa-IP'],
            'status': data['status'],
            'firmware_name': data['firmware_name'],
            'firmware_git_desc': data['firmware_git_desc'],
            'filename': fname,
            'ECON_type':(fname.split("report"))[1].split("_")[1],
            'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
        }
        mydatabase['testMuxCalibInfo'].insert_one(testmuxcalib_info)
        
    testresetrequest_info = {
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_reset_requests' in test['nodeid']},
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
    }
    testserializer_info = {
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_serializer' in test['nodeid']},
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
    }
    try:
        testzs_info = {
            'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                               'outcome': test['outcome'],
                                                               'keywords': test['keywords'],
                                                               'setup':test['setup'] if 'setup' in test else None,
                                                               'call':test['call'] if 'call' in test else None,
                                                               'teardown':test['teardown'] if 'teardown' in test else None,
                                                               'failure_information':grabFailureInfo(test),
                                                               } for test in data['tests'] if 'test_zs' in test['nodeid']},
            "chip_number": data["chip_number"],
            'hard_failure': False,
            "branch": data['branch'],
            'commit_hash': data['commit_hash'],
            'remote_url': data['remote_url'],
            'FPGA-hexa-IP': data['FPGA-hexa-IP'],
            'status': data['status'],
            'firmware_name': data['firmware_name'],
            'firmware_git_desc': data['firmware_git_desc'],
            'filename': fname,
            'ECON_type':(fname.split("report"))[1].split("_")[1],
            'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
        }
        mydatabase['testZSInfo'].insert_one(testzs_info)
    except:
        testzs_info = {
            'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {
                                                               'outcome': test['outcome'],
                                                               'keywords': test['keywords'],
                                                               'setup':test['setup'] if 'setup' in test else None,
                                                               'call':test['call'] if 'call' in test else None,
                                                               'teardown':test['teardown'] if 'teardown' in test else None,
                                                               'failure_information':grabFailureInfo(test),
                                                               } for test in data['tests'] if 'test_zs' in test['nodeid']},
            "chip_number": data["chip_number"],
            'hard_failure': True,
            "branch": data['branch'],
            'commit_hash': data['commit_hash'],
            'remote_url': data['remote_url'],
            'FPGA-hexa-IP': data['FPGA-hexa-IP'],
            'status': data['status'],
            'firmware_name': data['firmware_name'],
            'firmware_git_desc': data['firmware_git_desc'],
            'filename': fname,
            'ECON_type':(fname.split("report"))[1].split("_")[1],
            'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
        }
        mydatabase['testZSInfo'].insert_one(testzs_info)

    try:
        testalgorithm_info = {
            'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                               'outcome': test['outcome'],
                                                               'keywords': test['keywords'],
                                                               'setup':test['setup'] if 'setup' in test else None,
                                                               'call':test['call'] if 'call' in test else None,
                                                               'teardown':test['teardown'] if 'teardown' in test else None,
                                                               'failure_information':grabFailureInfo(test),
                                                               } for test in data['tests'] if 'test_algorithm' in test['nodeid']},
            "chip_number": data["chip_number"],
            "branch": data['branch'],
            'commit_hash': data['commit_hash'],
            'remote_url': data['remote_url'],
            'FPGA-hexa-IP': data['FPGA-hexa-IP'],
            'status': data['status'],
            'firmware_name': data['firmware_name'],
            'firmware_git_desc': data['firmware_git_desc'],
            'filename': fname,
            'ECON_type':(fname.split("report"))[1].split("_")[1],
            'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
        }
        mydatabase['testAlgorithmInfo'].insert_one(testalgorithm_info)
    except Exception as e:
        testalgorithm_info = {
            'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {
                                                               'outcome': test['outcome'],
                                                               'keywords': test['keywords'],
                                                               'setup':test['setup'] if 'setup' in test else None,
                                                               'call':test['call'] if 'call' in test else None,
                                                               'teardown':test['teardown'] if 'teardown' in test else None,
                                                               'failure_information':grabFailureInfo(test),
                                                               } for test in data['tests'] if 'test_algorithm' in test['nodeid']},
            "chip_number": data["chip_number"],
            "branch": data['branch'],
            'commit_hash': data['commit_hash'],
            'remote_url': data['remote_url'],
            'FPGA-hexa-IP': data['FPGA-hexa-IP'],
            'status': data['status'],
            'firmware_name': data['firmware_name'],
            'firmware_git_desc': data['firmware_git_desc'],
            'filename': fname,
            'ECON_type':(fname.split("report"))[1].split("_")[1],
            'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
        }
        mydatabase['testAlgorithmInfo'].insert_one(testalgorithm_info)
        print(f'trouble uploading: {e} removing metadata but keeping failure information')
    testpackets_info = {
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_packets' in test['nodeid']},
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
    }
    testpll_info = {
        'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_pll' in test['nodeid']},
        "chip_number": data["chip_number"],
        "branch": data['branch'],
        'commit_hash': data['commit_hash'],
        'remote_url': data['remote_url'],
        'FPGA-hexa-IP': data['FPGA-hexa-IP'],
        'status': data['status'],
        'firmware_name': data['firmware_name'],
        'firmware_git_desc': data['firmware_git_desc'],
        'filename': fname,
        'ECON_type':(fname.split("report"))[1].split("_")[1],
        'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
    }
    try:
        test_OBerror_info = {
            'test_info':{f"{stringReplace(test['nodeid'].split('::')[1])}": {'metadata':test['metadata'] if 'metadata' in test else None,
                                                           'outcome': test['outcome'],
                                                           'keywords': test['keywords'],
                                                           'setup':test['setup'] if 'setup' in test else None,
                                                           'call':test['call'] if 'call' in test else None,
                                                           'teardown':test['teardown'] if 'teardown' in test else None,
                                                           'failure_information':grabFailureInfo(test),
                                                           } for test in data['tests'] if 'test_obsram_voltages_fastscan' in test['nodeid']},
            "chip_number": data["chip_number"],
            "branch": data['branch'],
            'commit_hash': data['commit_hash'],
            'remote_url': data['remote_url'],
            'FPGA-hexa-IP': data['FPGA-hexa-IP'],
            'status': data['status'],
            'firmware_name': data['firmware_name'],
            'firmware_git_desc': data['firmware_git_desc'],
            'filename': fname,
            'ECON_type':(fname.split("report"))[1].split("_")[1],
            'Timestamp':datetime.strptime((fname.split('/')[-1].split('chip')[-1].split('_')[-2] + ' '+fname.split('/')[-1].split('chip')[-1].split('_')[-1].split('.')[0]), "%Y-%m-%d %H-%M-%S"),
        }
        mydatabase['testOBError'].insert_one(test_OBerror_info)
    except Exception as e:
        print(f'{e}, no OB error test available')
    ## Insert File into the DB 
    mydatabase['NonTestingInfo'].insert_one(non_testing_info)
    mydatabase['testI2CInfo'].insert_one(i2c_info)
    mydatabase['TestSummary'].insert_one(testingSummary)
    mydatabase['testPowerInfo'].insert_one(power_info)
    mydatabase['testFCInfo'].insert_one(testfc_info)
    mydatabase['testIOInfo'].insert_one(testio_info)
    mydatabase['testBistInfo'].insert_one(testbist_info)
    mydatabase['testCommonModeInfo'].insert_one(testcommonmode_info)
    mydatabase['testErrInInfo'].insert_one(testerrin_info)
    mydatabase['testInputAlignerInfo'].insert_one(testinputaligner_info)
    mydatabase['testResetRequestInfo'].insert_one(testresetrequest_info)
    mydatabase['testSerializerInfo'].insert_one(testserializer_info) 
    mydatabase['testPacketsInfo'].insert_one(testpackets_info)
    mydatabase['testPLLInfo'].insert_one(testpll_info)
    
    
