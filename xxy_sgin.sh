#!/bin/bash

function rand(){
    min=$1
    max=$(($2-$min+1))
    num=$(date +%s%N)
    echo $(($num%$max+$min))
  }
rnd=$(rand 10 22)
sleep "$rnd"m

count_line=`wc -l /opt/check_in/info.txt |awk '{print $1}'`

for int in $( seq 1 $count_line )
do
        account_data=""
        next_line=`sed -n "$int,"$int"p" /opt/check_in/info.txt`
        for i in `echo $next_line`
        do
                account_data[0]=`echo $i |awk -F "[~]" '{print $1}'`
                account_data[1]=`echo $i |awk -F "[~]" '{print $2}'`
                account_data[2]=`echo $i |awk -F "[~]" '{print $3}'`
                account_data[3]=`echo $i |awk -F "[~]" '{print $4}'`
                account_data[4]=`echo $i |awk -F "[~]" '{print $5}'`
        done

        account=`echo ${account_data[0]}`
        password=`echo ${account_data[1]}`
        address=`echo ${account_data[2]}`
        longitude=`echo ${account_data[3]}`
        latitude=`echo ${account_data[4]}`

        login_url='https://api.xixunyun.com/login/api?platform=android&version=3.3.3'
        data="request_source=3&account=$account&password=$password&school_id=222"
        Header="Content-Type:application/x-www-form-urlencoded"
        singin=`curl -s -H $Header -d $data -X POST $login_url |python -m json.tool`
        code=`echo "$singin" |jq '.code'`
        message=`echo "$singin" |jq '.message'`

        if [ $code == '20000' ]; then
                token=`echo "$singin" |jq '.data.token'|sed 's/\"//g'`
                #echo $token
                user_name=`echo "$singin"|jq '.data.user_name'`
                echo "$user_name"
        else
                echo "$message"
        fi

        check_in_data="sign_type=0&address=$address&longitude=$longitude&latitude=$latitude"
        check_in_url="https://api.xixunyun.com/signin?platform=android&version=3.3.3&token=$token"
        check_in_res=`curl -s -H $Header -d $check_in_data -X POST $check_in_url |python -m json.tool`
        #echo $check_in_url
        echo $check_in_res |jq '.message'

        sleep_space=$( rand 45 59 )

        if [ $int == $count_line ]; then
                exit 0
        else
                sleep "$sleep_space"s
        fi

done
