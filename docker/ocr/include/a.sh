#!/bin/sh
cd /tmp
tar xfvz /tmp/geckodriver.tar.gz
ln -fs /tmp/geckodriver /usr/bin/geckodriver
#unzip /tmp/chromedriver.zip -d /tmp
#cp /tmp/chromedriver /usr/bin/chromedriver
/opt/share/test/exec_atest.sh
if [ $? -eq 0 ]
then
  echo "Successfully run exec_atest"
  exit 0
else
  echo "Unsuccesfully run exec_atest" 
  exit 1
fi
