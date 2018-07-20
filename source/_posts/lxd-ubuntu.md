---
title: lxd-ubuntu
date: 2018-07-02 15:20:41
tags: [LXD, practice]
---

ENV: UBUNTU

## Add a non root user
```shell
adduser lxduser
usermod -aG sudo lxduser
##disable password authentication
sudo nano /etc/ssh/sshd_config
PasswordAuthentication no
sudo systemctl reload sshd
```

## Configure LXD
```shell
sudo usermod --append --groups lxd lxduser
sudo apt-get update
sudo apt-get install zfsutils-linux
sudo lxd init
Do you want to configure a new storage pool (yes/no) [default=yes]? yes
Name of the storage backend to use (dir or zfs) [default=zfs]: zfs
Create a new ZFS pool (yes/no) [default=yes]? yes
Name of the new ZFS pool [default=lxd]: lxd
Would you like to use an existing block device (yes/no) [default=no]?
Would you like to use an existing block device (yes/no) [default=no]? no
Size in GB of the new loop device (1GB minimum) [default=15]: 15
Would you like LXD to be available over the network (yes/no) [default=no]? no
Do you want to configure the LXD bridge (yes/no) [default=yes]? yes

```

## Create Container
```shell
lxc list
Generating a client certificate. This may take a minute...
If this is your first time using LXD, you should also run: sudo lxd init
To start your first container, try: lxc launch ubuntu:16.04

+------+-------+------+------+------+-----------+
| NAME | STATE | IPV4 | IPV6 | TYPE | SNAPSHOTS |
+------+-------+------+------+------+-----------+

lxc launch ubuntu:x webserver

##The x in ubuntu:x is a shortcut for the first letter of Xenial, the codename of Ubuntu 16.04. ubuntu: is the identifier for the preconfigured repository of LXD images. You could also use ubuntu:16.04 for the image name.

```

## Configure Container
```shell
lxc exec webserver -- sudo --login --user ubuntu
```

## Ubuntu Nginx AutoStart
[https://community.rackspace.com/products/f/public-cloud-forum/6747/ubuntu-and-debian---adding-an-nginx-init-script]

```
sudo nano /etc/init.d/nginx
```
Add those, **spotted: ADD YOUR NGINX INSTALLATION PATH INTO $PATH**
```
#! /bin/sh
 
### BEGIN INIT INFO
# Provides:          nginx
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts the nginx web server
# Description:       starts nginx using start-stop-daemon
### END INIT INFO
 
PATH=/usr/local/nginx/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/local/nginx/sbin
NAME=nginx
DESC=nginx
 
test -x $DAEMON || exit 0
 
# Include nginx defaults if available
if [ -f /etc/default/nginx ] ; then
    . /etc/default/nginx
fi
 
set -e
 
. /lib/lsb/init-functions
 
case "$1" in
  start)
    echo -n "Starting $DESC: "
    start-stop-daemon --start --quiet --pidfile /usr/local/nginx/logs/$NAME.pid \
        --exec $DAEMON -- $DAEMON_OPTS || true
    echo "$NAME."
    ;;
  stop)
    echo -n "Stopping $DESC: "
    start-stop-daemon --stop --quiet --pidfile /usr/local/nginx/logs/$NAME.pid \
        --exec $DAEMON || true
    echo "$NAME."
    ;;
  restart|force-reload)
    echo -n "Restarting $DESC: "
    start-stop-daemon --stop --quiet --pidfile \
        /usr/local/nginx/logs/$NAME.pid --exec $DAEMON || true
    sleep 1
    start-stop-daemon --start --quiet --pidfile \
        /usr/local/nginx/logs/$NAME.pid --exec $DAEMON -- $DAEMON_OPTS || true
    echo "$NAME."
    ;;
  reload)
      echo -n "Reloading $DESC configuration: "
      start-stop-daemon --stop --signal HUP --quiet --pidfile /usr/local/nginx/logs/$NAME.pid \
          --exec $DAEMON || true
      echo "$NAME."
      ;;
  status)
      status_of_proc -p /usr/local/nginx/logs/$NAME.pid "$DAEMON" nginx && exit 0 || exit $?
      ;;
  *)
    N=/etc/init.d/$NAME
    echo "Usage: $N {start|stop|restart|reload|force-reload|status}" >&2
    exit 1
    ;;
esac
 
exit 0
```
```
sudo chmod +x /etc/init.d/nginx
sudo /usr/sbin/update-rc.d -f nginx defaults
```
The output will be similar to this:
```
Adding system startup for /etc/init.d/nginx ...
 Adding system startup for /etc/init.d/nginx ...
   /etc/rc0.d/K20nginx -> ../init.d/nginx
   /etc/rc1.d/K20nginx -> ../init.d/nginx
   /etc/rc6.d/K20nginx -> ../init.d/nginx
   /etc/rc2.d/S20nginx -> ../init.d/nginx
   /etc/rc3.d/S20nginx -> ../init.d/nginx
   /etc/rc4.d/S20nginx -> ../init.d/nginx
   /etc/rc5.d/S20nginx -> ../init.d/nginx
```

Then start/stop/restart
```
sudo /etc/init.d/nginx start
...
sudo /etc/init.d/nginx stop
...
sudo /etc/init.d/nginx restart
```
## Reset timezone
```
sudo dpkg-reconfigure tzdata
```

## Rename Container
1,	Login to the container
	```
	sudo -s
	hostname newName
	echo newName > /etc/hostname
	bash
	reboot
	exit
	```
2,	Return to the host
	```
	sudo -s
	lxc stop oldName
	lxc move oldName newName
	lxc start newName
	lxc list
	```


## Copy Container
```
lxc copy old1 new1
lxc start new1
```

## Add Swap Space 

[https://www.digitalocean.com/community/tutorials/how-to-add-swap-space-on-ubuntu-16-04]

#### Check system for swap information
```
sudo swapon --show
```
If you don't get back any output, this means your system does not have swap space available currently.

You can verify that there is no active swap using the free utility:
```
free -h
```
```
Output
              total        used        free      shared  buff/cache   available
Mem:           488M         36M        104M        652K        348M        426M
Swap:            0B          0B          0B
```
#### Check Available Space on the Hard Drive Partition
The most common way of allocating space for swap is to use a separate partition devoted to the task. However, altering the partitioning scheme is not always possible. We can just as easily create a swap file that resides on an existing partition.

Before we do this, we should check the current disk usage by typing:

```
df -h
```
```
Output
Filesystem      Size  Used Avail Use% Mounted on
udev            238M     0  238M   0% /dev
tmpfs            49M  624K   49M   2% /run
/dev/vda1        20G  1.1G   18G   6% /
tmpfs           245M     0  245M   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           245M     0  245M   0% /sys/fs/cgroup
tmpfs            49M     0   49M   0% /run/user/1001
```

#### Create a Swap File
Now that we know our available hard drive space, we can go about creating a swap file within our filesystem. We will create a file of the swap size that we want called swapfile in our root (/) directory.

The best way of creating a swap file is with the fallocate program. This command creates a file of a preallocated size instantly.

Since the server in our example has 512MB of RAM, we will create a 1 Gigabyte file in this guide. Adjust this to meet the needs of your own server:
```
sudo fallocate -l 1G /swapfile
```
We can verify that the correct amount of space was reserved by typing:
```
ls -lh /swapfile
```
```
-rw-r--r-- 1 root root 1.0G Apr 25 11:14 /swapfile
```

#### Enabling the Swap File
Now that we have a file of the correct size available, we need to actually turn this into swap space.

First, we need to lock down the permissions of the file so that only the users with root privileges can read the contents. This prevents normal users from being able to access the file, which would have significant security implications.

Make the file only accessible to root by typing:
```
sudo chmod 600 /swapfile
```
We can now mark the file as swap space by typing:
```
sudo mkswap /swapfile
```
```
Setting up swapspace version 1, size = 1024 MiB (1073737728 bytes)
no label, UUID=6e965805-2ab9-450f-aed6-577e74089dbf
```
After marking the file, we can enable the swap file, allowing our system to start utilizing it:
```
sudo swapon /swapfile
```
We can verify that the swap is available by typing:
```
sudo swapon --show
```
```
Output
NAME      TYPE  SIZE USED PRIO
/swapfile file 1024M   0B   -1
```

#### Make the swap file permanant
Our recent changes have enabled the swap file for the current session. However, if we reboot, the server will not retain the swap settings automatically. We can change this by adding the swap file to our `/etc/fstab`file.

```
sudo cp /etc/fstab /etc/fstab.bak
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

#### Adjusting the Swappiness Property
The swappiness parameter configures how often your system swaps data out of RAM to the swap space. This is a value between 0 and 100 that represents a percentage.

With values close to zero, the kernel will not swap data to the disk unless absolutely necessary. Remember, interactions with the swap file are "expensive" in that they take a lot longer than interactions with RAM and they can cause a significant reduction in performance. Telling the system not to rely on the swap much will generally make your system faster.

Values that are closer to 100 will try to put more data into swap in an effort to keep more RAM space free. Depending on your applications' memory profile or what you are using your server for, this might be better in some cases.

```
cat /proc/sys/vm/swappiness
```
```
Output
60
```
For a Desktop, a swappiness setting of 60 is not a bad value. For a server, you might want to move it closer to 0.

We can set the swappiness to a different value by using the sysctl command.

For instance, to set the swappiness to 10, we could type:
```
sudo sysctl vm.swappiness=10
```
```
Output
vm.swappiness = 10
```

This setting will persist until the next reboot. We can set this value automatically at restart by adding the line to our /etc/sysctl.conf file:
```
sudo nano /etc/sysctl.conf
```
At the bottom, you can add:
```
vm.swappiness=10
```
#### Adjusting the Cache Pressure Setting
Another related value that you might want to modify is the vfs_cache_pressure. This setting configures how much the system will choose to cache inode and dentry information over other data.

Basically, this is access data about the filesystem. This is generally very costly to look up and very frequently requested, so it's an excellent thing for your system to cache. You can see the current value by querying the proc filesystem again:
```
cat /proc/sys/vm/vfs_cache_pressure
```
```
Output
100
```

As it is currently configured, our system removes inode information from the cache too quickly. We can set this to a more conservative setting like 50 by typing:
```
sudo sysctl vm.vfs_cache_pressure=50
```
Again, this is only valid for our current session. We can change that by adding it to our configuration file like we did with our swappiness setting:
```
sudo nano /etc/sysctl.conf
vm.vfs_cache_pressure=50
```

## Bash Script to launch lxd

REF:[https://gist.github.com/CalebEverett/aef682acf6988bbc44d9d8196f222355]

```bash
#!/bin/bash

# variables
CONTAINER=mycontainer
IMAGE=ubuntu-daily:xenial
PORT=8080
PROFILES=default
FOLDER=app
REPO=https://github.com/CalebEverett/hello-lxd.git
RUN_USER=app
RUN_USER_UID=1444
CONTAINER_ROOT_UID=$(cat /etc/subgid | grep lxd | cut -d : -f 2)

function wait_bar () {
  for i in {1..10}
  do
    printf '= %.0s' {1..$i}
    sleep $1s
  done
}

# create the container if it doesn't exist
if [ ! -e /var/lib/lxd/containers/$CONTAINER ]
  then
    lxc launch --verbose $IMAGE $CONTAINER
    wait_bar 0.5
    echo container $CONTAINER started
  else
    echo container $CONTAINER already created
fi

# apply profiles
lxc profile apply $CONTAINER $PROFILES

# delete ubuntu user
if [ ! -z $(lxc exec $CONTAINER -- getent passwd | grep ubuntu) ]
then
  lxc exec $CONTAINER -- userdel -r ubuntu
fi

# create running user
if [ -z $(lxc exec $CONTAINER -- getent passwd | grep $RUN_USER) ]
then
  lxc exec $CONTAINER -- useradd -u $RUN_USER_UID -s /usr/sbin/nologin $RUN_USER
fi

#install node
if [ -z $(lxc exec $CONTAINER -- which node) ]
then
  printf "\n\n*** Installing node ***"
  lxc exec $CONTAINER -- /bin/bash -c 'curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -'
  lxc exec $CONTAINER -- apt-get install -y nodejs
  echo Node $(lxc exec $CONTAINER -- node -v) installed
else
  echo Node $(lxc exec $CONTAINER -- node -v) already installed
fi

#install git
if [ -z $(lxc exec $CONTAINER -- which git) ]
then
  printf "\n\n*** Installing git ***"
  lxc exec $CONTAINER -- apt-get install -y git
  echo $(lxc exec $CONTAINER -- git --version) installed
else
  echo $(lxc exec $CONTAINER -- git --version) already installed
fi

# redirect 80 to $PORT
if [[ -z $(lxc exec $CONTAINER -- cat /etc/ufw/before.rules | grep PREROUTING) ]]
then
  lxc exec $CONTAINER -- /bin/bash -c "sed -i '/#   ufw-before-forward/ a\
#\n\
# redirect 80 to $PORT\n\
*nat\n\
:PREROUTING ACCEPT [0:0]\n\
-A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port $PORT\n\
COMMIT' /etc/ufw/before.rules"
  lxc exec $CONTAINER -- ufw enable
  lxc exec $CONTAINER -- ufw allow $PORT/tcp
fi

#mount $FOLDER directory if developing
if [[ $FOLDER &&  $PROFILES == *"default"* ]]
then
  printf "\n\n*** Mounting shared folder ***\n"
  if [ ! -d ./$FOLDER ]; then mkdir ./$FOLDER; fi
  if [[ -z $(lxc config device list $CONTAINER | grep $FOLDER) ]]
  then
    lxc config device add $CONTAINER $FOLDER disk path=/usr/src/$FOLDER source=$(pwd)/$FOLDER
    sudo chown -R $((CONTAINER_ROOT_UID + RUN_USER_UID)):$((CONTAINER_ROOT_UID + $RUN_USER_UID)) ./$FOLDER
    sudo setfacl -R -m d:u:$USER:xwr,u:$USER:xwr,d:g:$USER:xwr,g:$USER:xwr ./$FOLDER
    sudo chown -R $((CONTAINER_ROOT_UID + RUN_USER_UID)):$((CONTAINER_ROOT_UID + $RUN_USER_UID)) ./$FOLDER
    echo $(pwd)/$FOLDER mounted at /usr/src/$FOLDER
  else
    echo Directory $(pwd)/$FOLDER already mounted
  fi
fi

#clone repo and install modules
if [ $REPO ]
  then 
  if [[ -z $(lxc exec $CONTAINER -- cat /usr/src/$FOLDER/package.json) ]]
    then
      lxc exec $CONTAINER -- git clone -q $REPO /usr/src/$FOLDER
      lxc exec $CONTAINER --env HOME=/usr/src/$FOLDER -- npm install
      lxc exec $CONTAINER -- chown -R $RUN_USER:$RUN_USER /usr/src/$FOLDER/node_modules
    fi
fi

# build and run as a service if production
if [[ $PROFILES == *"pro"* ]]
then  
  if [[ $(lxc exec $CONTAINER -- /bin/bash -c 'if [ ! -f /etc/systemd/system/$CONTAINER.service ]; then echo 0; fi') ]]
  then
    printf "\n\n*** Creating service file ***"
    lxc exec $CONTAINER -- /bin/bash -c "cat <<-EOF > /etc/systemd/system/$CONTAINER.service
    [Unit]
    Description=$CONTAINER
    [Service]
    WorkingDirectory=/usr/src/$FOLDER
    ExecStart=/usr/bin/node /usr/src/$FOLDER/index.js
    Restart=always
    RestartSec=10
    StandardOutput=syslog
    StandardError=syslog
    SyslogIdentifier=$CONTAINER
    User=$RUN_USER
    Environment=HOME=/usr/src/$FOLDER
    Environment=NODE_ENV=production
    Environment=PORT=$PORT
    
    [Install]
    WantedBy=multi-user.target
EOF"
    lxc exec $CONTAINER -- systemctl enable $CONTAINER.service
    sleep 3.0s
    lxc exec $CONTAINER -- systemctl start $CONTAINER.service
  fi
fi

printf "\n" && lxc list $CONTAINER

# start app for dev
if [[ $PROFILES == *"default"* && -z $(lxc exec $CONTAINER -- ps aux | grep /usr/src/$FOLDER/index.js) ]]
then
  google-chrome $(lxc exec $CONTAINER -- bash -c "ifconfig | grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' | head -n 1")
  lxc exec $CONTAINER --env HOME=/usr/src/$FOLDER --env PORT=$PORT -- node index.js
fi
```