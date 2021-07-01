#pragma once
#include <string>
#include <torch/script.h>
#include <torch/torch.h>
#include <vector>

class Backend {
private:
  torch::jit::script::Module m_model;
  int m_loaded;

public:
  Backend();
  void perform(std::vector<float *> in_buffer, std::vector<float *> out_buffer,
               int n_vec, std::string method);
  int load(std::string path);
};
