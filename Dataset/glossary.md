## Dataset Features

There are two types of I/O Request Packet (IRP) logs used for this project: (1) Benign and (2) Ransomware (or malicious). The benign dataset ontained from the archive contains logs in 11 different folders. Each folder represents different hardened or santinized machines where IRP logs are captured. We process the dataset and generate the following features from text based records -

```
* Operation (Categorical / String)
	- IRP (I/O Request Packet; Determines whether the given callback data structure represents an I/O request packet (IRP)-based I/O operation.)
	- FSF (Fast System Filter; Determines whether the given callback data structure represents a legacy file system filter - FSFilter callback operation.)
	- FI0 (Fast I/O; Determines whether the given callback data structure represents a fast I/O operation.)

* Sequence Number (Hex -> Int64)
	- A number for a particular

* Pre-operation Time (Timestamp -> Int64 as seconds)
	- Recorded as hours:minutes:seconds:milliseconds

* Post-operation Time (Timestamp -> Int64 as seconds)
	- Recorded as hours:minutes:seconds:milliseconds

* Operation Elapsed (Int64)
	- The difference between the start and end of the operation will always be wihin a day

* Process ID (Int64)
	- Fetched the value of the current process's ID using PsGetCurrentProcessId routine

* Thread ID (Int64)
	- Fetched the value of the current thread's ID using PsGetCurrentThreadId routine

* Parent PID (Int64)
	- Process ID of the parent process

* Process Name (String)

* Major Operation Type (Categorical / String)
	- The string of the Major operation type will have MJ keyword.
	- There are three kinds of operational flags.

* Minor Operation Type (Categorical / String)
	- The string of the Minor operation type will have MN keyword.
	- This is a sub entity of the major operation type.

* IRP Flag (Hex -> Int64)
	- If set, the flag will be a hex value followed by the following additional information:
	- IRP_NOCACHE - The operation is a noncached I/O operation. 
	- IRP_PAGING_IO - The operation is a paging I/O operation.
	- IRP_SYNCHRONOUS_API - The I/O operation is synchronous.
	- IRP_SYNCHRONOUS_PAGING_IO - The operation is a synchronous paging I/O operation.

* Device Object (Hex -> Int64)
	- An OS representation of a logical, virtual, or physical device for which a driver handles I/O requests, organized into a device stack

* File Object (Hex -> Int64)
	- Pointer to the file object, if any, for the operation

* Transaction (Hex -> Int64)
	- On Windows Vista and later, this member is an opaque transaction pointer to the transaction that is associated with the operation.

* Status (Hex -> Int64)
	- A 32-bit numbering space, used to map the value to a human-readable next text message

* Inform (Hex -> Int64)

* Argument 1 (Hex -> Int64)

* Argument 2 (Hex -> Int64)

* Argument 3 (Hex -> Int64)

* Argument 4 (Hex -> Int64)

* Argument 5 (Hex -> Int64)

* Argument 6 (Hex -> Int64)

* Buffer Length (Int64)

* Entropy (Float)

* File Name (String)

* Family ID (A Flag | 0 for benign and >0 for ransomware families)

* class (A Flag | 0 for benign and 1 for ransomware)
```
