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

from escpos.printer import Usb
import datetime
p = Usb(0x1fc9, 0x2016)

p.text("0"*80)

# p.text("University Pizza\n")
# p.text("123 Main Street\n")
# p.text("(123) 456-7890\n\n")

# # Print current date and time
# p.text("Date: " + str(datetime.datetime.now()) + "\n\n")

# # Print order details
# p.text("Order Details\n")
# p.text("-------------\n")
# p.text("Large Pepperoni Pizza\n")
# p.text("Medium Coke\n")
# p.text("Garlic Bread\n\n")

# # Print total
# p.text("Total: $20.00\n")

# Cut the receipt and eject it from the printer
p.cut()
