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

p = Usb(0x1FC9, 0x2016)

print(p.paper_status())
# p.cashdraw(2)
# p.image("./assets/10c.png", fragment_height=100, center=True)
# Print the header
p.set(align="center", font="a", custom_size=True, width=3, height=3, bold=True)
p.text("UNIVERSITY PIZZA\n\n")
p.set(align="center", font="b", custom_size=True, width=2, height=1)
p.text("1457 University Ave West\n")
p.text("Windsor, Ontario, N9B1B8\n")
p.text("226-782-9600\n")
p.text("\n")

# Print the order details
p.set(align="right", font="a", custom_size=True, width=1, height=1, bold=False)
p.text("Date: 10-May-2023\n")
p.text("Time: 06:23:29PM\n")
p.text("\n")

# Print the items
p.set(align="center", font="a", custom_size=True, width=1, height=1, bold=False)
spacing = 40
p.text("{:<{}}{}".format("1 Large Pepperoni Pizza", spacing, "$12.99\n"))
p.text("{:<{}}{}".format("1 Medium Mushroom Pizza", spacing, "$10.99\n"))
p.text("{:<{}}{}".format("2 Cans of Soda", spacing, "$2.50\n"))
p.text("\n")

# Print the totals
p.set(align="center", font="a", custom_size=True, width=1, height=1, bold=True)
spacing = 30
p.text("{:<{}}{}".format("Method:", spacing, "cash\n"))
p.text("{:<{}}{}".format("Subtotal:", spacing, "$26.48\n"))
p.text("{:<{}}{}".format("Discount", spacing, "-$1.25\n"))
p.text("{:<{}}{}".format("Tax:", spacing, "$2.12\n"))
p.text("{:<{}}{}".format("Total:", spacing, "$28.60\n"))
p.text("\n")

# Print a thank you message
p.set(align="center", font="a", custom_size=True, width=1, height=1, bold=False)
p.text("Thank you for your business!\n")
p.cut()

# close the connection to the printer
p.close()
