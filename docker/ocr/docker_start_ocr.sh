#!/bin/sh
docker run -P -v /var/jenkins_home/workspace/pipefirst:/opt/share --network=host --name ocrbuntu ocrbuntu
docker rm ocrbuntu
