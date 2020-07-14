#include <fstream>
#include <iostream>
#include <utility>
#include <string>
#include <array>
#include <vector>
int main() {
  std::ifstream image("../img/sent.jpg", std::ios::binary);
  std::vector<std::array<char, 64>> buffers;
  if (image.is_open()) {
    std::cout << image.rdbuf();
  }
  std::cout << std::endl;
  return 0;
}
