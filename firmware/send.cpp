/*
 * Parse image into Arduino serial size buffers (64 byte) and send them over
 * serial to the transceiver.
 *
 * The configuration for the serial port is from this tutorial:
 * https://blog.mbedded.ninja/programming/operating-systems/linux/linux-serial-ports-using-c-cpp/
 *
 * For more information about the termios options, read here:
 * https://www.cmrr.umn.edu/~strupp/serial.html#3_1
 */
#include <stdio.h>
#include <termios.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>
#include <unistd.h>

void print_err(int err) { printf("%s\n", strerror(err)); }

int main(int argc, char *argv[]) {
  if (argc <= 1) {
    printf("Missing serial port i.e. send /dev/ttyS8\n");
    return -1;
  }

  FILE *file_stream = fopen("../img/sent.jpg", "r");
  if (file_stream == NULL) {
    printf("No such file or directory\n");
    return -1;
  }

  int serial_fd = open(argv[1], O_RDWR | O_NOCTTY | O_NDELAY);
  if (serial_fd == -1) {
    print_err(errno);
    return -1;
  }
  struct termios tty;
  memset(&tty, 0, sizeof tty);

  if (tcgetattr(serial_fd, &tty) != 0) {
    printf("Error %i from tcgetattr: %s\n", errno, strerror(errno));
  }

  tty.c_cflag &= ~PARENB; // clear parity bit, disabling parity
  tty.c_cflag &= ~CSTOPB; // clear stop field only one stop bit used in comm.
  tty.c_cflag |= CS8; // 8 bits per byte
  tty.c_cflag &= ~CRTSCTS // disable hardware flow contorl (RTS/CTS)
  tty.c_cflag |= CREAD | CLOCAL; // turn on read and ignor control lines
  tty.c_cflag &= ~ICANON; // disable canonical mode
  tty.c_cflag &= ~ECHO; // disable echo
  tty.c_cflag &= ~ECHOE; // disable erasure
  tty.c_cflag &= ~ECHONLY; // disable new-line echo
  tty.c_lflag &= ~ISIG; // diable interpretation of INTR, QUIT and SUSP

  const int ARDUINO_BUFFER_SIZE = 64, CHECKSUM_SIZE = 1, HEADER_SIZE = 2;//bytes
  char *buf[ARDUINO_BUFFER_SIZE];

  int total_bytes = 0, total_serial_bytes = 0;
  while (!feof(file_stream)) {
    int read_bytes = fread(buf, sizeof(char), ARDUINO_BUFFER_SIZE, file_stream);

    if (ferror(file_stream)) {
      printf("There was an error\n");
      return -1;
    }

    int serial_bytes = write(serial_fd, buf, read_bytes);

    printf("%d\n", serial_bytes);
    if (serial_bytes == -1) {
      print_err(errno);
      return -1;
    }

    total_bytes += read_bytes;
    total_serial_bytes += serial_bytes;

    usleep(50);
  }
  printf("Bytes read from image: %d\n", total_bytes);
  printf("Bytes sent on serial: %d\n", total_serial_bytes);
  fclose(file_stream);
return 0;
}
