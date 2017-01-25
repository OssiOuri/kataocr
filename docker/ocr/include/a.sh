#!/bin/sh
cd /tmp
tar xfvz /tmp/geckodriver.tar.gz
ln -fs /tmp/geckodriver /usr/bin/geckodriver
#unzip /tmp/chromedriver.zip -d /tmp
#cp /tmp/chromedriver /usr/bin/chromedriver
cd /opt/share/test
ls -l
exec_atest.sh
return_value=$?
if [ $return_value -eq 0 ]
then
  echo "Tests passed (exec_atest)"
  exit 0
else
  echo "Test failed (exec_atest)" 
  exit $return_value
fi
