#! /bin/sh
#
# Install Joey IP display code, to run on boot
#
#   v1.0    17/11/15
#
#   David Meiklejohn
#   Gooligum Electronics
#

echo "Installing Joey IP display code"

# copy Python script to /usr/local/sbin
cp ip_disp.py /usr/local/sbin
chmod 755 /usr/local/sbin/ip_disp.py

# backup /etc/rc.local
TODAY=$(date +%y%m%d)
cp /etc/rc.local /etc/rc.local.bak$TODAY

# insert IP display lines into /rc.local
sed -f insert-ip_disp.sed /etc/rc.local.bak$TODAY > /etc/rc.local

echo "done!"

