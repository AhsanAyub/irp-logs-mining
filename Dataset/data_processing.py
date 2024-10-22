__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Martindale, Nathan", "Smith, Steven",
               "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"

# Importing libraries
import os
import glob
import pandas as pd
import numpy as np
from datetime import datetime
import aggregator as aggregator
    

'''# Scanning all the file names
os.chdir("research/irp-logs-mining/Dataset/benign-irp-logs/machine_7")
all_filenames = [i for i in glob.glob('*')]
all_filenames = sorted(all_filenames)'''

# NPSY flags
def generateStringForIRPFlags(x):
    val = "0:0:0:0"
    if(len(x) != 4):
        return val
    else:
        if(x[0] != '-'): # N flag
            val = '1:'
        else:
            val = '0:'
            
        if(x[1] != '-'): # P flag
            val += '1:'
        else:
            val += '0:'
            
        if(x[2] != '-'): # S flag
            val += '1:'
        else:
            val += '0:'
            
        if(x[3] != '-'): # Y flag
            val += '1'
        else:
            val += '0'
        
        return val


def main(raw_dataset):
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
    
    raw_dataset = raw_dataset.drop(raw_dataset.index[0]) # Removing the first row    
    raw_dataset.columns = raw_dataset.columns.str.strip()
    
    # Operation Type
    raw_dataset['Opr'] = raw_dataset['Opr'].str.strip()
    raw_dataset = raw_dataset.drop(raw_dataset[(raw_dataset['Opr'] != 'IRP') & (raw_dataset['Opr'] != 'FSF') & (raw_dataset['Opr'] != 'FIO')].index)
    
    # OneHotEncoding and then concat for operation
    one_hot = pd.get_dummies(raw_dataset.Opr, prefix='operation')
    raw_dataset = raw_dataset.drop('Opr', axis=1)
    raw_dataset = one_hot.join(raw_dataset)
    del one_hot
    
    # Sequence Number
    raw_dataset['SeqNum'] = raw_dataset['SeqNum'].str.strip()
    
    # Pre Operation Time
    raw_dataset['PreOp Time'] = raw_dataset['PreOp Time'].str.strip()
    raw_dataset['PreOp Time'] = [datetime.strptime(i, "%H:%M:%S:%f").strftime("%H:%M:%S.%f") for i in raw_dataset['PreOp Time']]
    raw_dataset['PreOp Time'] = pd.to_timedelta(raw_dataset['PreOp Time']).dt.total_seconds()
    
    # Post Operation Time
    raw_dataset['PostOp Time'] = raw_dataset['PostOp Time'].str.strip()
    raw_dataset['PostOp Time'] = [datetime.strptime(i, "%H:%M:%S:%f").strftime("%H:%M:%S.%f") for i in raw_dataset['PostOp Time']]
    raw_dataset['PostOp Time'] = pd.to_timedelta(raw_dataset['PostOp Time']).dt.total_seconds()
    
    # Operation Elapsed
    raw_dataset['operation_elapsed'] = raw_dataset['PostOp Time'] - raw_dataset['PreOp Time']
    
    # Parent ID
    raw_dataset['PPID'] = raw_dataset['PPID'].apply(str)
    raw_dataset['PPID'] = raw_dataset['PPID'].str.strip()
    raw_dataset['PPID'] = raw_dataset['PPID'].fillna(np.NaN) # Missing Value
    raw_dataset['PPID'] = raw_dataset['PPID'].str.replace('None', '-1') # nan and -1 does not represent anything
    try:
        raw_dataset['parent_id'] = raw_dataset['PPID'].astype('int32')
    except:
        raw_dataset['parent_id'] = raw_dataset['PPID'].astype(float)
        raw_dataset['parent_id'] = raw_dataset['parent_id'].astype('int32')
    raw_dataset = raw_dataset.drop('PPID', axis=1)
    
    # Process ID and Thread ID
    raw_dataset['Process.Thrd'] = raw_dataset['Process.Thrd'].apply(str)
    raw_dataset['Process.Thrd'] = raw_dataset['Process.Thrd'].str.strip()
    raw_dataset[['process_id', 'thread_id']] = raw_dataset['Process.Thrd'].str.split('.',expand=True)
    raw_dataset = raw_dataset.drop('Process.Thrd', axis=1)
    
    raw_dataset['process_id'] = raw_dataset['process_id'].fillna(np.NaN) # Missing Value
    raw_dataset['process_id'] = raw_dataset['process_id'].str.replace('None', '-1') # nan and -1 does not represent anything
    raw_dataset['process_id'] = raw_dataset['process_id'].astype('int32')
    
    raw_dataset['thread_id'] = raw_dataset['thread_id'].fillna(np.NaN) # Missing Value
    raw_dataset['thread_id'] = raw_dataset['thread_id'].str.replace('None', '-1') # nan and -1 does not represent anything
    raw_dataset['thread_id'] = raw_dataset['thread_id'].astype('int32')
    
    # Process Name
    raw_dataset['Process Name'] = raw_dataset['Process Name'].str.strip()
    
    # Major Operation
    raw_dataset['Major Operation'] = raw_dataset['Major Operation'].str.strip()
    raw_dataset['Major Operation'] = raw_dataset['Major Operation'].fillna(np.NaN) # Missing Value
    
    # Minor Operation
    raw_dataset['Minor Operation'] = raw_dataset['Minor Operation'].str.strip()
    raw_dataset['Minor Operation'] = raw_dataset['Minor Operation'].fillna(np.NaN) # Missing Value
    
    # IRP Flags
    raw_dataset['IrpFlags'] = raw_dataset['IrpFlags'].str.strip()
    raw_dataset[['irp_flag', 'temp']] = raw_dataset['IrpFlags'].str.split(' ',expand=True)
    raw_dataset['irp_flag'] = raw_dataset['irp_flag'].apply(str)
    raw_dataset['irp_flag'] = raw_dataset['irp_flag'].fillna(np.NaN) # Missing Value
    raw_dataset['irp_flag'] = raw_dataset['irp_flag'].str.replace('nan', '-0x1') # nan and -1 does not represent anything
    raw_dataset['irp_flag'] = raw_dataset['irp_flag'].str.replace('None', '-0x1') # None and -1 does not represent anything
    raw_dataset['irp_flag'] = raw_dataset['irp_flag'].apply(int, base=16)
    
    # Four Distinct IRP Flags - NPSY
    raw_dataset['temp'] = raw_dataset['temp'].apply(str)
    raw_dataset[["irp_nocache", "irp_paging_io", "irp_synchoronous_api",
                 "irp_synchoronous_paging_io"]] = raw_dataset['temp'].apply(lambda x : generateStringForIRPFlags(x)).str.split(':',expand=True)
    raw_dataset = raw_dataset.drop(['temp', 'IrpFlags'], axis=1)
    
    # Device Objects
    raw_dataset['DevObj'] = raw_dataset['DevObj'].str.strip()
    raw_dataset['DevObj'] = raw_dataset['DevObj'].fillna(np.NaN) # Missing Value
    
    # File Objects
    raw_dataset['FileObj'] = raw_dataset['FileObj'].str.strip()
    raw_dataset['FileObj'] = raw_dataset['FileObj'].fillna(np.NaN) # Missing Value
    
    # Transaction
    raw_dataset['Transactn'] = raw_dataset['Transactn'].str.strip()
    raw_dataset['Transactn'] = raw_dataset['Transactn'].fillna(np.NaN) # Missing Value
    
    # Status and Inform
    raw_dataset['status:inform'] = raw_dataset['status:inform'].apply(str)
    raw_dataset['status:inform'] = raw_dataset['status:inform'].str.strip()
    raw_dataset[['status', 'inform']] = raw_dataset['status:inform'].str.split(':',expand=True)
    raw_dataset['status'] = raw_dataset['status'].fillna(np.NaN) # Missing Value
    raw_dataset['status'] = raw_dataset['status'].str.replace('None', '-0x1') # None and -1 does not represent anything
    raw_dataset['status'] = raw_dataset['status'].str.replace('nan', '-0x1') # nan and -1 does not represent anything
    raw_dataset['status'] = raw_dataset['status'].apply(int, base=16) # Convert hex to int
    raw_dataset = raw_dataset.drop('status:inform', axis=1)
    
    # Arguments
    raw_dataset['Arg 1'] = raw_dataset['Arg 1'].str.strip()
    raw_dataset['Arg 1'] = raw_dataset['Arg 1'].fillna(np.NaN) # Missing Value
    raw_dataset['Arg 2'] = raw_dataset['Arg 2'].str.strip()
    raw_dataset['Arg 2'] = raw_dataset['Arg 2'].fillna(np.NaN) # Missing Value
    raw_dataset['Arg 3'] = raw_dataset['Arg 3'].str.strip()
    raw_dataset['Arg 3'] = raw_dataset['Arg 3'].fillna(np.NaN) # Missing Value
    raw_dataset['Arg 4'] = raw_dataset['Arg 4'].str.strip()
    raw_dataset['Arg 4'] = raw_dataset['Arg 4'].fillna(np.NaN) # Missing Value
    raw_dataset['Arg 5'] = raw_dataset['Arg 5'].str.strip()
    raw_dataset['Arg 5'] = raw_dataset['Arg 5'].fillna(np.NaN) # Missing Value
    raw_dataset['Arg 6'] = raw_dataset['Arg 6'].str.strip()
    raw_dataset['Arg 6'] = raw_dataset['Arg 6'].fillna(np.NaN) # Missing Value
    
    # Buffer Length
    raw_dataset['BufferLength'] = raw_dataset['BufferLength'].apply(str)
    raw_dataset['BufferLength'] = raw_dataset['BufferLength'].str.strip()
    raw_dataset['BufferLength'] = raw_dataset['BufferLength'].fillna(np.NaN) # Missing Value
    raw_dataset['BufferLength'] = raw_dataset['BufferLength'].str.replace('None', '0') # None and 0 does not represent anything
    raw_dataset['BufferLength'] = raw_dataset['BufferLength'].str.replace('nan', '0') # nan and 0 does not represent anything'''
    raw_dataset['buffer_length'] = raw_dataset['BufferLength'].astype(float)
    raw_dataset = raw_dataset.drop('BufferLength', axis=1)
    
    # Entropy
    raw_dataset['Entropy'] = raw_dataset['Entropy'].apply(str)
    raw_dataset['Entropy'] = raw_dataset['Entropy'].str.strip()
    raw_dataset['Entropy'] = raw_dataset['Entropy'].fillna(np.NaN) # Missing Value
    raw_dataset['Entropy'] = raw_dataset['Entropy'].str.replace('None', '0') # None and 0 does not represent anything
    raw_dataset['Entropy'] = raw_dataset['Entropy'].str.replace('nan', '0') # nan and 0 does not represent anything
    raw_dataset['entropy'] = raw_dataset['Entropy'].astype(float)
    raw_dataset = raw_dataset.drop('Entropy', axis=1)
    
    # File Name
    raw_dataset['Name'] = raw_dataset['Name'].str.strip()
    raw_dataset['Name'] = raw_dataset['Name'].fillna(np.NaN) # Missing Value
    
    # Additional two columns for class and family id
    raw_dataset['class'] = 0
    raw_dataset['family_id'] = 0
    
    # Renaming column names as per defination
    raw_dataset = raw_dataset.rename(columns={  'operation_IRP' : 'operation_irp',
                                                'operation_FSF' : 'operation_fsf',
                                                'operation_FIO' : 'operation_fio',
                                                'SeqNum' : 'sequence_number',
                                                'PreOp Time' : 'pre_operation_time',
                                                'PostOp Time' : 'post_operation_time',
                                                'Process Name' : 'process_name',
                                                'Major Operation' : 'major_operation_type',
                                                'Minor Operation' : 'minor_operation_type',
                                                'DevObj' : 'device_object',
                                                'FileObj' : 'file_object',
                                                'Transactn' : 'transaction',
                                                'Arg 1' : 'arg1',
                                                'Arg 2' : 'arg2',
                                                'Arg 3' : 'arg3',
                                                'Arg 4' : 'arg4',
                                                'Arg 5' : 'arg5',
                                                'Arg 6' : 'arg6',
                                                'Name' : 'file_name' })
    
    # Returning the processed dataframe
    return raw_dataset[column_names]


if __name__ == '__main__':
    
    '''all_filenames = [i for i in glob.glob('2*')]
    all_filenames = sorted(all_filenames)
    print(all_filenames)'''
    
    
    all_given_files = [i for i in glob.glob('./ransomware-irp-logs-9/*')]
    all_given_files = sorted(all_given_files)
    all_given_files_hashes = [filename.split('/')[-1] for filename in all_given_files]
    all_given_files_hashes = [filename.split('.')[0] for filename in all_given_files_hashes]
    
    all_available_files_hashes = [i for i in glob.glob('./ransomware-irp-logs/Time_Interval_Dataset/*')]
    all_available_files_hashes = [filename.split('/')[-1] for filename in all_available_files_hashes]
    all_available_files_hashes = [filename.split('.')[0] for filename in all_available_files_hashes]
    all_available_files_hashes = sorted(all_available_files_hashes)
    
    for i in range(len(all_given_files_hashes)):
        if(all_given_files_hashes[i] in all_available_files_hashes):
            all_given_files_hashes[i] = 0
            os.remove(all_given_files[i])
            all_given_files.pop(i)
            
    # File Name for the csv file 
    #file_name = '02ef81bb120472b87d413516a8ccc8202d9e04d686ebdedbfcd963b6a9673109'
    i = 1
    
    for file_name in all_given_files:
    
    # Initialize a process dataframe
    #processed_dataset = main(pd.read_csv('../../ransomware-lrp-logs/' + str(file_name), engine='python', sep = '\t'))
    
        try:
            processed_dataset = main(pd.read_csv(str(file_name), engine='python', sep = '\t', compression='gzip'))
            print("Data processing is done.")
            
            # Generate aggregated dataframe
            processed_aggregate_dataset = aggregator.aggegateData(processed_dataset)
            print("Aggegating the processed dataset is also done.")
            
            file_name_copy = file_name
            file_name = file_name.split('/')[-1]
            file_name = file_name.split('.')[0]
            
            # Dump processed dataset
            # processed_dataset.to_csv("./ransomware-irp-logs/" + str(file_name) + "_processed.csv.gz", compression='gzip')
            processed_dataset.to_pickle("./ransomware-irp-logs/" + str(file_name) + "_processed.pkl.gz", compression='gzip')
            print("Processed dataset is dumped, shape %s" % str(processed_dataset.shape))
            
            # Dump aggregated dataframe
            processed_aggregate_dataset.to_csv("./ransomware-irp-logs/" + str(file_name) + "_processed_aggregated.csv.gz", compression='gzip')
            print("Aggregated dataset is dumped, shape %s" % str(processed_aggregate_dataset.shape))
            
            del processed_dataset, processed_aggregate_dataset
            
            os.remove(file_name_copy)
            print("%s is removed" % file_name)
            
            print(i)
            i += 1

        except:
            print(i)
            i += 1
            continue
