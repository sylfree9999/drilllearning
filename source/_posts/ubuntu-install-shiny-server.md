---
title: Install R Shiny Server in Ubuntu
date: 2018-05-09 16:36:38
tags: [Ubuntu, Shiny]
---

* Install Python
```
sudo apt-get update
sudo apt-get -y upgrade
#type python3 check if python3 is installed
sudo apt-get install -y python3-pip
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
sudo apt-get install gfortran
nano ~/.bashrc
#type on the top of the file
alias python=python3
source ~/.bashrc
```


* Install Java
```
sudo apt-get install default-jre
sudo apt-get install default-jdk
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
```

* Setting JAVA_HOME
```
sudo update-alternatives --config java
sudo nano /etc/environment
JAVA_HOME="/usr/lib/jvm/java-8-oracle"
source /etc/environment
echo $JAVA_HOME
```


* Install R from source and X11
```

sudo apt-get install libcurl4-openssl-dev
#install x11
sudo apt-get install xvfb xauth xfonts-base
#Xvfb :0 -ac -screen 0 1960x2000x24 &
#then set Sys.setenv("DISPLAY"=":0") on top of ui.R

#install cairo
sudo apt-get build-dep cairo
sudo apt-get install libcairo2-dev
```
#### If you choose to use cairo, put `options(bitmapType='cairo')` on top of the server.R or put it in the Rprofile so that all sessions will read this configuration. [https://stackoverflow.com/questions/17243648/cant-display-png]

```
wget https://mirrors.tuna.tsinghua.edu.cn/CRAN/src/base/R-3/R-3.5.0.tar.gz
tar xzvf R-3.5.0.tar.gz
cd R-3.5.0
./configure --with-readline=no --with-libtiff --with-libjpeg --with-libpng --with-x --with-cairo
make
make check
make install

```

* Rprofile
At startup, R will source the **RProfile.site** file.
Then look for a .Rprofile file to source in the current working directory.
Not found, it will look for on in ~/.Rprofile.
There are two special functions you can put:
	* **.First()** will run at the start of the R session
	* **.Last()** will run at the end of the session

Check where is the RHOME



Sample Rprofile.site file
```
# Things you might want to change
# options(papersize="a4") 
# options(editor="notepad") 
# options(pager="internal")

# R interactive prompt 
# options(prompt="> ")
# options(continue="+ ") 

# to prefer Compiled HTML help 
options(chmhelp=TRUE) 
# to prefer HTML help 
# options(htmlhelp=TRUE) 

# General options 
options(tab.width = 2) 
options(width = 130)
options(graphics.record=TRUE) 
options(bitmapType='cairo')

.First <- function(){
 #library(Hmisc)
 #library(R2HTML)
 cat("\nWelcome at", date(), "\n") 
}

.Last <- function(){ 
 cat("\nGoodbye at ", date(), "\n")
}
```



* Install R Packages for Shiny
```
sudo apt-get install libxml2-dev

sudo su - -c "R -e \"install.packages(c('shiny','shinydashboard','shinyjs','quanteda', 'dygraphs', 'rhandsontable', 'keras','DEoptim','RSQLite','reshape2','mlbench','future','promises','shinyWidgets','devtools','Hmisc','XML','DT'), repos='https://mirrors.tuna.tsinghua.edu.cn/CRAN/')\""


sudo su - -c "R -e \"devtools::install_github('madlogos/recharts')\""
sudo su - -c "R -e \"devtools::install_github('lchiffon/REmap')\""

```

* In order to use shinyjs, install V8
```
cd /usr/local/lib/R
sudo chmod o+w site-library
sudo apt-get install -y libv8-3.14-dev
R
install.packges("V8")
```

* Install keras(h5py),tensorflow
```
sudo apt-get install python-pip3 python-virtualenv
sudo pip3 install tensorflow -i https://pypi.tuna.tsinghua.edu.cn/simple
sudo pip3 install keras -i https://pypi.tuna.tsinghua.edu.cn/simple
```

* Install Shiny Server, check this page[https://www.rstudio.com/products/shiny/download-server/] for the newest package
```
sudo apt-get install gdebi-core
wget https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.7.907-amd64.deb
sudo gdebi shiny-server-1.5.7.907-amd64.deb
```

* Shiny Server Management
```
start shiny-server / sudo systemctl start shiny-server.service
stop shiny-server  / sudo systemctl stop shiny-server.service
restart shiny-server / sudo systemctl restart shiny-server.service
status shiny-server  / sudo systemctl status shiny-server.service
sudo reload shiny-server /sudo systemctl reload shiny-server.service
```

* Shiny config file
	*	conf: `/etc/shiny-server/shiny-server.conf`
	*	site: `/srv/shiny-server/`
	*	log:  `/var/log/shiny-server.log` or `/var/log/shiny-server/*.log`