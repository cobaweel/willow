import serial, getopt, sys, urllib2

# Set defaults
port_name = 0
url = "http://localhost:8000/put"

# Read command line
switches, _ = getopt.getopt(sys.argv[1:], "p:u:")
for switch, arg in switches:
  if switch == "-p":
    if arg.isdigit():
      port_name = int(arg)
    else:
      port_name = arg
  if switch == "-u":
    url = arg

# Open serial port
port = serial.Serial(port_name)
port.open()

# Relay serial port data to url
while True:
  byte = port.read(1)
  urllib2.urlopen(conf.url, byte)
