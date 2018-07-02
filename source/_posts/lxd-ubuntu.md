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