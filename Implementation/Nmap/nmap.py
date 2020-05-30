#!/bin/bash

ip_range(){
#Removing the files if they exist
if ( ls "ip_add.txt" || ls "ip_sub.txt" || ls "ip_full.txt" );
then
  rm ip_add.txt
  rm ip_sub.txt
  rm ip_full.txt
  echo "files have been removed !!"
else 
  echo "Files don't exist continuing..."
fi

#Collecting the ip address subnet and adding the range to be used in nmap
sleep 2
ip add > ip_add.txt 
cat ip_add.txt | grep wlan0 | grep inet | tr -d " " | cut -b 5-14 > ip_sub.txt
(cat ip_sub.txt && echo "1-255" )> ip_full.txt
subnet="$( awk 'BEGIN { ORS = " " } { print }' ip_full.txt | tr -d ' ')"
echo $subnet
sleep 2

#removing file if exists to prevent conflicts
if (ls "simp_nmap.txt" || ls "vuln_nmap.txt")
then
 rm simp_nmap.txt
 rm vuln_nmap.txt
echo "Ready to Scan ..."
sleep 1
fi
#Conducting a simple nmap scan
echo "---------- Simple nmap scan -----------"
nmap $subnet -sn simp_nmap.txt

#conducting a vulnerability test using a pre-defined script
echo "--------- Vulnerability Scan ----------"
echo "Please wait till nmap scan is done !...."
nmap -sV -oN vuln_nmap.txt --script vuln $subnet 
}

ip_range
