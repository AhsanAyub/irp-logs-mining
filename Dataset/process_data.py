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
import numpy as np

def createList(data, family_id, class_id):
    
    temp_master_data = []
    
    # Operation
    data[1][0] = data[1][0].strip()
    if (data[1][0] == "IRP" or data[1][0] == "irp"):
        temp_master_data.append(1)
        temp_master_data.append(0)
        temp_master_data.append(0)
    
    elif (data[1][0] == "FSF" or data[1][0] == "fsf"):
        temp_master_data.append(0)
        temp_master_data.append(1)
        temp_master_data.append(0)
        
    elif (data[1][0] == "FIO" or data[1][0] == "fio"):
        temp_master_data.append(0)
        temp_master_data.append(0)
        temp_master_data.append(1)
    
    else:
        temp_master_data.append(0)
        temp_master_data.append(0)
        temp_master_data.append(0)
        
    temp_master_data.append(int((data[1][1].strip()), 16))              # Sequence Number
    
    data[1][2] = data[1][2].strip()
    h, m, s, f = data[1][2].split(':')                                  # Pre operation time
    pre_operation_time = int(h) * 3600 + int(m) * 60 + int(s) + int(f) / 1000
    temp_master_data.append(pre_operation_time)
    
    data[1][3] = data[1][3].strip()
    h, m, s, f = data[1][3].split(':')                                  # Pre operation time
    post_operation_time = int(h) * 3600 + int(m) * 60 + int(s) + int(f) / 1000
    temp_master_data.append(post_operation_time)
    
    temp_master_data.append(post_operation_time - pre_operation_time)   # operation_elapsed
    
    process_id, thread_id = str(data[1][4]).split('.')                  # dataset has process_id.thread_id as float
    temp_master_data.append(int(process_id))                            # process id
    temp_master_data.append(int(thread_id))                             # thread id

    temp_master_data.append(int((data[1][5])))                          # parent id
    
    try:
        temp_master_data.append(data[1][6].strip())                     # process name
    except:
        temp_master_data.append(data[1][6])                             # process name; probably will execute for nan
    
    try:
        temp_master_data.append(data[1][7].strip())                     # major operation type
    except:
        temp_master_data.append(data[1][7])                             # major operation type; probably will execute for nan
    
    try:
        temp_master_data.append(data[1][8].strip())                     # minor operation type
    except:
        temp_master_data.append(data[1][8])                             # minor operation type; probably will execute for nan
    
    try:
        '''
            Definition of IRP Flag:
            fprintf( File, "\t0x%08lx ", RecordData->IrpFlags );
            fprintf( File, "%s", (RecordData->IrpFlags & IRP_NOCACHE) ? "N":"-" );
            fprintf( File, "%s", (RecordData->IrpFlags & IRP_PAGING_IO) ? "P":"-" );
            fprintf( File, "%s", (RecordData->IrpFlags & IRP_SYNCHRONOUS_API) ? "S":"-" );
            fprintf( File, "%s", (RecordData->IrpFlags & IRP_SYNCHRONOUS_PAGING_IO) ? "Y":"-" );
        '''
        
        data[1][9] = data[1][9].strip()
        irp_flag_hex = str(data[1][9]).split(' ')[0]                      # IRP flag | Conversion to int from hex
        temp_master_data.append(int(irp_flag_hex, 16))
        
        irp_flag_index = str(data[1][9]).split(' ')[1]
        
        if (len(irp_flag_index)) == 4:
            if(irp_flag_index[0] == 'N'):
                temp_master_data.append(1)
            else:
                temp_master_data.append(0)
                
            if(irp_flag_index[1] == 'P'):
                temp_master_data.append(1)
            else:
                temp_master_data.append(0)
                
            if(irp_flag_index[2] == 'S'):
                temp_master_data.append(1)
            else:
                temp_master_data.append(0)
                
            if(irp_flag_index[3] == 'Y'):
                temp_master_data.append(1)
            else:
                temp_master_data.append(0)
        
        else:
            temp_master_data.append(0)
            temp_master_data.append(0)
            temp_master_data.append(0)
            temp_master_data.append(0)
        
    except:
        temp_master_data.append(np.nan)
        temp_master_data.append(0)
        temp_master_data.append(0)
        temp_master_data.append(0)
        temp_master_data.append(0)
    
    try:
        data[1][10] = data[1][10].strip()                                   # device object | Conversion to int from hex
        temp_master_data.append(int(data[1][10], 16))    
    except:
        temp_master_data.append(np.nan)
    
    try:
        data[1][11] = data[1][11].strip()                                   # File object | Conversion to int from hex
        temp_master_data.append(int(data[1][11], 16))
    except:
        temp_master_data.append(np.nan)
        
    try:
        data[1][12] = data[1][12].strip()                                   # Trnx | Conversion to int from hex
        temp_master_data.append(int(data[1][12], 16))    
    except:
        temp_master_data.append(np.nan)
            
    try:
        '''
        Definition:
            fprintf( File, "\t0x%08lx:0x%p", RecordData->Status, (PVOID)RecordData->Information );
        '''
        data[1][13] = data[1][13].strip()
        status = str(data[1][13]).split(':')[0]                             # Status | Conversion to int from hex
        temp_master_data.append(int(status, 16))
        information = str(data[1][13]).split(':')[1]                        # Inform | Conversion to int from hex
        temp_master_data.append(int(information, 16))
        
    except:
        temp_master_data.append(np.nan)
        temp_master_data.append(np.nan)

             
    try:
        data[1][14] = data[1][14].strip()                                   # Argument 1 | Conversion to int from hex
        temp_master_data.append(int(data[1][14], 16))    
    except:
        temp_master_data.append(np.nan)
        
    try:
        data[1][15] = data[1][15].strip()                                   # Argument 2 | Conversion to int from hex
        temp_master_data.append(int(data[1][15], 16))    
    except:
        temp_master_data.append(np.nan)
        
    try:
        data[1][16] = data[1][16].strip()                                   # Argument 3 | Conversion to int from hex
        temp_master_data.append(int(data[1][16], 16))    
    except:
        temp_master_data.append(np.nan)
        
    try:
        data[1][17] = data[1][17].strip()                                   # Argument 4 | Conversion to int from hex
        temp_master_data.append(int(data[1][17], 16))    
    except:
        temp_master_data.append(np.nan)
        
    try:
        data[1][18] = data[1][18].strip()                                   # Argument 5 | Conversion to int from hex
        temp_master_data.append(int(data[1][18], 16))    
    except:
        temp_master_data.append(np.nan)
        
    try:
        data[1][19] = data[1][19].strip()                                   # Argument 6 | Conversion to int from hex
        temp_master_data.append(int(data[1][19], 16))    
    except:
        temp_master_data.append(np.nan)
        
    temp_master_data.append(data[1][20])                                    # buffer length
    temp_master_data.append(data[1][21])                                    # entropy
    temp_master_data.append(data[1][22])                                    # file name
    temp_master_data.append(family_id)                                      # Family ID
    temp_master_data.append(class_id)                                       # Class ID | 0 for benign and 1 for malicious
    
    return temp_master_data
    

# Scanning all the file names
os.chdir("research/irp-logs-mining/Dataset/benign-irp-logs/machine_7")
all_filenames = [i for i in glob.glob('*')]
all_filenames = sorted(all_filenames)

# Initializing the dataframe to accumulate and process the datasets
class_val = 0    # 0 for benign and 1 for malicious
family_id = 0    # 0 for benign and >= 1 for malicious
# The following are the column names to be used for the processed dataset
column_names =  [
                    "operation_irp", "operation_fsf", "operation_fio", #categorical / string -> int as flags
                    "sequence_number", #hex / string -> int
                    "pre_operation_time", "post_operation_time", #timestamp -> float
                    "operation_elapsed", #float
                    "process_id", "thread_id", "parent_id", #numerical
                    "process_name", #string
                    "major_operation_type", "minor_operation_type", #categorical / string
                    "irp_flag", #hex / string -> int
                    "irp_nocache", "irp_paging_io", "irp_synchoronous_api", "irp_synchoronous_paging_io", #flag values
                    "device_object", "file_object", "transaction", "status", "inform", #hex / string -> int
                    "arg1", "arg2", "arg3", "arg4", "arg5", "arg6", # hex / string -> int
                    "buffer_length", "entropy", #numerical
                    "file_name", #string
                    "family_id", #numerical / multiclass
                    "class" #binary
                ]


for file_name in all_filenames:

	#file_name = "../../1b95ab402c44763b5f91fd976090e1d67759c7e0b7ff3a7974a1e5a5e26ac4a3"

	# Dataframe for processed dataset
	master_data = pd.DataFrame(columns=column_names)

	# Importing the dataset
	dataset = pd.read_csv(file_name, sep = '\t')
	dataset = dataset.drop(dataset.index[0])
	dataset = dataset.rename(columns={x:y for x,y in zip(dataset.columns,range(0,len(dataset.columns)))})    # Remaining column names w/ numerics
	print(dataset.head())
	    
	#localPrintFlag = 1 # Just a flag to visualize the progress of the following loop

	# Loop to iterate through the imported dataset row wise and populate the dataframe
	for data in dataset.iterrows():
	    temp_master_data = createList(data, family_id, class_val) # Processed row for the dataframe
	    master_data = master_data.append(pd.Series(temp_master_data, index = column_names), ignore_index=True)
	        
	    # Just for visualization
	    #print (localPrintFlag)
	    #localPrintFlag = localPrintFlag + 1
	    
	# Printing the dataframe
	print(master_data.head())
	# Convert the data into csv
	pd.DataFrame(master_data).to_csv(file_name + '_processed.csv')