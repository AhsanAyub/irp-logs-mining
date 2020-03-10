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
import aggregator as aggregator

if __name__ == '__main__':
    
    pwd = os.getcwd()
    
    for i in range(1, 12): # Since there are 11 machines
        # Accessing file paths to all the machines one by one
        file_path = "./benign-irp-logs/machine_" + str(i) + "/"
        os.chdir(file_path)
    
        # Storing the file names for all the aggregated datasets
        all_filenames = [i for i in glob.glob('*_processed.csv')]
        all_filenames = sorted(all_filenames)

        # Aggregation of benign dataset one file in a folder    
        for filename in all_filenames:
            
            # Initialize a process dataframe
            processed_dataset = pd.read_csv(filename)
            processed_dataset = processed_dataset.drop(['Unnamed: 0'], axis=1)
            print(processed_dataset.head())
            
            # Generate aggregated dataframe
            processed_aggegate_dataset = aggregator.aggegateData(processed_dataset)
            print("Aggegating the processed dataset is also done.")
            
            # Dump aggregated dataframe
            filename = filename.split('.csv')[0]
            processed_aggegate_dataset.to_csv(str(filename) + "_aggregated.csv")
            
            del processed_dataset
            del processed_aggegate_dataset
        
        os.chdir(pwd)
    
    del all_filenames