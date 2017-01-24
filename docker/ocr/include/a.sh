#!/bin/sh
cd /tmp
tar xfvz /tmp/geckodriver.tar.gz
ln -fs /tmp/geckodriver /usr/bin/geckodriver
#unzip /tmp/chromedriver.zip -d /tmp
#cp /tmp/chromedriver /usr/bin/chromedriver
cd /opt/share/test
pwd
ls -l
./exec_atest.sh
#if [ $? -eq 0 ]
#then
#  echo "Successfully run template"
#  exit 0
#else
#  echo "Unsuccesfully run template" 
#  exit 1
#fi
#/bin/bash
