__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Martindale, Nathan", "Smith, Steven",
               "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"

import IRP_Code_Definations as irpCodeDefination
from collections import Counter 

# Importing the libraries
import pandas as pd

'''
Defination of the processed dataframe
    process_id - ID of the process (First out of two keys for grouping)
    process_name - Name of the process (Sewcond out of two key for grouping)    
    numIRP - Total count of IRPs
    numFSO - Total count of FSOs
    numFIO - Total count of FIOs
    numSeqNo - Number of unique Sequence Numbers / Indicative of the number of records
    totalTimeElapsed - Sum of operation_elapsed
    pre_operation_time - First reported pre_operation_time
    post_operation_time - Final reported post_operation_time
    totalOperationalTimeElapsed - Substraction of the final reported post_operation_time from the first reported pre_operation_time
    numThreadID - Number of unique Thread IDs
    parent_id - Parent ID of the tuple <processID, processName>
    numMajorOperationTypes - Number of unique Major Operation Types
    major_opration_type_types_seq_items - Sequence of major_operation_types items
    numMinorOperationTypes - Number of unique Minor Operation Types
    minor_opration_type_types_seq_items - Sequence of minor_operation_types items
    numIRPFlag - Number of unique IRP Flags
    numIRP_nocache - Number of unique irp_nocache
    numIRP_paging_io - Number of unique irp_paging_io
    numIRP_synchoronous_api - Number of unique irp_synchoronous_api
    numIRP_synchoronous_paging_io - Number of unique irp_synchoronous_paging_io
    numDeviceObject - Number of unique Device Objects
    numFileObject - Number of unique File Objects
    numTransaction - Number of unique Transaction
    numStatus - Number of unique Status
    status_seq_items - Sequence of status items
    numInform - Number of unique Inform
    numArg1 - Number of unique arg1
    numArg2 - Number of unique arg2
    numArg3 - Number of unique arg3
    numArg4 - Number of unique arg4
    numArg5 - Number of unique arg5
    numArg6 - Number of unique arg6
    numBufferLength - Number of unique buffer_length
    sumBufferLength - Summation of all the appeared items in buffer_length
    meanBufferLength - Mean of all the appeared items in buffer_length
    maxBufferLength - Max value fom all the appeared items in buffer_length
    minBufferLength - Min value fom all the appeared items in buffer_length
    stdBufferLength - Standard Deviation of all the appeared items in buffer_length
    numEntropy - Number of unique entropy
    sumEntropy - Summation of all the appeared items in entropy
    meanEntropy - Mean of all the appeared items in entropy
    maxEntropy - Max value fom all the appeared items in entropy
    minEntropy - Min value fom all the appeared items in entropy
    stdEntropy - Standard Deviation of all the appeared items in entropy
    file_name_seq_items - Sequence of file_names items
    numFileName - Number of unique File Names
    totalFileName - Size of the all the accessed files 
    doc_files_count - Number of files' interaction in documents folder
    family_id - Family ID of the Ransomware Family
    class - Benign and ransomware process would be denoted as 0 and 1 respectively
'''

# Return the count of the number of times the files are accessed in the Document or Doc Files folder
def number_of_doc_files_accessed(file_names):
    doc_files_count = 0
    
    if(len(file_names) > 0):    
        for file_name in file_names:
            file_name = str(file_name)
            if(file_name.find("Doc file") != -1 or (file_name.find("Documents") != -1)):
                doc_files_count += 1
            else:
                continue
    
    return doc_files_count

# Flag if the doc_files_count is more than the mean value
def doc_files_count_flag(val, mean):
    return (val >= mean) if 1 else 0

# Return the dataframe aggregated from the dataset grouped with process id and process name
def aggegateData(dataset):
    processDataList = []
    groupedData = dataset.groupby(['process_id', 'process_name'])
    for item in groupedData:
        temp = []    
        temp.append(item[0][0]) # process_id
        temp.append(item[0][1]) # process_name
        temp.append(Counter(item[1]['operation_irp'])[1])           # numIRP
        temp.append(Counter(item[1]['operation_fsf'])[1])           # numFSO
        temp.append(Counter(item[1]['operation_fio'])[1])           # numFIO
        temp.append(item[1]['sequence_number'].unique().size)       # numSeqNo
        temp.append(item[1]['operation_elapsed'].sum())             # totalTimeElapsed
        temp.append(item[1]['pre_operation_time'].min())            # pre_operation_time
        temp.append(item[1]['post_operation_time'].max())           # post_operation_time
        temp.append(item[1]['post_operation_time'].max() - 
                    item[1]['pre_operation_time'].min())            # totalOperationalTimeElapsed
        temp.append(item[1]['thread_id'].unique().size)             # numThreadID
        temp.append(item[1]['parent_id'].unique()[0])               # parent_id
        temp.append(item[1]['major_operation_type'].unique().size)  # numMajorOperationTypes
        temp.append([irpCodeDefination.getMajorOperationCode(key)
                    for key in item[1]['major_operation_type']])    # major_opration_type_types_seq_items
        temp.append(item[1]['minor_operation_type'].unique().size)  # numMinorOperationTypes
        temp.append([irpCodeDefination.getMinorOperationCode(key)
                    for key in item[1]['minor_operation_type']])    # minor_opration_type_types_seq_items
        temp.append(item[1]['irp_flag'].unique().size)              # numIRPFlag
        temp.append(Counter(item[1]['irp_nocache'])[1])             # numIRP_nocache
        temp.append(Counter(item[1]['irp_paging_io'])[1])           # numIRP_paging_io
        temp.append(Counter(item[1]['irp_synchoronous_api'])[1])    # numIRP_synchoronous_api
        temp.append(Counter(item[1]['irp_synchoronous_paging_io'])[1])    # numIRP_synchoronous_paging_io
        temp.append(item[1]['device_object'].unique().size)         # numDeviceObject
        temp.append(item[1]['file_object'].unique().size)           # numFileObject
        temp.append(item[1]['transaction'].unique().size)           # numTransaction
        temp.append(item[1]['status'].unique().size)                # numStatus
        temp.append(item[1]['status'].tolist())                     # status_seq_items
        temp.append(item[1]['inform'].unique().size)                # numInform
        temp.append(item[1]['arg1'].unique().size)                  # numArg1
        temp.append(item[1]['arg2'].unique().size)                  # numArg2
        temp.append(item[1]['arg3'].unique().size)                  # numArg3
        temp.append(item[1]['arg4'].unique().size)                  # numArg4
        temp.append(item[1]['arg5'].unique().size)                  # numArg5
        temp.append(item[1]['arg6'].unique().size)                  # numArg6
        temp.append(item[1]['buffer_length'].unique().size)         # numBufferLength
        temp.append(item[1]['buffer_length'].sum())                 # sumBufferLength
        temp.append(item[1]['buffer_length'].mean())                # meanBufferLength
        temp.append(item[1]['buffer_length'].max())                 # maxBufferLength
        temp.append(item[1]['buffer_length'].min())                 # minBufferLength
        temp.append(item[1]['buffer_length'].std())                 # stdBufferLength
        temp.append(item[1]['entropy'].unique().size)               # numEntropy
        temp.append(item[1]['entropy'].sum())                       # sumEntropy
        temp.append(item[1]['entropy'].mean())                      # meanEntropy
        temp.append(item[1]['entropy'].max())                       # maxEntropy
        temp.append(item[1]['entropy'].min())                       # minEntropy
        temp.append(item[1]['entropy'].std())                       # stdEntropy
        temp.append(item[1]['file_name'].tolist())                  # file_name_seq_items
        temp.append(item[1]['file_name'].unique().size)             # numFileName
        temp.append(len(item[1]['file_name']))                      # totalFileName
        temp.append(number_of_doc_files_accessed(item[1]['file_name'].tolist()))     # doc_files_count
        temp.append(0)                                              # doc_files_flag
        temp.append(0)                                              # family_id
        temp.append(0)                                              # class
        processDataList.append(temp)
    
    cols = ['process_id', 'process_name', 'numIRP', 'numFSO', 'numFIO', 'numSeqNo',
            'totalTimeElapsed', 'pre_operation_time', 'post_operation_time',
            'totalOperationalTimeElapsed', 'numThreadID', 'parent_id',
            'numMajorOperationTypes', 'major_opration_type_types_seq_items',
            'numMinorOperationTypes', 'minor_opration_type_types_seq_items',
            'numIRPFlag', 'numIRP_nocache',  'numIRP_paging_io', 'numIRP_synchoronous_api',
            'numIRP_synchoronous_paging_io', 'numDeviceObject', 'numFileObject',
            'numTransaction', 'numStatus', 'status_seq_items', 'numInform', 'numArg1',
            'numArg2', 'numArg3', 'numArg4', 'numArg5', 'numArg6', 'numBufferLength',
            'sumBufferLength', 'meanBufferLength', 'maxBufferLength', 'minBufferLength',
            'stdBufferLength', 'numEntropy', 'sumEntropy', 'meanEntropy', 'maxEntropy',
            'minEntropy', 'stdEntropy', 'file_name_seq_items', 'numFileName',
            'totalFileName', 'doc_files_count', 'doc_files_flag', 'family_id', 'class']
    
    processed_data = pd.DataFrame(processDataList, columns = cols)
    del processDataList
    doc_files_count_mean = round(processed_data['doc_files_count'].mean())
    processed_data['doc_files_flag'] = [doc_files_count_flag(doc_files_count,doc_files_count_mean)
                                        for doc_files_count in processed_data['doc_files_count']]
    return processed_data