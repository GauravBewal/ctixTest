#!/bin/bash
set -e
python3 --version
pip3 freeze

cd /git/ctix_tests
apt-get install -y sudo
JENKINS_GID=997
JENKINS_GROUP=jenkins
JENKINS_USER=jenkins
JENKINS_UID=997

groupadd -g ${JENKINS_GID} ${JENKINS_GROUP}
useradd -u ${JENKINS_UID} -g ${JENKINS_GID} -d /home/${JENKINS_USER} -m ${JENKINS_USER}

cat >> /etc/sudoers <<EOF
Defaults:root !requiretty
Defaults:${JENKINS_USER} !requiretty
${JENKINS_USER} ALL=(ALL) NOPASSWD: ALL
EOF
#chown -R ${JENKINS_USER}:${JENKINS_GROUP} /git
#chown ${JENKINS_USER}:${JENKINS_GROUP} /git/ctix_tests
chmod 777 -R /git

sudo -iH -u ${JENKINS_USER} "$@"
google-chrome --version
firefox -v

# Pass Display variable while running the docker
echo "Docker Display is: "$DISPLAY
Xvfb $DISPLAY -screen 0 1920x1200x16 &
# Experimenting x11vnc -passwd TestVNC -display :10 -N -forever & 1366x768x16


# We should run it as a normal user and not root, Chromedriver requests the tests to be executed as normal user.
su - jenkins -c "export PYTHONPATH=/git/ctix_tests; cd /git/ctix_tests; [ -f /git/ctix_tests/env.sh ] && . /git/ctix_tests/env.sh;"
