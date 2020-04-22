# Importing libraries
import os
import glob
import json
from shutil import copytree
from shutil import copyfile

def findIndex(hash_file, all_filenames_hashes):
    """ Utility function to return the index of the hash file from the list """
    index = 0
    for hashes in all_filenames_hashes:
        if(hashes == hash_file):
            return index
        index += 1
        
    return -1

def main():
    """
    Main function to iterate through all the hashes in the json dataset.
    For each iteration, the fetch hash file is checked if it exists in the dataset.
    If does, then four types of copy opereation will be performed:
        1. Labeled dataset
        2. Processed dataset
        3. Aggregated dataset
        4. Folder in the Time Interval dataset
    """
    for family_name in json_data["family_outline"]:
        # Create a directory in the folder
        path_time_interval = "./ransomware-irp-logs/Time_Interval_Dataset/" + str(family_name)
        path_processed = "./ransomware-irp-logs/" + str(family_name)
        os.mkdir(path_time_interval)
        os.mkdir(path_processed)
        
        for hashes in json_data[family_name]:
            # fetch all the files
            index_of_hash_file = findIndex(hashes, all_filenames_hashes)
            if (index_of_hash_file == -1):
                print("%s NOT found" % hashes)
            else:
                filename_labeled = all_filenames_labeled[index_of_hash_file].split('/')[-1]
                filename_aggregated = all_filenames_aggregated[index_of_hash_file].split('/')[-1]
                filename_processed = all_filenames_processed[index_of_hash_file].split('/')[-1]
                
                print(str(all_filenames_labeled[index_of_hash_file]), str(path_processed) + "/" + str(filename_labeled))
                print(str(all_filenames_aggregated[index_of_hash_file]), str(path_processed) + "/" + str(filename_aggregated))
                print(str(all_filenames_processed[index_of_hash_file]), str(path_processed) + "/" + str(filename_processed))
                print("./ransomware-irp-logs/Time_Interval_Dataset/" + str(hashes), str(path_time_interval) + "/" + str(hashes))
                print("\n")
                
                try:
                    
                    copyfile(str(all_filenames_labeled[index_of_hash_file]), str(path_processed) + "/" + str(filename_labeled))
                    copyfile(str(all_filenames_aggregated[index_of_hash_file]), str(path_processed) + "/" + str(filename_aggregated))
                    copyfile(str(all_filenames_processed[index_of_hash_file]), str(path_processed) + "/" + str(filename_processed))
                    copytree("./ransomware-irp-logs/Time_Interval_Dataset/" + str(hashes), str(path_time_interval) + "/" + str(hashes))
                except:
                    print("Something went wrong for %s" % hashes)
                    continue

if __name__ == '__main__':
    
    all_filenames_labeled = [i for i in glob.glob('./ransomware-irp-logs/*labeled*')]
    all_filenames_labeled = sorted(all_filenames_labeled)
    all_filenames_aggregated = [i for i in glob.glob('./ransomware-irp-logs/*aggregated*')]
    all_filenames_aggregated = sorted(all_filenames_aggregated)
    all_filenames_processed = [i for i in glob.glob('./ransomware-irp-logs/*_processed.*')]
    all_filenames_processed = sorted(all_filenames_processed)
    all_filenames_hashes = [filename.split('_')[0] for filename in all_filenames_labeled]
    all_filenames_hashes = [filename.split('/')[-1] for filename in all_filenames_hashes]
    
    json_data = json.load(open("rasomware_family_and_sample_map.json"))
    main()

    del all_filenames_labeled, all_filenames_aggregated, all_filenames_processed, all_filenames_hashes
    del json_data
