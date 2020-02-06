__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Martindale, Nathan", "Smith, Steven",
               "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"

import os
import glob
import pandas as pd

def createList(data, family_id, class_id):
    temp_master_data = []
    temp_master_data.append(data[1][0])             # Operation
    temp_master_data.append(int(data[1][1], 16))    # Sequence Number
    h, m, s, f = data[1][2].split(':')              # Pre operation time
    pre_operation_time = int(h) * 3600 + int(m) * 60 + int(s) + int(f) / 1000
    temp_master_data.append(pre_operation_time)
    h, m, s, f = data[1][3].split(':')              # Pre operation time
    post_operation_time = int(h) * 3600 + int(m) * 60 + int(s) + int(f) / 1000
    temp_master_data.append(post_operation_time)
    temp_master_data.append(post_operation_time - pre_operation_time)   # operation_elapsed
    process_id, thread_id = str(data[1][4]).split('.')  # dataset has process_id.thread_id as float
    temp_master_data.append(int(process_id))    # process id
    temp_master_data.append(int(thread_id))     # thread id
    temp_master_data.append(int(data[1][5]))    # parent id
    temp_master_data.append(data[1][6])         # process name
    temp_master_data.append(data[1][7])         # major operation type
    try:
        data[1][8] = str(data[1][8]).split(' ')[0]      # IRP flag | Conversion in int from hex
        temp_master_data.append(int(data[1][8], 16))    
    except:
        temp_master_data.append(data[1][8])
    
    try:
        data[1][9] = str(data[1][9]).split(' ')[0]      # device object | Conversion in int from hex
        temp_master_data.append(int(data[1][9], 16))    
    except:
        temp_master_data.append(data[1][9])
    
    try:
        data[1][10] = str(data[1][10]).split(' ')[0]      # File object | Conversion in int from hex
        temp_master_data.append(int(data[1][10], 16))    
    except:
        temp_master_data.append(data[1][10])
        
    try:
        data[1][11] = str(data[1][11]).split(' ')[0]      # Trnx | Conversion in int from hex
        temp_master_data.append(int(data[1][11], 16))    
    except:
        temp_master_data.append(data[1][11])
            
    try:
        data[1][12] = str(data[1][12]).split(' ')[0]      # Status | Conversion in int from hex
        temp_master_data.append(int(data[1][12], 16))    
    except:
        temp_master_data.append(data[1][12])   
        
    temp_master_data.append(data[1][13])                    # Inform | Conversion in int from hex
             
    try:
        data[1][14] = str(data[1][14]).split(' ')[0]      # Argument 1 | Conversion in int from hex
        temp_master_data.append(int(data[1][14], 16))    
    except:
        temp_master_data.append(data[1][14])
        
    try:
        data[1][15] = str(data[1][15]).split(' ')[0]      # Argument 2 | Conversion in int from hex
        temp_master_data.append(int(data[1][15], 16))    
    except:
        temp_master_data.append(data[1][15])
        
    try:
        data[1][16] = str(data[1][16]).split(' ')[0]      # Argument 3 | Conversion in int from hex
        temp_master_data.append(int(data[1][16], 16))    
    except:
        temp_master_data.append(data[1][16])
        
    try:
        data[1][17] = str(data[1][17]).split(' ')[0]      # Argument 4 | Conversion in int from hex
        temp_master_data.append(int(data[1][17], 16))    
    except:
        temp_master_data.append(data[1][17])
        
    try:
        data[1][18] = str(data[1][18]).split(' ')[0]      # Argument 5 | Conversion in int from hex
        temp_master_data.append(int(data[1][18], 16))    
    except:
        temp_master_data.append(data[1][18])
        
    try:
        data[1][19] = str(data[1][19]).split(' ')[0]      # Argument 6 | Conversion in int from hex
        temp_master_data.append(int(data[1][19], 16))    
    except:
        temp_master_data.append(data[1][19])
        
    temp_master_data.append(data[1][20])                # buffer length
    temp_master_data.append(data[1][21])                # entropy
    temp_master_data.append(data[1][22])                # file name
    temp_master_data.append(family_id)                  # Family ID
    temp_master_data.append(class_id)                   # Class ID | 0 for benign and 1 for malicious
    
    return temp_master_data
    

# Scanning all the file names
os.chdir("Dataset/benign-irp-logs/1447319093")
all_filenames = [i for i in glob.glob('*')]
all_filenames = sorted(all_filenames)

# Initializing the dataframe to accumulate and process the datasets
class_val = 0    # 0 for benign and 1 for malicious
family_id = 0    # 0 for benign and >= 1 for malicious
# The following are the column names to be used for the processed dataset
column_names =  [
                    "operation", #categorical / string
                    "sequence_number", #hex / string -> int
                    "pre_operation_time", "post_operation_time", #timestamp -> float
                    "operation_elapsed", #float
                    "process_id", "thread_id", "parent_id", #numerical
                    "process_name", #string
                    "major_operation_type", #categorical / string
                    "irp_flag", "device_object", "file_object", "transaction", "status", "inform", #hex / string -> int
                    "arg1", "arg2", "arg3", "arg4", "arg5", "arg6", # hex / string -> int
                    "buffer_length", "entropy", #numerical
                    "file_name", #string
                    "family_id", #numerical / multiclass
                    "class" #binary
                ]

for i in range(10,15):
    
    # Dataframe for processed dataset
    master_data = pd.DataFrame(columns=column_names)

    # Importing the dataset
    dataset = pd.read_csv(all_filenames[i], sep = '\t')
    dataset = dataset.rename(columns={x:y for x,y in zip(dataset.columns,range(0,len(dataset.columns)))})    # Remaining column names w/ numerics
    print(dataset.head())
    
    localPrintFlag = 1 # Just a flag to visualize the progress of the following loop
    
    # Loop to iterate through the imported dataset row wise and populate the dataframe
    for data in dataset.iterrows():
        temp_master_data = createList(data, family_id, class_val) # Processed row for the dataframe
        master_data = master_data.append(pd.Series(temp_master_data, index = column_names), ignore_index=True)
        
        # Just for visualization
        print (i, localPrintFlag)
        localPrintFlag = localPrintFlag + 1
    
    # Printing the dataframe
    print(master_data.head())
    # Convert the data into csv
    pd.DataFrame(master_data).to_csv(all_filenames[i] + '_processed.csv') 