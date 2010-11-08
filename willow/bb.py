import serial, getopt, sys, urllib2

# Set defaults
g_port_name = 0
g_host = "localhost:8000"
g_tag = "serial"

# Read command line
switches, _ = getopt.getopt(sys.argv[1:], "p:h:t:")
for switch, arg in switches:
  if switch == "-p":
    if arg.isdigit():
      g_port_name = int(arg)
    else:
      g_port_name = arg
  if switch == "-h":
    g_host = arg
  if switch == "-t":
    g_tag = arg

# Open serial port
port = serial.Serial(g_port_name)
port.open()

def shout(label, obj):
  print "%-30s: %s" % (label, obj)

shout("Reading data from port", g_port_name)
shout("Posting data to host", g_host)
shout("Using tag", g_tag)

# Relay serial port data to url
while True:
  byte = port.read(1)
  msg = '{ "tag": "%s", "byte": "%s" }' % (g_tag, byte)
  shout("Received ", byte)
  try:
    urllib2.urlopen("http://" + g_host + "/put", msg)
    shout("Posted", msg)
  except urllib2.URLError:
    shout("ERROR - no willow on", g_host)

