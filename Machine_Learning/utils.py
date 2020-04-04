__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Martindale, Nathan", "Smith, Steven",
               "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"


# Import libraries
import os
import glob
import pandas as pd


def read_gzip_compressed_dataset(file):
    """ Get a file path and return the dataset compressed using gzip algorithm """
    
    try:
        return pd.read_pickle(file, compression='gzip')
    except:
        try:
            return pd.read_csv(file, compression='gzip', header=0, sep=',', quotechar='"')
        except:
            print("%s cannot be read" % file)
            return
        
        
def read_zip_compressed_dataset(file):
    """ Get a file path and return the dataset compressed using zip algorithm """
    
    try:
        return pd.read_pickle(file, compression='zip')
    except:
        try:
            return pd.read_csv(file, compression='zip', header=0, sep=',', quotechar='"')
        except:
            print("%s cannot be read" % file)
            return


def read_uncompressed_dataset(file):
    """ Get a file path and return the uncompressed dataset"""
    
    try:
        return pd.read_pickle(file)
    except:
        try:
            return pd.read_csv(file)
        except:
            print("%s cannot be read" % file)
            return
    
    
def combineBenignIRPLogs(path):
    """
    The fuction iterates through every CSV file in a path.
    
    It will return the concat version of the dataframes inside a machine folder.
    """
    
    all_file_names = [i for i in glob.glob(str(path) + '/' + '*_processed.*')]
    all_file_names = sorted(all_file_names)
    
    # Combine all files in the dataframe
    try:
        return pd.concat([pd.read_csv(f) for f in all_file_names])
    except:
        print("Something went wrong in combining benign logs")


def getBenignDataset():
    """
    The fuction takes account to combineBenignIRPLogs(path) to iterate through
    all the machines'logs.
    
    It will return the concat version of the dataframes.
    """
    
    benign_dataset = pd.concat([combineBenignIRPLogs(str(os.getcwd()) + "/Dataset/benign-irp-logs/machine_" + str(i))
                                for i in range(1,12)])
    benign_dataset = benign_dataset.drop(['Unnamed: 0'], axis=1)
    
    return benign_dataset
    

def getRansomwareDataset(path):
    """ Get a file path and return the ransomware dataset """
    
    compression_type = path.split('.')[-1]
    if (compression_type == 'gz'):
        ransomware_dataset = read_gzip_compressed_dataset(path)
    elif (compression_type == 'zip'):        
        ransomware_dataset = read_zip_compressed_dataset(path)
    else:
        ransomware_dataset = read_uncompressed_dataset(path)
    
    try:
        ransomware_dataset = ransomware_dataset.drop(['Unnamed: 0'], axis=1)
    except:
        print("No need to drop the column")
    
    return ransomware_dataset


def processDataset(dataset):
    """
    The function performs processing the dataset that has got records of both benign and
    ransomware logs. After processing the dataset, it will return the processed dataframe.
    """
    
    # Dropping the columns that are not needed for analysis
    dataset = dataset.drop(['sequence_number', 'device_object', 'file_object', 'file_name', 'inform',
                            'arg1', 'arg2', 'arg3', 'arg4', 'arg5', 'arg6', 'class', 'family_id'], axis=1)
    
    # Convert data type of certain dataframe rows
    dataset['irp_nocache'] = dataset['irp_nocache'].astype(int)
    dataset['irp_paging_io'] = dataset['irp_paging_io'].astype(int)
    dataset['irp_synchoronous_api'] = dataset['irp_synchoronous_api'].astype(int)
    dataset['irp_synchoronous_paging_io'] = dataset['irp_synchoronous_paging_io'].astype(int)
    dataset['status'] = dataset['status'].apply(hex)
    dataset['irp_flag'] = dataset['irp_flag'].apply(hex)
    
    # Combine two colums together -> process id and process name
    dataset['process_id-process_name'] = dataset['process_id'].astype(str) + '_' + dataset['process_name']
    dataset = dataset.drop(['process_name'], axis = 1)
    
    # One-hot-encode the string features
    return pd.get_dummies(dataset, columns=['process_id-process_name', 'major_operation_type',
                                                             'minor_operation_type', 'irp_flag',
                                                             'transaction', 'status'], drop_first=True)


def getRansomwareFiles():
    """ Return all the ransomware files """
    
    try:
        all_file_names = [i for i in glob.glob(str(os.getcwd()) + '/Dataset/ransomware-irp-logs/*_labeled.*')]
        all_file_names = sorted(all_file_names)
        
        return all_file_names
    
    except:
        print("Ransomware files could not be read")
        return
    
def getProcessedDataset(ransomware_file_path):
    """
    The main function to perform processing the dataset.
    It will take input a ransomware file path.
    The function will return the processed dataframe in terms of X, Y_class, Y_family
    after utilizing features of other functions.
    """
    
    dataset = pd.concat([getBenignDataset(), getRansomwareDataset(ransomware_file_path)])
    Y_class = dataset.iloc[:, -1].values
    Y_family = dataset['family_id']
    
    return processDataset(dataset), Y_class, Y_family
    
#dataset, Y_class, Y_family = getProcessedDataset("/Users/ahsanayub/Documents/School Work/CSC 6220/irp-logs-mining/Dataset/ransomware-irp-logs/0bba707dc1545da8d7b7b74201a96097e267a345b7de996ea4d629af27ee4f0f_processed_labeled.pkl.gz")