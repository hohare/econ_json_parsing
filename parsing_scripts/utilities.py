import numpy as np

def get_timestamp_from_filename(filename, econType="ECOND"):
    """Convert a string containing a timestamp to a numpy timestamp"""
    date_time = filename[filename.find(econType)+6:].replace('.json','').replace("_"," ")
    date_time = date_time[:9] + date_time[9:].replace("-",":")
    return np.datetime64(date_time, )

def get_timestamp(timestamp):
    return np.datetime64(timestamp[:timestamp.find(":")+3])


def get_COB(filename):
    #start = filename[filename.find("COB"):]
    #end = filename[filename.find("ECOND"):]
    return filename[filename.find("COB"):].replace('.csv','')

