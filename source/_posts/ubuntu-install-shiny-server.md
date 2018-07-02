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
sudo apt-get install -y build-essential libssl-dev libffi-dev python3-dev
sudo apt-get install -y liblzma-dev  libblas-dev gfortran
nano ~/.bashrc
#type on the top of the file
alias python=python3
source ~/.bashrc
```


* Install Java
```
sudo apt-get install -y default-jre
sudo apt-get install -y default-jdk
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer

or
wget http://download.oracle.com/otn-pub/java/jdk/8u171-b11/512cd62ec5174c3487ac17c61aaa89e8/jdk-8u171-linux-x64.tar.gz?AuthParam=1530518840_9e538c86b030b30acb4afc0f47a60454

mkdir /apps/
tar -zxvf jdk-8u171-linux-x64.tar.gz -C /apps/
vi /etc/profile
export JAVA_HOME=/apps/jdk1.8.0_171
export PATH=$PATH:$JAVA_HOME/bin
source /etc/profile
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

sudo apt-get install -y libcurl4-openssl-dev
#install x11
sudo apt-get install -y xvfb xauth xfonts-base
#Xvfb :0 -ac -screen 0 1960x2000x24 &
#then set Sys.setenv("DISPLAY"=":0") on top of ui.R

#install cairo
sudo apt-get -y build-dep cairo
sudo apt-get install -y libcairo2-dev

```
#### If you choose to use cairo, put `options(bitmapType='cairo')` on top of the server.R or put it in the Rprofile so that all sessions will read this configuration. [https://stackoverflow.com/questions/17243648/cant-display-png]

```
sudo apt-get install libbz2-dev
wget https://mirrors.tuna.tsinghua.edu.cn/CRAN/src/base/R-3/R-3.5.0.tar.gz
tar xzvf R-3.5.0.tar.gz
cd R-3.5.0
sudo -s
./configure --with-readline=no --with-libtiff --with-libjpeg --with-libpng --with-x --with-cairo
make
make check
make install

```
Check capabilities:
```R
R
capabilities()
```

* Rprofile
At startup, R will source the **RProfile.site** file.
Then look for a .Rprofile file to source in the current working directory.
Not found, it will look for on in ~/.Rprofile.

[https://www.r-bloggers.com/fun-with-rprofile-and-customizing-r-startup/]
```
In the absence of any command-line flags being used, when R starts up, it will “source” (run) the site-wide R startup configuration file/script if it exists. In a fresh install of R, this will rarely exist, but if it does, it will usually be in ‘/Library/Frameworks/R.framework/Resources/etc/’ on OS X, ‘C:Program FilesRR-***etc’ on Windows, or ‘/etc/R/’ on Debian. Next, it will check for a .Rprofile hidden file in the current working directory (the directory where R is started on the command-line) to source. Failing that, it will check your home directory for the .Rprofile hidden file.
```

There are two special functions you can put:
	* **.First()** will run at the start of the R session
	* **.Last()** will run at the end of the session

You can check if you have a site-wide R configuration script by running
<span style="color: red">Create RProfile.site under R.home/etc/</span>

```R
R.home(component = "home")
```
in the R console and then checking for the presence of Rprofile.site in that directory. The presence of the user-defined R configuration can be checked for in the directory of whichever path
```R
path.expand("~")
```
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

#.First <- function(){
# #library(Hmisc)
# #library(R2HTML)
# cat("\nWelcome at", date(), "\n") 
#}

#.Last <- function(){ 
# cat("\nGoodbye at ", date(), "\n")
#}
```
* In order to use shinyjs, install V8
```
cd /usr/local/lib/R
sudo mkdir site-library
sudo chmod o+w site-library
sudo apt-get install -y libv8-3.14-dev
R
chooseCRANmirror(81)
install.packges("V8")
```


* Install R Packages for Shiny
```
sudo apt-get install -y libxml2-dev

sudo su - -c "R -e \"install.packages(c('shiny','shinydashboard','shinyjs','quanteda', 'dygraphs', 'rhandsontable', 'keras','DEoptim','RSQLite','reshape2','mlbench','future','promises','shinyWidgets','devtools','Hmisc','XML','DT'), repos='https://mirrors.tuna.tsinghua.edu.cn/CRAN/')\""


sudo su - -c "R -e \"devtools::install_github('madlogos/recharts')\""
sudo su - -c "R -e \"devtools::install_github('lchiffon/REmap')\""
```

* Install keras(h5py),tensorflow
```
sudo apt-get install -y python-virtualenv
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

## Deploy App 

[https://www.linode.com/docs/development/r/how-to-deploy-rshiny-server-on-ubuntu-and-debian/#deploy-your-app]

By default, Shiny Server uses /srv/shiny-server/ as its site directory. Any Shiny apps in this directory will be served automatically.

Copy the example app directory into /srv/shiny-server/:
```
sudo cp -r Example/ /srv/shiny-server/
```
In a web browser, navigate to the app’s address. Replace example.com with your Linode’s public IP address or FQDN:
```
example.com:3838/Example
```
You should see your app displayed:


## Configure Shiny Server
Shiny Server’s configuration file is stored at `/etc/shiny-server/shiny-server.conf`:

```
# Instruct Shiny Server to run applications as the user "shiny"
run_as shiny;

# Define a server that listens on port 3838
server {
  listen 3838;

  # Define a location at the base URL
  location / {

    # Host the directory of Shiny Apps stored in this directory
    site_dir /srv/shiny-server;

    # Log all Shiny output to files in this directory
    log_dir /var/log/shiny-server;

    # When a user visits the base URL rather than a particular application,
    # an index of the applications available in this directory will be shown.
    directory_index on;
  }
}
```