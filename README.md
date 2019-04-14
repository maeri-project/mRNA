# mRNA: Efficienct mapping space exploration for Reconfigurable Neural Accelerator
## Introduction
**mRNA** is a mapping space exploration tool for **MAERI**. 
MAERI is a DNN Spatial Accelerator which is able to support flexible Dataflows. It aims at efficient mapping of datalfows emanating from the diverse deep learning landscape. For details of **MAERI**, please refer to the ASPLOS 2018 paper below and for its code base, you can go to [here](https://github.com/georgia-tech-synergy-lab/maeri)

>Hyoukjun Kwon, Ananda Samajdar, and Tushar Krishna, MAERI: Enabling Flexible Dataflow Mapping over DNN Accelerators via Reconfigurable Interconnects, ASPLOS 2018

**mRNA** generates the DNN Model which is implemented by Tensorflow, extracts the necessary information from each layer, and generate the optimal mapping strategy which map a layer onto MAERI. It has three basic functionalities:

1. Efficienctly search the optimal DNN mapping for MAERI
2. Mapping space exploration tool for developers to understand the impact of mapping over MAERI
3. Generate the Network configuration(s) for MERI.

For details on mRNA, please refer to the ISPASS 2019 paper below.
>Zhongyuan Zhao, Hyoukjun Kwon, Sachit Kuhar, Weiguang Sheng, Zhigang Mao, and Tushar Krishna, mRNA: Enabling Efficient Mapping Space Exploration for a Reconfigurable Neural
Accelerator, ISPASS 2019

## Tool Setup
1. If you want to use Front-end Paser, you should have **python3**, **Tensorflow** environment and **lark-parser** package. The install information of **Tensorflow** goes to 
[here](https://tensorflow.google.cn/install). The install information of **lark-parser** package goes to 
[here](https://github.com/lark-parser/lark). And the for information of installing **python3** please go to [here](https://www.python.org/downloads/).
2. For using **mRNA**, you should install **Gglags**, the download and install information of **Gflags** please go to [here](https://github.com/gflags/gflags).
3. Install instruction:

```
1. Enter into mRNA folder
2. cd build
3. cmake ../
4. make
```

We also provide an executable file inside build folder so that you do not need to install gflags. However, if this does not work, you should install mRNA according to the afore mentioned steps.

## Command Guide

### Front-end Parser
The Front-end Parser get the DNN Model as input and output the information of each layer include DNN Model name, layer type and name. And four dimensional representation of input, weight, output and hidden unit (for LSTM). The command example is:

```
python3 network_parser.py #dnn_model#.py
```
And all the output parameters of each layer for a DNN mdoel are located inside param folder. 
The **input** folder contains all the layer representations for four DNN Model (alexnet, resnet, vggnet and rnn). We also provide the Tensorflow implementation so that you can try to generate the parameters of each layer for a specific model.  

### Analyzer

You can use **--help** command to check all the descriptions of each command

```
build/MAERI_Mapper --help

```
You can see the architecture of MAERI (32 MSes in this example) under different scales by typing command

```
build/MAERI_Mapper -show_maei num_ms=32

```

If you want to understand the impact of mapping over MAERI, example below is the command of mapping a convolutional layer of alexnet, and generating the profile result for this layer

```
1. cd mNRA/input/alexnet
2. ../../build/MAERI_Mapper -model_para="Model_parameter_4.txt" -show_energy 
                            -config_file="Config_file.txt" -num_ms=256 -dn_bw=128 -rn_bw=256 
                            -performance
```
If you want to generate the configuration, you should add **-genconfig** option in the commmand.

```
../../build/MAERI_Mapper -model_para="Model_parameter_2.txt" -show_energy 
                         -config_file="Config_file.txt" -dn_bw=128 -rn_bw=256 
                         –performance -genconfig
```

### Output file
The output file of mRNA is generated int the same path as the input file. The name scheme of the output profile file is as follows

```
DNN-#DNNModelName#-#Layer Type##Layer Number#_#MS Num#-#DSW#-#RSW#-#Opt Goal#.txt

```
The DSW and RSW represents the bandwidth of DS and RS Network. Example of outputfile is: 

```
DNN-GoogleNet-CONV1_MAERI-MS-256-DSW-128-RSW-256_Opt-performance.txt

```




