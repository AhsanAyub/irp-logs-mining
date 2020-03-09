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
    
if __name__ == '__main__':
    pwd = os.getcwd()
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