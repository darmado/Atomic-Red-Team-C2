#!/bin/bash

check_internet() {
	wget -q --tries=10 --timeout=10 --spider https://github.com
	if [[ $? -eq 0 ]]; then
        	echo "Connection Found"
	else
        	printf "NO Connection Found\nExiting...\n"
		exit 0
	fi	
}

debian_install() {
	sudo apt-get install git python3.7 python3-pip wget unzip -y
	git clone https://github.com/blackbotinc/Atomic-Red-Team-Intelligence-C2.git
	cd artic2
	pip3 install -r requirements.txt
	sudo wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip -O /usr/local/sbin/ngrok
	sudo unzip /usr/local/sbin/ngrok
	sudo chmod a+x /usr/local/sbin/ngrok

}

arch_install() {
	echo "y" | sudo pacman -S git python-pip python3 wget unzip
	check_internet
	git clone https://github.com/blackbotinc/Atomic-Red-Team-Intelligence-C2.git
	cd artic2
	pip3 install -r requirements.txt
	sudo wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip -O /usr/local/sbin/ngrok
	sudo unzip /usr/local/sbin/ngrok
	sudo chmod a+x /usr/local/sbin/ngrok
}

check_internet
if [[ $(which apt-get) == "/usr/bin/apt-get" ]]
then
	debian_install
elif [[ $(which pacman) == "/usr/bin/pacman" ]]
then
	arch_install
fi

