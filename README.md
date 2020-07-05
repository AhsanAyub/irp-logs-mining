## I/O Request Packet (IRP) Logs Driven Ransomware Detection Scheme

The project aims to extract pattern(s) of malicious processes (e.g., ransomware) from the IRP logs that were generated by running 272 ransomware samples on a Windows machine. Besides, there are labelled benign IRP logs that were recorded in different sessions of users' machine which did not have any malicious program installed.

All the ransomware samples were labelled and grouped with its families with the help of [AVClass](https://github.com/malicialab/avclass) - a malware labelling tool and [VirusTotal](https://developers.virustotal.com/reference) API engine. After the datasets are processed and labelled, we constructed an Artificial Neural Network (ANN) model in order to perform binary classification (detection of benign and malicious logs).

The research project has been published at the IEEE 21st International Conference on Information Reuse and Integration for Data Science [(IEEE IRI 2020)](https://homepages.uc.edu/~niunn/IRI20/).


## Acknowledgement

We would like to thank [Andrea Continella, Ph.D.](https://conand.me/) to provide us with the datasets that we have used on this project. The research paper can be found here: [SheildFS 2016](https://dl.acm.org/doi/pdf/10.1145/2991079.2991110)


### Citing this work
If you use our implementation for academic research, you are highly encouraged to cite [our paper](https://ahsanayub.github.io/assets/paper/Authors_Copy_An_IO_Request_Packet_(IRP)_Driven_Effective_Ransomware_Detection_Scheme_using_Artificial_Neural_Network.pdf).

```
@inproceedings{ayub2020io,
	title={An I/O Request Packet (IRP) Driven Effective Ransomware Detection Scheme using Artificial Neural Network},
	author={Ayub, Md Ahsan and Continella, Andrea and Siraj, Ambareen},
	booktitle={2020 IEEE International Conference on Information Reuse and Integration (IRI)},
	year={2020},
	pages={1-6},
	organization={IEEE}
}
```

The work has been entire funded by [Cybersecurity Education, Research & Outreach Center (CEROC)](https://www.tntech.edu/ceroc/) at Tennessee Tech University.
