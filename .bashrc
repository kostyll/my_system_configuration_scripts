export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
export PROJECT_HOME="/home/andrew/workspace"
export COLORTERM="urxvt"
export PATH=$PATH:/home/andrew/mscripts/
export PATH=$PATH:/home/andrew/workspace/job_1/gae/google_appengine/
export PYTHONPATH=/home/andrew/workspace/job_1/gae/google_appengine:/home/andrew/workspace/job_1/mathengine:/home/andrew/workspace/job_1/mathengine/app:$PYTHONPATH
alias show_my_ip="wget -q -O /tmp/getmyip.php http://php.kichrum.org.ua/getmyip.php; cat /tmp/getmyip.php; echo ""; rm /tmp/getmyip.php"

switchkeys-activate

