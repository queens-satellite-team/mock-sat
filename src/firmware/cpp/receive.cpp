#include <stdio.h>
#include <string.h>
#include <iostream>

#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <unistd.h>
#include <sys/file.h>
#include <stdexcept>

int main() {
  int serial_port = open("/dev/ttyS9", O_RDWR);

  struct termios tty;
  memset(&tty, 0, sizeof tty);

  if (tcgetattr(serial_port, &tty) != 0) {
    printf("Error %i from tcgetattr: %s\n", errno, strerror(errno));
  }

  tty.c_cflag &= ~PARENB;
  tty.c_cflag &= ~CSTOPB;
  tty.c_cflag |= CS8;
  tty.c_cflag &= ~CRTSCTS;
  tty.c_cflag |= CREAD | CLOCAL;

  tty.c_lflag &= ~ICANON;
  tty.c_lflag &= ~ECHO;
  tty.c_lflag &= ~ECHOE;
  tty.c_lflag &= ~ECHONL;
  tty.c_lflag &= ~ISIG;
  tty.c_iflag &= ~(IXON | IXOFF | IXANY);
  tty.c_iflag &= ~(IGNBRK|BRKINT|PARMRK|ISTRIP|INLCR|IGNCR|ICRNL);

  tty.c_oflag &= ~OPOST;
  tty.c_oflag &= ~ONLCR;

  tty.c_cc[VTIME] = 10;
  tty.c_cc[VMIN] = 0;

  cfsetispeed(&tty, B115200);
  cfsetospeed(&tty, B115200);

  if (tcsetattr(serial_port, TCSANOW, &tty) != 0) {
    printf("Error %i from tcsetattr: %s\n", errno, strerror(errno));
  }

  if (flock(serial_port, LOCK_EX | LOCK_NB) == -1) {
    throw std::runtime_error("Serial port with  file descriptor " +
        std::to_string(serial_port) + " is already locked by another process.");
  }

  char read_buf[256];
  memset(&read_buf, '\0', sizeof(read_buf));
  int n = 0;
  while (n < 10) {
    n += read(serial_port, &read_buf, sizeof(read_buf));
    std::cout << n << std::endl;
  }

  for (int i = 0; i < 10; ++i) {
    std::cout << read_buf[i];
  }
  std::cout << std::endl;
}
