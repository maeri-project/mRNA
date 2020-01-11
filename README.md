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

## Installation
### MAERI_Mapper
To build MAERI_Mapper, you'll need:
* [gflags]
* pkg-config
* make
* gcc

#### Building on Mac
You'll first need to have [brew] installed on your Mac.
```bash
git clone https://github.com/georgia-tech-synergy-lab/mRNA
cd mRNA
brew install pkg-config gflags
make -j4
make install
```

You can uninstall with ``make uninstall``

#### Building on Linux
The following instructions are for Ubuntu: use the correct package manager for your distro.
```bash
git clone https://github.com/georgia-tech-synergy-lab/mRNA
cd mRNA
apt install libgflags-dev build-essential pkg-config
make -j4
make install
```

You can uninstall with ``make uninstall``

#### Building on Windows
Follow the instructions for [Building on Linux](#building-on-linux) with bash on windows.


### Front-end Parser
1. If you want to use Front-end Parser, you should have python3, [Tensorflow] and [lark-parser]. 


### Front-end Parser
The Front-end Parser takes the DNN Model as input and outputs the information of each layer including the DNN Model name, layer type and name, and a four dimensional representation of input, weight, output and hidden unit (for LSTM). 

Here is an example:

```
python3 network_parser.py #dnn_model#.py
```
All the output parameters of each layer for a DNN mdoel are located inside the param folder. 
The **input** folder contains all the layer representations for four DNN Model (alexnet, resnet, vggnet and rnn). 
We also provide a Tensorflow implementation so that you can try to generate the parameters of each layer for a specific model.  

### Analyzer

Use **--help** to get a list of all the commands.

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
[Tensorflow]: https://tensorflow.google.cn/install
[lark-parser]: https://github.com/lark-parser/lark
[gflags]: https://github.com/gflags/gflags
[brew]: https://brew.sh