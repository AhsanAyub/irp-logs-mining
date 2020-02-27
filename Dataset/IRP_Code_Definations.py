"""
    The purpose of the script is to create an associative numeric code
    of the IRP major and minor string based codes.
    
    The methods will return the numeric code associated with the code.
"""

__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Martindale, Nathan", "Smith, Steven",
               "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@students.tntech.edu"
__status__ = "Prototype"

# Import library
import numpy as np

irp_major_operation = {
            # standard IRP_MJ string definitions 
            "IRP_MJ_CREATE": 1,
            "IRP_MJ_CREATE_NAMED_PIPE": 2,
            "IRP_MJ_CLOSE": 3,
            "IRP_MJ_READ": 4,
            "IRP_MJ_WRITE": 5,
            "IRP_MJ_QUERY_INFORMATION": 5,
            "IRP_MJ_SET_INFORMATION": 6,
            "IRP_MJ_QUERY_EA": 7,
            "IRP_MJ_SET_EA": 8,
            "IRP_MJ_FLUSH_BUFFERS": 9,
            "IRP_MJ_QUERY_VOLUME_INFORMATION": 10,
            "IRP_MJ_SET_VOLUME_INFORMATION": 11,
            "IRP_MJ_DIRECTORY_CONTROL": 12,
            "IRP_MJ_FILE_SYSTEM_CONTROL": 13,
            "IRP_MJ_DEVICE_CONTROL": 14,
            "IRP_MJ_INTERNAL_DEVICE_CONTROL": 15,
            "IRP_MJ_SHUTDOWN": 16,
            "IRP_MJ_LOCK_CONTROL": 17,
            "IRP_MJ_CLEANUP": 18,
            "IRP_MJ_CREATE_MAILSLOT": 19,
            "IRP_MJ_QUERY_SECURITY": 20,
            "IRP_MJ_SET_SECURITY": 21,
            "IRP_MJ_POWER": 22,
            "IRP_MJ_SYSTEM_CONTROL": 23,
            "IRP_MJ_QUERY_QUOTA": 24,
            "IRP_MJ_SET_QUOTA": 25,
            "IRP_MJ_PNP": 26,
            
            # FSFilter string definitions
            "IRP_MJ_ACQUIRE_FOR_SECTION_SYNC": 27,
            "IRP_MJ_RELEASE_FOR_SECTION_SYNC": 28,
            "IRP_MJ_ACQUIRE_FOR_MOD_WRITE": 29,
            "IRP_MJ_RELEASE_FOR_MOD_WRITE": 30,
            "IRP_MJ_ACQUIRE_FOR_CC_FLUSH": 31,
            "IRP_MJ_RELEASE_FOR_CC_FLUSH": 32,
            "IRP_MJ_NOTIFY_STREAM_FO_CREATION": 32,
            
            # FAST_IO and other string definitions
            "IRP_MJ_FAST_IO_CHECK_IF_POSSIBLE": 33,
            "IRP_MJ_DETACH_DEVICE": 34,
            "IRP_MJ_NETWORK_QUERY_OPEN": 35,
            "IRP_MJ_MDL_READ": 36,
            "IRP_MJ_MDL_READ_COMPLETE": 37,
            "IRP_MJ_PREPARE_MDL_WRITE": 38,
            "IRP_MJ_MDL_WRITE_COMPLETE": 39,
            "IRP_MJ_VOLUME_MOUNT": 40,
            "IRP_MJ_VOLUME_DISMOUNT": 41
        }

irp_minor_operation = {
            # Strings for the Irp minor codes 
            "IRP_MN_QUERY_DIRECTORY": 1,
            "IRP_MN_NOTIFY_CHANGE_DIRECTORY": 2,
            "IRP_MN_USER_FS_REQUEST": 3,
            "IRP_MN_MOUNT_VOLUME": 4,
            "IRP_MN_VERIFY_VOLUME": 5,
            "IRP_MN_LOAD_FILE_SYSTEM": 5,
            "IRP_MN_TRACK_LINK": 6,
            "IRP_MN_LOCK": 7,
            "IRP_MN_UNLOCK_SINGLE": 8,
            "IRP_MN_UNLOCK_ALL": 9,
            "IRP_MN_UNLOCK_ALL_BY_KEY": 10,
            "IRP_MN_NORMAL": 11,
            "IRP_MN_DPC": 12,
            "IRP_MN_MDL": 13,
            "IRP_MN_COMPLETE": 14,
            "IRP_MN_COMPRESSED": 15,
            "IRP_MN_MDL_DPC": 16,
            "IRP_MN_COMPLETE_MDL": 17,
            "IRP_MN_COMPLETE_MDL_DPC": 18,
            "IRP_MN_SCSI_CLASS": 19,
            "IRP_MN_START_DEVICE": 20,
            "IRP_MN_QUERY_REMOVE_DEVICE": 21,
            "IRP_MN_REMOVE_DEVICE": 22,
            "IRP_MN_CANCEL_REMOVE_DEVICE": 23,
            "IRP_MN_STOP_DEVICE": 24,
            "IRP_MN_QUERY_STOP_DEVICE": 25,
            "IRP_MN_CANCEL_STOP_DEVICE": 26,
            "IRP_MN_QUERY_DEVICE_RELATIONS": 27,
            "IRP_MN_QUERY_INTERFACE": 28,
            "IRP_MN_QUERY_CAPABILITIES": 29,
            "IRP_MN_QUERY_RESOURCES": 30,
            "IRP_MN_QUERY_RESOURCE_REQUIREMENTS": 31,
            "IRP_MN_QUERY_DEVICE_TEXT": 32,
            "IRP_MN_FILTER_RESOURCE_REQUIREMENTS": 32,
            "IRP_MN_READ_CONFIG": 33,
            "IRP_MN_WRITE_CONFIG": 34,
            "IRP_MN_EJECT": 35,
            "IRP_MN_SET_LOCK": 36,
            "IRP_MN_QUERY_ID": 37,
            "IRP_MN_QUERY_PNP_DEVICE_STATE": 38,
            "IRP_MN_QUERY_BUS_INFORMATION": 39,
            "IRP_MN_DEVICE_USAGE_NOTIFICATION": 40,
            "IRP_MN_SURPRISE_REMOVAL": 41,
            "IRP_MN_QUERY_LEGACY_BUS_INFORMATION": 42,
            "IRP_MN_WAIT_WAKE": 43,
            "IRP_MN_POWER_SEQUENCE": 44,
            "IRP_MN_SET_POWER": 45,
            "IRP_MN_QUERY_POWER": 46,
            "IRP_MN_QUERY_ALL_DATA": 47,
            "IRP_MN_QUERY_SINGLE_INSTANCE": 48,
            "IRP_MN_CHANGE_SINGLE_INSTANCE": 49,
            "IRP_MN_CHANGE_SINGLE_ITEM": 50,
            "IRP_MN_ENABLE_EVENTS": 51,
            "IRP_MN_DISABLE_EVENTS": 52,
            "IRP_MN_ENABLE_COLLECTION": 53,
            "IRP_MN_DISABLE_COLLECTION": 54,
            "IRP_MN_REGINFO": 55,
            "IRP_MN_EXECUTE_METHOD": 56
        }

# Full list - https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-erref/596a1078-e883-4972-9bbc-49e60bebca55
irp_status_codes = { 
            # String Codes of the interesting flags - Not a complete list
            0: "STATUS_SUCCESS",
            298: "STATUS_FILE_LOCKED_WITH_ONLY_READERS",
            299: "STATUS_FILE_LOCKED_WITH_ONLY_WRITERS",
            2147483653: "STATUS_BUFFER_OVERFLOW",
            2147483654: "STATUS_NO_MORE_FILES",
            3221225487: "STATUS_NO_SUCH_FILE",
            3221225524: "STATUS_OBJECT_NAME_NOT_FOUND",
            3221225530: "STATUS_OBJECT_PATH_NOT_FOUND",
            3221225688: "STATUS_CANT_WAIT"
        }

# Return the value of the IRP Major Operation Type String
def getMajorOperationCode(key):
    if key in irp_major_operation:
        return irp_major_operation[key]
    else:
        return np.nan

# Return the value of the IRP Minor Operation Type String        
def getMinorOperationCode(key):
    if key in irp_minor_operation:
        return irp_minor_operation[key]
    else:
        return np.nan
        
def getIRPStatusCodeString(key):
    if key in irp_status_codes:
        return irp_status_codes[key]
    else:
        return "Not found"