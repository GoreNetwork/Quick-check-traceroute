# Quick-check-traceroute
Quick check traceroute

Copy your list of devices into "the_tracert.txt", this the program will pull any IPs out (so you can just paste a tracert in here) 
Update username/password in the program run the program (there are 2)
The program SSHs into each device, pulls interface info and CPU info.  It then makes an HTTP page that will show the BW used, and error rate of each interface (with decent usage).  Devices with more than .5% error rates will show up in red.
