## Dataset Features

There are two types of I/O Request Packet (IRP) logs used for this project: (1) Benign and (2) Ransomware (or malicious). The following are the features fields -

```
* Operation (Categorical / String)
* Sequence Number (Hex)
* Pre-operation Time (Timestamp)
* Post-operation Time (Timestamp)
* Process ID (Numerical)
* Thread ID (Numerical)
* Parent ID (Numerical)
* Process Name (String)
* Major Operation Type (Categorical / String)
* IRP Flag (Hex)
* Device Object (Hex)
* File Object (Hex)
* Transaction (Hex)
* Status (Hex)
* Inform (String)
* Argument 1 (Hex)
* Argument 2 (Hex)
* Argument 3 (Hex)
* Argument 4 (Hex)
* Argument 5 (Hex)
* Argument 6 (Hex)
* Buffer Length (Numeric)
* Entropy (Numeric)
* File Name (String)
```

## Data Processing

The benign dataset ontained from the archive contains logs in 11 different folders. Each folder represents different hardened or santinized machines where IRP logs are captured. We process the dataset and generate the following features from text based records -

```
* Operation (Categorical / String)
* Sequence Number (Hex -> Int64)
* Pre-operation Time (Timestamp -> Int64 as seconds)
* Post-operation Time (Timestamp -> Int64 as seconds)
* Operation Elapsed (Int64)
* Process ID (Int64)
* Thread ID (Int64)
* Parent ID (Int64)
* Process Name (String)
* Major Operation Type (Categorical / String)
* IRP Flag (Hex -> Int64)
* Device Object (Hex -> Int64)
* File Object (Hex -> Int64)
* Transaction (Hex -> Int64)
* Status (Hex -> Int64)
* Inform (String)
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