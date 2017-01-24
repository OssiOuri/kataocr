#!/bin/sh
sudo docker run -P -v /home/jenkins/ci/workspace/pipefirst:opt/share --network=host --name ocrbuntu ocrbuntu
sudo docker rm ocrbuntu
