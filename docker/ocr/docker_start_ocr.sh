#!/bin/sh
sudo docker run -P -v /var/jenkins_home/workspace/pipefirst:/opt/share --network=host --name ocrbuntu ocrbuntu
sudo docker rm ocrbuntu
