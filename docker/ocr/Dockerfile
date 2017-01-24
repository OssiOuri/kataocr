FROM ubuntu:16.10
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gdebi \
    wget
RUN pip3 install robotframework
RUN pip3 install robotframework-xvfb
#get web drivers to /tmp directory, unpack and install later
RUN wget -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.13.0/geckodriver-v0.13.0-linux64.tar.gz 
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN gdebi google-chrome-stable_current_amd64.deb
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/2.27/chromedriver_linux64.zip
RUN apt-get update && apt-get install -y \
    python \
    python-pip \
    curl \
    xvfb \
    unzip \
    firefox
RUN pip install robotframework
RUN pip install robotframework-xvfb
RUN pip install robotframework-selenium2Library
ADD ./include/a.sh /
CMD /a.sh
