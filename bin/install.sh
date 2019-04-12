#!/bin/bash

#defining some color variables
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${GREEN}#########################################################################"
echo -e "########################${YELLOW} PLEASE READ BELOW ${GREEN}##############################"
echo -e "####################${YELLOW} Script creator: Raoul Dinmohamed ${GREEN}###################"
echo -e "####################${YELLOW} Contact: hakan.kece@hva.nl ${GREEN}#########################"
echo -e "######${YELLOW} Place of creation: Amsterdam University of Applied Sciences ${GREEN}######"
echo -e "#########################################################################"${YELLOW}
echo ""
echo -e "                   This script will do the following:"
echo ""
echo -e "${GREEN}[*]${YELLOW} Update the VM to the most recent and stable version"
echo ""
echo -e "${GREEN}[*]${YELLOW} Install the minimum required packages"
echo ""
echo -e "${GREEN}[*]${YELLOW} Install the minimum required versions of modules"
echo ""
echo -e "${GREEN}[*]${YELLOW} Configure the virtual machine for the application"
echo ""
echo -e "${GREEN}[*]${YELLOW} Create user-friendly commands for utilizing the application"
echo ""
echo -e "${GREEN}########################################################################"
echo -e "#########${YELLOW} Contact the script creator for more information ${GREEN}##############"
echo -e "#####################${YELLOW} ©2019 All Rights Reserved ${GREEN}########################"
echo -e "########################################################################${NC}"
echo ""
echo -e "Are you sure you want to continue? (${GREEN}y/${RED}n${NC})"
read answer
if [ $answer == y ]
then
echo -e "${GREEN}The installation has started. This might take several minutes...${NC}"

#change Color to green #2
tput setaf 2;

#install min. required modules
apt-get update -y
pip3 install Flask
pip3 install pymongo
pip3 install pandas
pip3 install matplotlib
pip3 install pyyaml
pip3 install pyOpenSSL
apt-get install python-tk
apt install mongodb -y
service mongodb start

apt-get install python3-tk -y

#install konsole 
apt install -y konsole 

echo -e "${Yellow}Creating user-friendly commands"

#creating stop command
rm -rf /usr/local/bin/stopsniffer
touch /usr/local/bin/stopsniffer
cat stopsniffer.sh >> /usr/local/bin/stopsniffer
chmod +x /usr/local/bin/stopsniffer

#creating start command
rm -rf /usr/local/bin/startsniffer
touch /usr/local/bin/startsniffer
cat startsniffer.sh >> /usr/local/bin/startsniffer
chmod +x /usr/local/bin/startsniffer

#create web app command
rm -rf /usr/local/bin/startwebapp
touch /usr/local/bin/startwebapp
cat startwebapp.sh >> /usr/local/bin/startwebapp
chmod +x /usr/local/bin/startwebapp

echo -e "${GREEN} Commands succesfully created!"


echo ""
echo ""
echo -e "${GREEN}The packages have been successfully installed${NC}"
echo ""
echo -e "${GREEN}Try running the sniffer by typing: ${YELLOW}startsniffer${NC}"
echo ""
echo ""

else
echo -e "${RED}The script has been cancelled${NC}"
fi
