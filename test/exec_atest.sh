#!/bin/sh
echo "called exec_atest.sh"
python --version
robot --version
python -m robot --outputdir ./output bigdigit.robot
