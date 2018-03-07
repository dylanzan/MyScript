#! /bin/bash

function checkos(){
    if [ -f /etc/redhat-release ];then
        OS=CentOS
    elif [ ! -z "`cat /etc/issue | grep bian`" ];then
        OS=Debian
    elif [ ! -z "`cat /etc/issue | grep Ubuntu`" ];then
        OS=Ubuntu
    else
        echo "Not support OS, Please reinstall OS and retry!"
        exit 1
    fi
}
# Get version
function getversion(){
    if [[ -s /etc/redhat-release ]];then
        grep -oE  "[0-9.]+" /etc/redhat-release
    else
        grep -oE  "[0-9.]+" /etc/issue
    fi
}

# CentOS version
function centosversion(){
    local code=$1
    local version="`getversion`"
    local main_ver=${version%%.*}
    if [ $main_ver == $code ];then
        return 0
    else
        return 1
    fi
}

function firewall_set(){
    echo "firewall set start..."
    if centosversion 6; then
        /etc/init.d/iptables status > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            iptables -L -n | grep '${Port}' | grep 'ACCEPT' > /dev/null 2>&1
            if [ $? -ne 0 ]; then
                iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport ${Port} -j ACCEPT
                iptables -I INPUT -m state --state NEW -m udp -p udp --dport ${Port} -j ACCEPT
                /etc/init.d/iptables save
                /etc/init.d/iptables restart
            else
                echo "port ${Port} has been set up."
            fi
        else
            echo "WARNING: iptables looks like shutdown or not installed, please manually set it if necessary."
        fi
    elif centosversion 7; then
        systemctl status firewalld > /dev/null 2>&1
        if [ $? -eq 0 ];then
            firewall-cmd --permanent --zone=public --add-port=${Port}/tcp
            firewall-cmd --permanent --zone=public --add-port=${Port}/udp
            firewall-cmd --reload
        else
            echo "Firewalld looks like not running, try to start..."
            systemctl start firewalld
            if [ $? -eq 0 ];then
                firewall-cmd --permanent --zone=public --add-port=${Port}/tcp
                firewall-cmd --permanent --zone=public --add-port=${Port}/udp
                firewall-cmd --reload
            else
                echo "WARNING: Try to start firewalld failed. please enable port ${Port} manually if necessary."
            fi
        fi
    fi
    echo "firewall set completed..."
}

# Run
sshd_config_dir=`find / -name sshd_config`
port_number=`cat /etc/ssh/sshd_config |grep -w 'Port'|awk '{print $2}'`
read -p "plz input a number to sshd_Port: " Port
if [ "$port_number" -eq '22' ]; then
  if [ $Port -ge 1 ] && [ $Port -le 65535 ]; then
    echo $Port
    if [ ! -z "`cat $sshd_config_dir | grep '#Port 22'`" ]; then
      sed -i "s/#Port 22/Port "${Port}"/g" $sshd_config_dir
      firewall_set
      echo 'Successful'
    elif [ ! -z "`cat $sshd_config_dir | grep 'Port 22'`" ]; then
      sed -i "s/22/"${Port}"/g" $sshd_config_dir
      firewall_set
      echo 'Successful'
    fi
  else
    echo 'plz input 1-65535 number!'
  fi
elif [ "$port_number" != '22' ]; then
  echo "$port_number"
  echo "The default port has been changed"
fi
