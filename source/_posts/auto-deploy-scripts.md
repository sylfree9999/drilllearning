---
title: auto-deploy-scripts
date: 2018-06-26 14:16:09
tags: [linux, practice]
---

## 自己建yum源【centos系统】

1，启一个httpd web service，不需要装tomcat这类，只需要一个静态的服务器即可
2，检查httpd service `service httpd status`
3，在`/var/www/html`下面创建一个目录挂载cdrom
4，挂载目录指令为
	`mount -t iso9660 -o ro /dev/cdrom /mnt/cdrom`
41，如果iso盘中没有`repodata`,即没有dependecy link文件，需要手动创建
	`createrepo /mnt/cdromlocal`
42，	创建完`repodata`后，需要再生成一个iso文件
	`mkisofs -o /mnt/example.iso /mnt/cdromlocal/`
5，设置重启自动挂载
	`vi /etc/fstab`
	在文件尾部追加
	`/dev/cdrom		/mnt/cdrom		iso9660		defaults		0		0`
6，在httpd html文件夹下面新建一个文件夹比方说叫centos，软链接指向这个mnt目录即可，假设mnt目录为/mnt/cdrom
	`ln -s /mnt/cdrom /var/www/html/centos`
7，更改centos repo.d文件，指向这个yum源
	`vi /etc/yum.repos.d/xxx.repo`
	```
	[base]
	name=CentOS-Local
	baseurl=http://192.168.X.X/centos
	gpgcheck=1
	enabled=1   #很重要，1才启用
	gpgkey=file:///mnt/cdrom/rpm-gpg/RPM-GPG-KEY-CentOS-6
	```
8，常用yum命令
	`yum clean all`	清除所有缓冲数据
	`yum repolist`	列出可用的yum源
	`yum deplist httpd`	列出一个包所依赖的包
	`yum remove httpd`	删除一个包

## 准备一个boot.sh脚本

`ssh-keygen -f`	查看pem对应的private key

ssh登陆所用的key pair存在.ssh/authorized_keys文件中，如果不小心删掉了，可以把private key的内容copy到authorized_keys文件，然后+空格+pem的名称，比如`ssh-rsa XXXXXX linuxAAAA`,之后再更改文件权限`chmod 600 .ssh/authorized_keys`

`ssh-keygen -f publickey.pem >> authorized.keys`或者可以用这个命令写进去前半段key的内容

`ssh-keygen -R hostname`	删除known_hosts

`sudo yum install expect`	模拟用户输入密码，yes等信息

```bash
#!/bin/bash
SERVERS="node-3.itcast.cn node-4.itcast.cn"
PASSWORD=123456
BASE_SERVER=172.16.203.100

#auto_ssh_copy_id() {
#    expect -c "set timeout -1;
#        spawn ssh-copy-id $1;
#        expect {
#            *(yes/no)* {send -- #yes\r;exp_continue;}
#            *assword:* {send -- $2\r;exp_continue;}
#            eof        {exit 0;}
#        }";
#}
#
#ssh_copy_id_to_all() {
#    for SERVER in $SERVERS
#    do
#        auto_ssh_copy_id $SERVER $PASSWORD
#    done
#}
#

auto_ssh_login() {
    expect -c "set timeout -1;
        spawn ssh -i /home/ec2-user/linuxSS.pem ec2-user@$1;
        expect {
            *(yes/no)* {send -- yes\r;exp_continue;}
            eof        {exit 0;}
        }";
}

ssh_login_to_all() {
        for SERVER in $SERVERS
        do
                auto_ssh_login $SERVER
        done
}

ssh_login_to_all


for SERVER in $SERVERS
do
       scp -i linuxSS.pem install.sh ec2-user@$SERVER:/home/ec2-user
       ssh -i linuxSS.pem ec2-user@$SERVER "sudo chmod u+x /home/ec2-user/install.sh;echo lalalal >> /home/ec2-use$
done
```

## Install.sh

如果用`echo`来写入到/etc/profile中，换行符不好弄
`<<`类似于文件的重定向，就是写个文件进去，`EOF`就是文件的标志，末尾也要写个EOF进去，就相当于追加一个文件到/etc/profile的末尾

```bash
#!/bin/bash

BASE_SERVER=172.16.203.100
yum install -y wget
wget $BASE_SERVER/soft/jdk-XXXX.tar.gz
tar -zxvf jdk-XXXX.tar.gz -C /usr/local
cat >> /etc/profile << EOF
export JAVA_HOME=/usr/local/jdkXXX
export PATH=\$PATH:\$JAVA_HOME/bin
EOF
```


