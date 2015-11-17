/exit 0/i\
# Wait until we have an IP address then display on Joey\
( # run in background so we don't delay boot process\
  until [ $(hostname -I) ]; do sleep 1; done\
  python /usr/local/sbin/ip_disp.py\
) &\

