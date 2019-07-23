#include <algorithm>
#include <ctype.h>
#include <fcntl.h>
#include <stdexcept>
#include <stdio.h>
#include <stdlib.h>
#include <sstream>
#include <string>
#include <string.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <unistd.h>

#define THROW(fmt, ...)                                     \
  do {                                                      \
    std::string msg;                                        \
    char errMsg[2048];                                      \
    sprintf(errMsg, "Exception occured! file=%s line=%d: "  \
            "err=%d errstr='%s' ",                          \
            __FILE__, __LINE__, errno, strerror(errno));    \
    msg += errMsg;                                          \
    sprintf(errMsg, fmt, ##__VA_ARGS__);                    \
    msg += errMsg;                                          \
    throw std::runtime_error(msg);                          \
  } while (0)

#define ASSERT(check, fmt, ...)               \
  do {                                        \
    if (!(check))  THROW(fmt, ##__VA_ARGS__); \
  } while (0)

void showHelp() {
  printf("USAGE:\n"
         "  readreg [-h] <address> [<address> ...]\n"
         "    -h         Print this help and exit\n"
         "    <address>  Address of the register to be read.\n"
         "               Both base10 and base16 types are allowed, provided\n"
         "               base16 numbers have a '0x' prefix.\n");
}

std::string tolower(const std::string& in) {
  std::string res(in);
  std::transform(res.begin(), res.end(), res.begin(),
                 [](unsigned char c) { return std::tolower(c); });
  return res;
}

unsigned long readReg(unsigned long addr) {
  constexpr unsigned long MmapSize = 4096UL;
  constexpr unsigned long MmapMask = MmapSize - 1;
  printf("Fdsfdsfdfdsf 0x%0lx\n", addr);
  auto fd = open("/dev/mem", O_RDWR | O_SYNC);
  ASSERT(fd == -1, "Failed to open '/dev/mem'");
  char* baseAddr = (char*)mmap(0, MmapSize, PROT_READ, MAP_SHARED, fd,
                               addr & ~MmapMask);
  ASSERT(baseAddr == (char*)-1, "Failed to 'mmap' for addr=0x%0lx", addr);
  printf("Fdsfdsfdfdsf fw4ew\n");
  char* tmpAddr = baseAddr + (addr & MmapMask);
  printf("fdsfdsfdsfdsfdsfdsfds\n");
  auto val = *(volatile unsigned long*)tmpAddr;
  printf("423ewrfewf\n");
  ASSERT(munmap(baseAddr, MmapSize) == -1,
         "Failed to 'munmap' for addr=0x%08lx", addr);
  close(fd);
  printf("Fdsfdsfdfdsf  wrtewfdesrtfd\n");
  return val;
}

int main(int argc, char** argv) {
  if (argc < 2) {
    showHelp();
    return -1;
  }
  if (!strcmp(argv[1], "-h")) {
    showHelp();
    return 0;
  }
  for (int i = 1; i < argc; ++i) {
    std::string addrStr(argv[i]);
    addrStr = tolower(addrStr);
    int base = 10;
    if (addrStr.size() > 2 && addrStr[0] == '0' && addrStr[1] == 'x') {
      base = 16;
      addrStr = addrStr.substr(2);
    }
    auto addr = (unsigned long)std::stol(addrStr, 0, base);
    printf("address:0x%08lx val:0x%08lx\n", addr, readReg(addr));
  }
  return 0;
}
