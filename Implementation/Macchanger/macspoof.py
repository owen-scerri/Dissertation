#!/bin/bash

#function
function startmac {
#removing previous used files 
rm selected_ap.txt
rm available_ap-*.csv
rm available_client-*.csv

#setting up the adapter to monitor mode
echo "Setting up Wlan0 into montior mode."
airmon-ng start wlan0
sleep 3

#Discovering available AP's
function disc_net {
xterm -hold -e "timeout 3s airodump-ng -w available_ap --output-format csv wlan0mon " &
echo "Break the script when you see the desired AP"
sleep 4
cat available_ap-01.csv
echo "Please Enter the desired access point."
read AP
echo "The AP selected is :"
ap_selected=$(cat available_ap-01.csv | grep -m1 $AP) 
echo $ap_selected >> selected_ap.txt

bssid=$(cat selected_ap.txt | head -1 | cut -d " " -f1 | tr "," " ")
echo "BSSID is : $bssid"
}
#running the function 
disc_net
#verifying if correct information is entered
echo "is this correct ? (Y/N)"
read verif
if [ $verif == N ]; then
  bssid="" 
   disc_net 
else
   echo "Continuing ...."
fi

#airodump on bssid to discover clients.
xterm -hold -e "timeout 30s airodump-ng --bssid $bssid -w available_client --output-format csv wlan0mon"
client=$(cat available_client-01.csv | grep -m2 $bssid | cut -d " " -f1 | tail -1 | tr "," " ")
echo "The Mac address selected is $client"

#macchanger
echo "-------------- Setting up wlan0 Please wait ! -------------"
airmon-ng stop wlan0mon
macchanger -m $client wlan0
ifconfig wlan0 up
macchanger -s wlan0
echo "-------------- Mac has been Changed ! -----------------"
sleep 2
#Showing that password has been changed 
echo "The new configuration is : $client "
ifconfig wlan0
exit
}


#Start of Script option to revert back to origianl MAC
echo "Do you want to change back to original Mac ? (Y/N)"
while :
do
 read option
 case $option in 
	Y)
		macchanger -p wlan0
		break
		;;
	N)
		echo "------ Starting MACChanger -------"
		startmac
 esac
done

