#include "Analyzer.h"
#include <gflags/gflags.h>
#ifndef LINUX
#define LINUX
#endif

#define _USE_GFLAGS
#ifdef _USE_GFLAGS

#ifdef LINUX
#include "Extern/gflags/linux/include/gflags.h"
#else
#include "Extern/gflags/windows/gflags.h"
#endif

DEFINE_bool(energy, false, "MAERI Mapper will generate the mapping stragy which has the least energy consumption.");
DEFINE_bool(energy_efficiency, false, "MAERI Mapper will generate the mapping stragy which has the highest energy efficiency.");
DEFINE_bool(performance, false, "MAERI Mapper will generate the mapping stragy which has the bset performance.");
DEFINE_bool(show_maeri, false, "Print the physical connection of the MAERI system.");
DEFINE_bool(genconfig, false, "The configuration of the generated mapping.");
//DEFINE_bool(cambricon, false, "Analyze cambricon.");
//DEFINE_bool(systolic_array, false, "Analyze systolic array.");
DEFINE_bool(show_energy, false, "MAERI Mapper will generate the normalized energy distribution.");
DEFINE_string(model_para, "Model_parameter.txt", "File path for parameters of the layer in DNN model.");
//DEFINE_string(dsn_input, "DSN_input.txt", "File path for input data of the distribute network.");
//DEFINE_string(dsn_output, "DSN_output.txt", "File path for output data of the distribute network.");
DEFINE_string(config_file, "Config_file.txt", "The configuration of the other parameters of the hardware and ISA.");
DEFINE_int32(num_ms, 256, "Specify the number of multiplier switches in MAERI system.");
DEFINE_int32(dn_bw, 256, "Specify the bandwidth of the distribute network.");
DEFINE_int32(rn_bw, 256, "Specify the bandwidth of the reduce network.");

#endif

int main(int argc, char** argv) {

  std::string opt;
  OptGoal opt_goal = all;
  opt = "all";
#ifdef _USE_GFLAGS
  #ifdef LINUX
    gflags::ParseCommandLineFlags(&argc, &argv, true);
  #else
    google::ParseCommandLineFlags(&argc, &argv, true);
  #endif

  if (FLAGS_energy) {
    opt_goal = energy;
    opt = "energy";
  }
  else if (FLAGS_energy_efficiency) {
    opt_goal = energy_efficiency;
    opt = "energy_efficiency";
  }
  else if (FLAGS_performance) {
    opt_goal = performance;
    opt = "performance";
  }

  //std::ifstream DSNInput(FLAGS_dsn_input);
  std::ifstream ModelParameter(FLAGS_model_para);
  std::ifstream ConfigFile(FLAGS_config_file);
  int ms_num = FLAGS_num_ms;
  int dn_bw  = FLAGS_dn_bw;
  int rn_bw  = FLAGS_rn_bw;
#else
#endif

  std::string Type[3] = {"CONV", "FC", "RNN"};
  /*
  std::string modelname = "VGGNet";
  std::string modeltype = "FC";
  */
  Maeri* maeri = new Maeri(ms_num, dn_bw, rn_bw);


  //Check the correctness of the data movement network.
  if(FLAGS_show_maeri) {
    std::string model = "model_graph.dot";
    std::ofstream maerimodel(model);
    maeri->DrawNetwork(maerimodel);
  }
/*
  CNNInput* layer_input = new CNNInput(4096, 1, 1);
  CNNFilter* filter_weight = new CNNFilter(1000, 4096, 1, 1, 1);
  CNNOutput* layer_output = new CNNOutput(1000, 1, 1);
  RNNHidden* hidden = new RNNHidden(512, 1, 1);
*/
  DNNModel* dnn = new DNNModel();
  dnn->parsefile(ModelParameter);

  std::string outputfile = "DNN-" + dnn->model_name + "-" + dnn->layer_type + dnn->layer_num + "_MAERI-MS-"
                           + std::to_string(maeri->pe_size) + "-DSW-" + std::to_string(maeri->dn_bw) + "-RSW-"
                           + std::to_string(maeri->rn_bw) + "_Opt-" + opt + ".txt";
  std::ofstream Profile_result(outputfile);

  Analyzer* analyzer = new Analyzer(maeri, dnn, opt_goal);

  analyzer->setshowenergy(FLAGS_show_energy);
  analyzer->setoptgoal(opt_goal);

  if(ConfigFile && FLAGS_show_energy) {
    analyzer->parseconfig(ConfigFile);
  }
  else if(FLAGS_show_energy && !ConfigFile) {
    std::cerr << "You must have a config file if you want to calculate energy, please check if config file exists in the path.\n";
  }
/*
  if(FLAGS_systolic_array && analyzer->dnn_model->layer_type == Type[0]) {
    analyzer->AnalyzeSystolicCNN(Profile_result);
  }
  else if(FLAGS_systolic_array && analyzer->dnn_model->layer_type == Type[1]) {
    analyzer->AnalyzeSystolicFC(Profile_result);
  }
  else if(FLAGS_cambricon && analyzer->dnn_model->layer_type == Type[0]) {
    analyzer->AnalyzeCambricon(Profile_result);
  }
  else if(FLAGS_cambricon && analyzer->dnn_model->layer_type == Type[1]) {
    analyzer->AnalyzeCambriconFC(Profile_result);
  }
  */

  if(analyzer->dnn_model->layer_type == Type[0]) {
    analyzer->AnalyzeCNN(Profile_result, opt_goal);
  }
  else if (analyzer->dnn_model->layer_type == Type[1]) {
    analyzer->AnalyzeFC(Profile_result, opt_goal);
  }
  else if (analyzer->dnn_model->layer_type == Type[2]) {
    analyzer->AnalyzeRNN(Profile_result, opt_goal);
  }

  if(FLAGS_genconfig) {
    std::string config_out = "Maeri_config_" + dnn->layer_type + dnn->layer_num + ".txt";
    std::ofstream OutputConfig(config_out);
    analyzer->ConfigGen(OutputConfig);
  }


  return 0;
}
