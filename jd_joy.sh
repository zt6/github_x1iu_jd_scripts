#!/usr/bin/env bash

## 路径
ShellDir=${QL_DIR:-$(cd $(dirname $0); pwd)}
[[ ${QL_DIR} ]] && ShellJS=js
ScriptsDir=${ShellDir}/scripts
ConfigDir=${ShellDir}/config
FileConf=${ConfigDir}/config.sh
CookieConf=${ConfigDir}/cookie.sh
FileConfSample=${ShellDir}/sample/config.sh.sample
LogDir=${ShellDir}/log
ListScripts=($(cd ${ScriptsDir}; ls *.js | grep -E "j[drx]_"))
ListCron=${ConfigDir}/crontab.list
ListCronLxk=${ScriptsDir}/docker/crontab_list.sh
ListJs=${LogDir}/js.list

## 导入config.sh
function Import_Conf {
  if [ -f ${FileConf} ]
  then
    . ${CookieConf}
    . ${FileConf}
    if [[ ! -s ${CookieConf} ]]; then
      echo -e "请先在Cookie管理中添加一条Cookie...\n"
      exit 1
    fi
  else
    echo -e "配置文件 ${FileConf} 不存在，请先按教程配置好该文件...\n"
    exit 1
  fi
}

## 用户数量UserSum
function Count_UserSum {
  UserSum=0
  for line in `cat $CookieConf`
  do
    ((UserSum++))
    eval Cookie${UserSum}="\"${line}\""
  done
}

## 组合Cookie和互助码子程序
function Combin_Sub {
  CombinAll=""
  if [[ ${AutoHelpOther} == true ]] && [[ $1 == ForOther* ]]; then

    ForOtherAll=""
    MyName=$(echo $1 | perl -pe "s|ForOther|My|")

    for ((m=1; m<=${UserSum}; m++)); do
      TmpA=${MyName}$m
      TmpB=${!TmpA}
      ForOtherAll="${ForOtherAll}@${TmpB}"
    done
    
    for ((n=1; n<=${UserSum}; n++)); do
      for num in ${TempBlockCookie}; do
        [[ $n -eq $num ]] && continue 2
      done
      CombinAll="${CombinAll}&${ForOtherAll}"
    done

  else
    for ((i=1; i<=${UserSum}; i++)); do
      for num in ${TempBlockCookie}; do
        [[ $i -eq $num ]] && continue 2
      done
      Tmp1=$1$i
      Tmp2=${!Tmp1}
      CombinAll="${CombinAll}&${Tmp2}"
    done
  fi

  echo ${CombinAll} | perl -pe "{s|^&||; s|^@+||; s|&@|&|g; s|@+&|&|g; s|@+|@|g; s|@+$||}"
}

## 组合Cookie、Token与互助码
function Combin_All {
  export JD_COOKIE=$(Combin_Sub Cookie)
}

## 申明全部变量
function Set_Env {
  Count_UserSum
  Combin_All
}


## 正常运行单个脚本
function Run_Normal {
  Import_Conf $1 && Detect_Cron && Set_Env
  
  FileNameTmp1=$(echo $1 | perl -pe "s|\.js||")
  FileNameTmp2=$(echo $1 | perl -pe "{s|jd_||; s|\.js||; s|^|jd_|}")
  SeekDir="${ScriptsDir} ${ScriptsDir}/backUp ${ConfigDir}"
  FileName=""
  WhichDir=""

  for dir in ${SeekDir}
  do
    if [ -f ${dir}/${FileNameTmp1}.js ]; then
      FileName=${FileNameTmp1}
      WhichDir=${dir}
      break
    elif [ -f ${dir}/${FileNameTmp2}.js ]; then
      FileName=${FileNameTmp2}
      WhichDir=${dir}
      break
    fi
  done
  
  if [ -n "${FileName}" ] && [ -n "${WhichDir}" ]
  then
    [ $# -eq 1 ] && Random_Delay
    LogTime=$(date "+%Y-%m-%d-%H-%M-%S")
    LogFile="${LogDir}/${FileName}/${LogTime}.log"
    [ ! -d ${LogDir}/${FileName} ] && mkdir -p ${LogDir}/${FileName}
    cd ${WhichDir}
    node ${FileName}.js 2>&1 | tee ${LogFile}
  else
    echo -e "\n在${ScriptsDir}、${ScriptsDir}/backUp、${ConfigDir}三个目录下均未检测到 $1 脚本的存在，请确认...\n"
    Help
  fi
}

Import_Conf $1 && Set_Env

node /ql/scripts/jd_joy_reward.js

while [  $(date "+%S") -lt 55  ]
do
  sleep 0.01
done

for ((a=1; a <= 10; a++))
do
    node /ql/scripts/jd_joy_reward.js &
    sleep 0.3
done

while [  $(date "+%S") -lt 58  ]
do
  sleep 0.01
done

for ((a=1; a <= 15; a++))
do
    node /ql/scripts/jd_joy_reward.js &
    sleep 0.2
done

if [ $(date "+%H") -ge 16 ]; then
  export JD_JOY_REWARD_NAME="20"
fi

node /ql/scripts/jd_joy_reward.js

sleep 10
