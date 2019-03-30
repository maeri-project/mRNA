//
// Created by Zhongyuan Zhao on 9/26/18.
//

#include "utility.h"

bool isNum(std::string str) {
  std::istringstream sin(str);
  double d;
  char c;
  if(!(sin >> d)) {
    return false;
  }
  else if(sin >> c) {
    return false;
  }
  else {
    return true;
  }
}

std::string getstr(std::istringstream& instr) {
  std::string str;
  while(instr >> str) {
    if(isNum(str)) {
      return str;
    }
    else {
      continue;
    }
  }
}
