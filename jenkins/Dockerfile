FROM ubuntu:18.04

RUN apt-get update && \
        DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata && \
    apt-get install -y --no-install-recommends build-essential && \
    apt-get install -y software-properties-common \
        python-dev \
        python3-dev \
        python3-tk \
        python3-pip \
        libffi-dev \
        libssl-dev \
        curl \
        libcurl3-dev \
        libxml2-dev \
        libxslt-dev \
        xfonts-100dpi \
        xfonts-75dpi \
        xfonts-scalable \
        xfonts-cyrillic \
        libxrender1 \
        libasound2 \
        libdbus-glib-1-2 \
        libgtk-3-0 \
        xvfb \
        libffi-dev \
        libssl-dev \
        openssh-client \
        git &&\
        apt-get clean \
        jsonschema


RUN python3 -m pip install --upgrade Cython && \
        python3 -m pip install numpy==1.19.5 && \
        python3 -m pip install \
        setuptools==56.1.0 \
        xmlrunner==1.7.7 \
        webdriver-manager \
        urllib3==1.26.4 \
        six==1.16.0 \
        selenium==3.141.0 \
        pytz==2021.1 \
        python-dateutil==2.8.1 \
        configparser==5.0.2 \
        html-testRunner==1.2.1 \
        Pillow==8.3.1 \
        matplotlib==3.3.4 \
        jira==3.1.1 \
        pandas==1.1.5 \
        ordered-set \
        deepdiff \
        jsondiff \
        jsonschema \
        python-docx

RUN apt-get install -y wget
# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#Updating apt to see and install Google Chrome
RUN apt-get -y update
#RUN apt-get install -y google-chrome-stable
RUN apt-get install -yqq unzip curl
#RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/92.0.4515.43/chromedriver_linux64.zip
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

#RUN apt-get -y update && \
#    apt-get install -y gnupg wget curl unzip --no-install-recommends && \
#    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
#    apt-get update -y && \
#    apt-get install -y google-chrome-stable && \
#    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
#    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
#    wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
#    unzip /chromedriver/chromedriver* -d /usr/local/bin/
#RUN chmod 755 /usr/local/bin/chromedriver

##### Install Chromedriver
ARG CHROME_VERSION="109.0.5414.74"

RUN wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /usr/local/bin/
RUN chmod 755 /usr/local/bin/chromedriver

# Check available versions here: https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb

##### install geckodriver and firefox
ARG GECKODRIVER_VERSION="v0.31.0"
#RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
#    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
#    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
#    chmod +x /usr/local/bin/geckodriver && \
#    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

RUN wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz



RUN FIREFOX_SETUP=firefox-setup.tar.bz2 && \
    apt-get purge firefox && \
    wget -O $FIREFOX_SETUP "https://download.mozilla.org/?product=firefox-latest&os=linux64" && \
    tar xjf $FIREFOX_SETUP -C /opt/ && \
    ln -s /opt/firefox/firefox /usr/bin/firefox && \
    rm $FIREFOX_SETUP

RUN apt-get install -y zip unzip
# Experimenting: Execute VNC viewer to check the execution
RUN apt-get install -y ffmpeg
#RUN ffmpeg -version
#RUN apt-get install -y git x11vnc
#EXPOSE 5920



ADD docker_entrypoint.sh /usr/bin/init_build_env
RUN chmod +x /usr/bin/init_build_env

#RUN useradd -m jenkins && echo "jenkins:jenkins" | chpasswd && adduser jenkins sudo
#USER jenkins
#RUN useradd -ms /bin/bash appuser
# Switch to 'appuser'
#USER appuser

ENTRYPOINT ["init_build_env"]

CMD ["bash"]
