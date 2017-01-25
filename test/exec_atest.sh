#!/bin/sh
echo "called exec_atest.sh mod"
python --version
#robot --version
python -m robot --outputdir ./output bigdigit.robot
