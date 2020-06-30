### Dataset Infomration

There are two types of datasets used in this project: [Ransomware IRP logs](https://github.com/AhsanAyub/irp-logs-mining/tree/master/Dataset/ransomware-irp-logs) and [Beneign IRP logs](https://github.com/AhsanAyub/irp-logs-mining/tree/master/Dataset/benign-irp-logs). The repo only contains a few samples that will help understand the datasets' structure as well as the code base. The full access to the datasets can be given upon request.


#### Ransomware IRP Logs

All the the experimentations have been performed with 272 ransomware samples grouped into 18 ransomware families. Therefore, this [folder](https://github.com/AhsanAyub/irp-logs-mining/tree/master/Dataset/ransomware-irp-logs) contains 18 unique folders that signify ransomware family. In every folder, there is one of the ransomware family's samples dataset saved into three files: `<sample-name>.processed` file is the processed version from the raw acquired IRP file of the sample; `<sample-name>.aggregated` file is the `process id` and `process name` tuple's aggregated version of the feature; and `<sample-name>.labeled` file is the derivative version of the processed file with an added feature of `class` to signify a record is benign or malicious. It is to note that not every record in the samples' datasets are malicious.


#### Benign IRP Logs

Benign IRP records have been collected through 11 volunteers' machines (includes home, office, and dev usuers ranging from Windows 7 to Windows 10). Similar to ransomware IRP logs, the [folder](https://github.com/AhsanAyub/irp-logs-mining/tree/master/Dataset/benign-irp-logs) contains a few sessions' datasets from each machine.