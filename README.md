# mRNA: Efficienct mapping space exploration for Reconfigurable Neural Accelerator
## Introduction
mRNA is a mapping space exploration tool for MAERI. 
MAERI is a DNN Spatial Accelerator which is able to support flexible Dataflows. It aims at efficient mapping datalfows due to the diverse deep learning landscape. Detail of MAERI can refer to ASPLOS paper below:

>Hyoukjun Kwon, Ananda Samajdar, and Tushar Krishna. MAERI: Enabling Flexible Dataflow Mapping over DNN Accelerators via Reconfigurable Interconnects. >ASPLOS 2018

mRNA generates the DNN Model which is implemented by Tensorflow, extract the necessary information from each layer and generate the optimal mapping strategy which map a layer onto MAERI. It has three basically functionalities:

1. Efficienctly search the optimal DNN mapping for MAERI
2. Mapping space exploration tool for developers to understand the impact of mapping over MAERI
3. Generate the Network configuration for MERI.

## Tool setup
1. If you want to use Front-end Paser, you should have python3, Tensorflow environment and larkparser package.

