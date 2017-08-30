# time-experiments
A collection of time experiment scripts espcially aimed for the Raspberry Pi.

## delay-icmp
```
usage: icmp.py [-h] [-i INTERVAL] host

measures the icmp round-trip time (RTT)

positional arguments:
  host                  host to connect

optional arguments:
  -h, --help            show this help message and exit
  -i INTERVAL, --interval INTERVAL
                        set interval (default 1)
```
## delay-nmea
```
usage: nmea.py [-h] [-d] [-s] nmea_pulse nmea_device pps_pulse pps_device

measures the delay between pps and nmea pulse

positional arguments:
  nmea_pulse     nmea_pulse path
  nmea_device    nmea device path
  pps_pulse      pps_pulse path
  pps_device     pps device path

optional arguments:
  -h, --help     show this help message and exit
  -d, --debug    enable debugging
  -s, --summery  show summery on exit
```
## tvt-udp-server
```
usage: udp_server.py [-h] [-p PORT] directory

udp tvt server receives packets from its clients and records the containing
time vs the local time

positional arguments:
  directory             data path

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  set port number (default 12345)
```
## tvt-udp-client
```
usage: udp_client.py [-h] [-p PORT] [-i INTERVAL] host

udp tvt client sends packets with its time periodically to the server

positional arguments:
  host                  host to connect

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  set port number (default 12345)
  -i INTERVAL, --interval INTERVAL
                        set interval (default 1)
```
## tvt-gpio-server
```
usage: gpio_server.py [-h] [-d] [-p PORT] [-i INTERVAL]
                      [--gpio-station GPIO_STATION]
                      pinout directory

gpio tvt server sends gpio impulses to its clients and records their time vs
local impulse time

positional arguments:
  pinout                output gpio
  directory             data path

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           enable debugging
  -p PORT, --port PORT  udp port (default 12345)
  -i INTERVAL, --interval INTERVAL
                        signal interval (default 1)
  --gpio-station GPIO_STATION
                        path to c gpio station
```
## tvt-gpio-client
```
usage: gpio_client.py [-h] [-d] [-p PORT] [--gpio-netlink]
                      [--gpio-polling GPIO_POLLING]
                      pinin host

gpio tvt client connects to impulse giving server and returns the current time
per udp

positional arguments:
  pinin                 input gpio
  host                  host to connect

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           enable debugging
  -p PORT, --port PORT  udp port (default 12345)
  --gpio-netlink        connect to gpio-netlink.ko
  --gpio-polling GPIO_POLLING
                        path to c gpio polling
```
