#!/bin/sh
sudo docker run -P -v /home/jenkins/ci/workspace/pipefirst:/opt/share --network=host --name ocrbuntu ocrbuntu
return_value=$?
sudo docker rm ocrbuntu
exit $return_value
