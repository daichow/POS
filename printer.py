# 1fc9:2016
# Bus 003 Device 002: ID 1fc9:2016 NXP Semiconductors Printer-80
# lsusb -vvv -d 1fc9:2016 | grep iInterface
# lsusb -vvv -d 1fc9:2016 | grep bEndpointAddress | grep OUT

# main@main:~/Documents/printer_test$ lsusb -vvv -d 1fc9:2016 | grep iInterface
# Couldn't open device, some information will be missing
#       iInterface              0
# main@main:~/Documents/printer_test$ lsusb -vvv -d 1fc9:2016 | grep bEndpointAddress | grep OUT
# Couldn't open device, some information will be missing
#         bEndpointAddress     0x01  EP 1 OUT
# main@main:~/Documents/printer_test$

# IF YOU GET THE PERMISSIONS ERROR DO THE FOLLOWING
# sudo echo 'SUBSYSTEMS=="usb", ATTRS{idVendor}=="1fc9", ATTRS{idProduct}=="2016", GROUP="users", MODE="0666"' >> /etc/udev/rules.d/80-myusb.rules
# REFRESH UDEV
# sudo udevadm control --reload-rules && sudo udevadm trigger

import sys
import json

# Read JSON data from standard input
json_data = sys.stdin.read()

# Parse JSON data
data = json.loads(json_data)

# Print the lists of strings
print(data["datetime"])

from escpos.printer import Usb
import datetime

p = Usb(0x1FC9, 0x2016)

print(p.paper_status())
if data["cash"] == True:
    p.cashdraw(2)
# p.image("./assets/10c.png", fragment_height=100, center=True)

# HEADER
p.set(align="center", font="a", custom_size=True, width=3, height=3, bold=True)
p.text("UNIVERSITY PIZZA\n\n")
p.set(align="center", font="b", custom_size=True, width=2, height=1)
p.text("1457 University Ave West\n")
p.text("Windsor, Ontario, N9B1B8\n")
p.text("226-782-9600\n")
p.text("\n")

# DATETIME
p.set(align="right", font="a", custom_size=True, width=1, height=1, bold=False)
for d in data["datetime"]:
    p.text(d)

# PRINT ITEMS
p.set(align="center", font="a", custom_size=True, width=1, height=1, bold=False)
for d in data["item"]:
    p.text(d)

## PRINT TOTALS
p.set(align="center", font="a", custom_size=True, width=1, height=1, bold=True)
for d in data["cost"]:
    p.text(d)

#  CLOSING
p.set(align="center", font="a", custom_size=True, width=1, height=1, bold=False)
p.text("Thank you for your business!\n")
p.cut()
p.close()
