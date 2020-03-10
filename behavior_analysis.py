__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Martindale, Nathan", "Smith, Steven",
               "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"

# Importing the libraries
import pandas as pd
import glob
import os
import numpy as np

def identifyDominatingFeatureSpace(aggegated_dataset_flagged, aggegated_dataset_not_flagged):
    flagged_items_list = []
    non_flagged_items_list = []
    
    # IRP Operations
    flagged_items_list.append(round(aggegated_dataset_flagged.numIRP.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.numIRP.median()))
    
    flagged_items_list.append(round(aggegated_dataset_flagged.numFSO.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.numFSO.median()))
    
    flagged_items_list.append(round(aggegated_dataset_flagged.numFIO.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.numFIO.median()))
    
    # Files
    flagged_items_list.append(round(aggegated_dataset_flagged.numFileObject.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.numFileObject.median()))
    
    flagged_items_list.append(round(aggegated_dataset_flagged.numFileName.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.numFileName.median()))
    
    flagged_items_list.append(round(aggegated_dataset_flagged.totalFileName.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.totalFileName.median()))
    
    # IRP Flags
    flagged_items_list.append(round(aggegated_dataset_flagged.numIRPFlag.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.numIRPFlag.median()))
    
    flagged_items_list.append(round(aggegated_dataset_flagged.numMajorOperationTypes.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.numMajorOperationTypes.median()))
    
    # Others
    flagged_items_list.append(round(aggegated_dataset_flagged.numStatus.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.numStatus.median()))
    
    flagged_items_list.append(round(aggegated_dataset_flagged.numInform.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.numInform.median()))
    
    # Buffer and Entropy
    flagged_items_list.append(round(aggegated_dataset_flagged.meanBufferLength.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.meanBufferLength.median()))
    
    flagged_items_list.append(round(aggegated_dataset_flagged.sumEntropy.median()))
    non_flagged_items_list.append(round(aggegated_dataset_not_flagged.sumEntropy.median()))

    return flagged_items_list, non_flagged_items_list


def benign_dataset_feature_space_exploration(dataset, cols):
    temp = [0 * i for i in range(len(cols))]
    groupedData = dataset.groupby(['session'])
    
    for item in groupedData:
        # IRP Opn
        if temp[0] <= round(item[1]['numIRP'].median()):
            temp[0] = round(item[1]['numIRP'].median())
        
        # FSO Opn
        if temp[1] <= round(item[1]['numFSO'].median()):
            temp[1] = round(item[1]['numFSO'].median())
        
        # FIO Opn
        if temp[2] <= round(item[1]['numFIO'].median()):
            temp[2] = round(item[1]['numFIO'].median())
            
        # File Object
        if temp[3] <= round(item[1]['numFileObject'].median()):
            temp[3] = round(item[1]['numFileObject'].median())
            
        # Unique Files Accessed
        if temp[4] <= round(item[1]['numFileName'].median()):
            temp[4] = round(item[1]['numFileName'].median())
            
        # Total File Accessed
        if temp[5] <= round(item[1]['totalFileName'].median()):
            temp[5] = round(item[1]['totalFileName'].median())
            
        # IRP Flag
        if temp[6] <= round(item[1]['numIRPFlag'].median()):
            temp[6] = round(item[1]['numIRPFlag'].median())
            
        # Major Opn Type
        if temp[7] <= round(item[1]['numMajorOperationTypes'].median()):
            temp[7] = round(item[1]['numMajorOperationTypes'].median())
            
        # Status
        if temp[8] <= round(item[1]['numStatus'].median()):
            temp[8] = round(item[1]['numStatus'].median())
            
        # Inform
        if temp[9] <= round(item[1]['numInform'].median()):
            temp[9] = round(item[1]['numInform'].median())
            
        # Buffer Length
        if temp[10] <= round(item[1]['meanBufferLength'].median()):
            temp[10] = round(item[1]['meanBufferLength'].median())
            
        # Entropy
        if temp[11] <= round(item[1]['sumEntropy'].median()):
            temp[11] = round(item[1]['sumEntropy'].median())
            
        # Machine
        temp[12] = round(item[1]['machine'].unique()[0])
        
        # Category
        temp[13] = 0   
        
    return temp
        
if __name__ == '__main__':
    pwd = os.getcwd()
    flag = 0    # 0 for benign and 1 for ransomware
    
    if (flag == 0):    # Benign datasets' behavior analysis
        os.chdir(pwd)
        
        benign_labels = ["IRP_Opn", "FSO_Opn", "FIO_Opn", "File_Object", "Unique_Files_Accessed", "Total_File_Accessed",
                      "IRP_Flag", "Major_Opn_Type", "Status", "Inform", "Buffer_Length", "Entropy", "Machine", "Category"]
        benign_feature_space_list = []
        
        for index in range(1, 12):
            file_path = "./Dataset/benign-irp-logs/machine_" + str(index) + "/"
            os.chdir(file_path)
            
            all_filenames = [i for i in glob.glob('*_aggregated.csv')]
            all_filenames = sorted(all_filenames)
            
            total_files = len(all_filenames)
            for i in range(total_files):
                filename = all_filenames[i]
                aggregated_dataset = pd.read_csv(filename)
                aggregated_dataset = aggregated_dataset.drop(['Unnamed: 0'], axis=1)
                print(aggregated_dataset.head())
                aggregated_dataset['machine'] = index
                aggregated_dataset['session'] = i + 1
                
                aggregated_dataset = aggregated_dataset.drop(['major_opration_type_types_seq_items',
                                                              'minor_opration_type_types_seq_items',
                                                              'status_seq_items', 'file_name_seq_items'], axis=1)
                if (i > 0):
                    aggregated_dataset_append = aggregated_dataset_append.append(aggregated_dataset)
                else:
                    aggregated_dataset_append = aggregated_dataset # Copy
            
                del aggregated_dataset
            
            benign_feature_space_list.append(benign_dataset_feature_space_exploration(aggregated_dataset_append, benign_labels))
            
            del total_files
            del aggregated_dataset_append
            os.chdir(pwd)
            
        behavior_benign_feature_space = pd.DataFrame(benign_feature_space_list, columns = benign_labels)
        del benign_feature_space_list
        
        # Dump aggregated dataframe
        behavior_benign_feature_space.to_csv("./Behavior_Analysis_Results/behaviour_benign_feature_space_exploration.csv")
    
    if (flag == 1):    # Ransomware datasets' behavior analysis
        os.chdir('./Dataset/ransomware-irp-logs/')
        
        # Storing the file names for all the aggregated datasets
        all_filenames = [i for i in glob.glob('*_aggregated*')]
        all_filenames = sorted(all_filenames)
        
        # Building lists
        labels = ["IRP Opn", "FSO Opn", "FIO Opn", "File Object", "Unique Files Accessed", "Total File Accessed",
                  "IRP Flag", "Major Opn Type", "Status", "Inform", "Buffer Length", "Entropy",
                  "Process_Names", "Ransomware_Hash", "Category"]
        processAggregateList = []
        
        for filename in all_filenames:
        #filename = all_filenames[0]
            flagged_items_list = []
            non_flagged_items_list = []
            
            try:
                aggegated_dataset = pd.read_csv(filename, compression='zip', header=0, sep=',', quotechar='"')
            except:
                try:
                    aggegated_dataset = pd.read_csv(filename, compression='gzip', header=0, sep=',', quotechar='"')
                except:
                    continue
                
            aggegated_dataset = aggegated_dataset.drop(['Unnamed: 0'], axis=1)
            print(aggegated_dataset.head())
        
            # Segragating flagged and non flagged dataframes
            aggegated_dataset_not_flagged = aggegated_dataset.drop(aggegated_dataset[(aggegated_dataset['doc_files_flag'] != 0)].index)
            aggegated_dataset_flagged = aggegated_dataset.drop(aggegated_dataset[(aggegated_dataset['doc_files_flag'] != 1)].index)
        
            # Removing the list items row
            aggegated_dataset_flagged = aggegated_dataset_flagged.drop(['major_opration_type_types_seq_items',
                                                                        'minor_opration_type_types_seq_items',
                                                                        'status_seq_items', 'file_name_seq_items'], axis=1)
            
            aggegated_dataset_not_flagged = aggegated_dataset_not_flagged.drop(['major_opration_type_types_seq_items',
                                                                        'minor_opration_type_types_seq_items',
                                                                        'status_seq_items', 'file_name_seq_items'], axis=1)        
            
            flagged_items_list, non_flagged_items_list = identifyDominatingFeatureSpace(aggegated_dataset_flagged,
                                                                                        aggegated_dataset_not_flagged)
            
            # Process names
            flagged_items_list.append(aggegated_dataset_flagged.process_name.tolist())
            non_flagged_items_list.append(np.NaN)
            
            # Ransomware Hash
            filename = filename.split('_')[0]
            flagged_items_list.append(filename)
            non_flagged_items_list.append(filename)
            
            # Category of the data or family : 0 and 1 indicate benign and malicious respectively
            flagged_items_list.append(1)
            non_flagged_items_list.append(0)
            
            processAggregateList.append(flagged_items_list)
            processAggregateList.append(non_flagged_items_list)
        
            del aggegated_dataset
            del aggegated_dataset_flagged
            del aggegated_dataset_not_flagged
        
        os.chdir(pwd)
        behaviour_feature_space_aggregated = pd.DataFrame(processAggregateList, columns = labels)
        
        # Dump aggregated dataframe
        behaviour_feature_space_aggregated.to_csv("./Behavior_Analysis_Results/behaviour_feature_space_aggregated.csv")