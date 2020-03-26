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

# Utility function to find the Process IDs and Process Names that are flagged
def find_malicious_logs(dataset):
    # Initialize return lists
    process_ids = []
    process_names = []
    
    dataset = dataset.drop(dataset[(dataset['doc_files_flag'] != 1)].index)
   
    process_ids = dataset['process_id'].tolist()
    process_names = dataset['process_name'].tolist()
    
    return process_ids, process_names

# Utility function to find the Process IDs and Process Names that are flagged
def set_malicious_logs_labels(dataset, process_ids, process_names, ransomware_hash):
    
    dataset['family_id'] = ransomware_hash
    
    malicious_copy_dataset = dataset[(dataset['process_id'].isin(process_ids) & dataset['process_name'].isin(process_names))]
    malicious_copy_dataset['class'] = 1
    
    benign_copy_dataset = dataset[~(dataset['process_id'].isin(process_ids) & dataset['process_name'].isin(process_names))]
    benign_copy_dataset['class'] = 0
    
    frames = [malicious_copy_dataset, benign_copy_dataset]
    return pd.concat(frames)


def generate_time_chunks(dataset, start_time, end_time, interval, ransomware_hash):
    chunk_size = round((end_time - start_time) / interval)
    
    #Create Directory
    file_path = "/Time_Interval_Dataset/" + str(ransomware_hash) #+ "/" + str(round(interval / 60)) + "_mins"
    try:
        if(os.path.isdir(os.getcwd() + file_path) != True):
            os.mkdir(os.getcwd() + file_path)
            print(str(os.getcwd() + file_path) + " is created.")
        file_path = file_path +  "/" + str(round(interval / 60)) + "_mins"
        if(os.path.isdir(os.getcwd() + file_path)) != True:
            os.mkdir(os.getcwd() + file_path)
            print(str(os.getcwd() + file_path) + " is created.")
    except OSError:
        print("Creation of the directory %s failed" % file_path)
        return
    
    file_name = str(ransomware_hash) + "_" + str(round(interval / 60)) + "_mins"
    str_log = ""
    start_time_index = start_time
    for i in range(chunk_size):
        if(i != chunk_size - 1):
            end_time_index = start_time_index + interval
        else:
            end_time_index = end_time + 1
        temp_dataset_copy = labeled_processed_data[((labeled_processed_data.pre_operation_time >= start_time_index) & (labeled_processed_data.pre_operation_time < end_time_index))] 
        
        # Dump the file
        temp_dataset_copy.to_pickle(str(os.getcwd()) + str(file_path) + "/" + str(file_name) + "_" + str(i+1) + ".pkl.gz", compression='gzip')
        
        str_log = str_log + str(i+1) + "\t" + str(start_time_index) + "\t" + str(end_time_index) + "\t" + str(temp_dataset_copy.shape) + "\n"
        start_time_index = start_time + ((i + 1) * interval)
        
    print(str_log)
    
    with open(str(os.getcwd()) + str(file_path)  + "/" + str(file_name) + ".txt", "w") as text_file:
        print(str_log, file=text_file)
    

if __name__ == '__main__':
    pwd = os.getcwd()
    os.chdir('./Dataset/ransomware-irp-logs/')
    
    # Storing the file names for all the aggregated datasets
    all_filenames_aggregated = [i for i in glob.glob('*_aggregated*')]
    all_filenames_aggregated = sorted(all_filenames_aggregated)
    
    all_filenames_processed = [i for i in glob.glob('*_processed.*')]
    all_filenames_processed = sorted(all_filenames_processed)
    
    file_name_aggregated = all_filenames_aggregated[7]
    file_name_processed = all_filenames_processed[7]
    
    try:
        aggegated_dataset = pd.read_csv(file_name_aggregated, compression='zip', header=0, sep=',', quotechar='"')
        try:
            processed_dataset = pd.read_csv(file_name_processed, compression='zip', header=0, sep=',', quotechar='"')
        except:
            processed_dataset = pd.read_pickle(file_name_processed, compression='zip')
    except:
        aggegated_dataset = pd.read_csv(file_name_aggregated, compression='gzip', header=0, sep=',', quotechar='"')
        try:
            processed_dataset = pd.read_csv(file_name_processed, compression='gzip', header=0, sep=',', quotechar='"')
        except:
            processed_dataset = pd.read_pickle(file_name_processed, compression='gzip')
            
    aggegated_dataset = aggegated_dataset.drop(['Unnamed: 0'], axis=1)    
    process_ids, process_names = find_malicious_logs(aggegated_dataset)
    
    ransomware_hash = file_name_aggregated.split('_')[0]
    labeled_processed_data = set_malicious_logs_labels(processed_dataset, process_ids, process_names, ransomware_hash)
    
    del aggegated_dataset
    del processed_dataset
    del process_ids
    del process_names
    
    # Dump processed and label dataset
    labeled_processed_data.to_pickle(str(ransomware_hash) + "_processed_labeled.pkl.gz", compression='gzip')
    print("Labeled dataset generated")
    
    # Partiton the data into time chunks
    ''' The difference will be around an hour and half and the values are in seconds'''
    start_time = labeled_processed_data.pre_operation_time.min()
    end_time = labeled_processed_data.pre_operation_time.max()
    
    generate_time_chunks(labeled_processed_data, start_time, end_time, (5*60), ransomware_hash) # 5 mins
    generate_time_chunks(labeled_processed_data, start_time, end_time, (10*60), ransomware_hash) # 10 mins
    generate_time_chunks(labeled_processed_data, start_time, end_time, (20*60), ransomware_hash) # 20 mins
    
    del labeled_processed_data
    
    os.chdir(pwd)