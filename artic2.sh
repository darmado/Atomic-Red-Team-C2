#!/bin/bash

# ARTiC2 Controller
# Help: ./artic2.sh --help

check_root() {
	if [[ $(id -u) != "0" ]]
	then
		printf "\033[91mRun this file as root\n\033[0m";
		exit 0;
	fi
}
check_internet() {
    wget -q --tries=10 --timeout=10 --spider https://github.com;
    if [[ $? -eq 0 ]]
    then
    	echo -e "\033[92mConnection Found\033[0m"
    else
    	printf "\033[91mNo Connection Found\nExiting...\n\033[0m"
	exit 0
    fi
}

debian_install() {
	check_root;
	check_internet;
	echo -e "\033[92mInstalling dependencies\033[0m"
    sudo add-apt-repository ppa:deadsnakes/ppa -y > /dev/null 2>&1;
    sudo apt-get update > /dev/null 2>&1;
    sudo apt-get install git python3.7 python3-pip wget unzip sed xxd libc-bin curl jq perl gawk grep coreutils -y;
    git clone https://github.com/blackbotinc/Atomic-Red-Team-Intelligence-C2.git;
    cd artic2;
    python3.7 -m pip install -r requirements.txt;
    sudo wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip -O /usr/local/sbin/ngrok;
    sudo unzip /usr/local/sbin/ngrok;
    sudo chmod a+x /usr/local/sbin/ngrok;
    export ARTIC2_PATH=$(pwd);
}

arch_install() {
	check_root;
	check_internet;
	echo -e "\033[92mInstalling dependencies\033[0m"
    echo "y" | sudo pacman -S git python-pip python3 wget unzip sed xxd glibc curl jq perl gawk grep coreutils >&- 2>&-1;
    git clone https://github.com/blackbotinc/Atomic-Red-Team-Intelligence-C2.git; cd artic2;
    pip3 install -r requirements.txt;
    sudo wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip -O /usr/local/sbin/ngrok;
    sudo unzip /usr/local/sbin/ngrok;
    sudo chmod a+x /usr/local/sbin/ngrok;
    export ARTIC2_PATH=$(pwd);
}

# Update ARTiC2 with git pull
update() {
    check_env;
    cd $ARTIC2_PATH && git pull origin master> /dev/null 2>&1 && echo -e "\033[92mARTiC2 checked for updates\033[0m" || echo -e "\033[91mARTiC2 failed to check for updates\033[0m";
}

# Check if ARTIC2_PATH is env variable
check_env() {
    if [[ -z ${ARTIC2_PATH} ]]
    then
        echo -e "\033[91mEnvironment variable ARTIC2_PATH not found";
        echo -e "Change directory to artic2 and run \"export ARTIC2_PATH=\$(pwd)\"\033[0m";
        exit 0;
    else
        echo -e "\033[92mEnvironment variable found\033[0m";
    fi
}

start_artic2() {
	check_internet;
    check_env;
	python3 $ARTIC2_PATH/artic2.py wss 127.0.0.1 $2 --port $3 || echo -e "\033[91mFailed to start ARTiC2\033[0m";
}

stop_artic2() {
    check_env;
    check_root;
    path="$ARTIC2_PATH/blackbot/core/wss/pid.txt";
    PID=$(cat $path);
    kill $PID > /dev/null 2>&1 && echo -e "\033[92mKilled process $PID\033[0m" || printf "\033[91mFailed to kill process\nMake sure the ARTiC2 server is running\n\033[0m";
}

# CHECK ARGS
if [[ $1 == "install" ]]
then
	if [[ $(which apt-get) == "/usr/bin/apt-get" ]]
	then
    	debian_install
	elif [[ $(which pacman) == "/usr/bin/pacman" ]]
	then
    	arch_install
	fi

elif [[ $1 == "start" ]]
then
    if [[ $# == 3 ]]
    then
	    start_artic2 "$@"
    else
        echo -e "\033[91mYou provided $# args. 2 args required";
        echo -e "Use \"./artic2.sh --help\" for help\033[0m";
    fi

elif [[ $1 == "stop" ]]
then
	stop_artic2

elif [[ $1 == "update" ]]
then
    update

elif [[ $1 == "--help" || "help" || "-h" ]]
then
    echo "Available arguments:";
    echo "    sudo ./artic2.sh install";
    echo "    ./artic2.sh start <username> <port>";
    echo "    ./artic2.sh stop";

else
    echo -e "Invalid argument, use \"./artic2.sh help\" for help";
fi
