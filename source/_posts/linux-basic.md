---
title: linux-basic
date: 2018-06-14 15:24:37
tags: [linux, concept]
---

### VMWARE NAT 虚拟网络的配置介绍

VMWARE会自己生成一个虚拟的路由器，这个路由器的IP地址一般就是子网的网关地址和DNS地址。
DNS地址也可以设置成一些知名的DNS服务器地址，例如google的8.8.8.8

VMWARE在windows上面也会虚拟出一个VMWARE用的网卡，例如vmnet8,如果想让windows可以与虚拟机子连接，就设置成同一个子网的IP即可

{% asset_img vmware-network-map.png %}

<!-- more -->

### 桥接模式Bridge

网桥类似于Hub
任何机子连上来都属于同一网段，共用同一个IP段，虚拟机可以跟物理机相互ping通，所以物理机如果使用了这个IP，虚拟机不能再使用这个IP，没有隔离

所有的网络请求都要经过网桥（包括windows内部的请求），网桥然后连接物理网卡再跟真正的网络相连

如果路由器的物理IP变了，就要所有IP的都手动改变，所以这种模式不太推荐


首先需要在虚拟机的Machine Settings里面更改网络配置为桥接模式

{% asset_img vmware-network-bridge01.png %}

{% asset_img vmware-network-bridge02.png %}

### 常用命令[centos 6.7]

#### 网络方面

1. 	`netstat -nltp` 
	list all listening programs and their port
2. 	`setup`
	进入图形界面更改配置
3. 	`vi /etc/sysconfig/network`
	修改主机名
	```
	NETWORKING=yes
	HOSTNAME=server1.itcast.cn
	```
4. 	`vi /etc/sysconfig/network-scripts/ifcfg-eth0`
	修改IP地址
	```
	DEVICE = "eth0"
	TYPE = "Ethernet"
	ONBOOT = "yes"  #是否网卡开机启用
	BOOTPROTO = "static"
	IPADDR = "192.168.11.200"
	NETMASK = "255.255.255.0"
	GATEWAY = "192.168.11.2"
	```

	`service network restart`
5. 	`vi /etc/hosts`
	修改ip地址和主机名的映射关系

6. 	如果设置完以后仍无法上网[https://blog.csdn.net/love666666shen/article/details/78087862]：
	1,	VMWare Edit -> Virtual Network Editor
	{% asset_img vmware-net-01.png %}

	2,	Delete VMnet8/Vmnet0, recreate those two network with same settings as you set in the linux. 记得保存之前的子网IP和掩码信息
	3,	Check Windows Services -> VMware DHCP Service/VMware NAT Service/VMware Workstation Server重新开启运行一下，并重启虚拟机
	{% asset_img vmware-net-02.png %}

	4,	在Windows中进入Vmnet8-> IPV4 Settings ->自动获取IP地址和DNS地址
	{% asset_img vmware-net-03.png %}

	5,	重启虚拟机，如果还是无法连接，在linux系统里面重新建一个Wired Connetion,然后来回切换一下网络

	{% asset_img vmware-net-04.png %}

7. 	添加iptables, open port
	```
	service iptables status
	service iptables start
	service iptables status 
	iptables -nL --line-numbers

	```

	`iptables -I INPUT -p tcp --dport 8080 -j ACCEPT`
	删除第八行rule：
	`iptables -D INPUT 8`

#### 日常操作命令
`pwd`	查看当前所在目录
`date`	查看当前系统时间
`who` 	查看当前有谁在线，登陆了服务器
`last`	查看最近的登陆历史记录
`ls -al`	查看隐藏文件以及更详细的信息，以列表形式显示
`mkdir -p aaa/bbb`	如果子目录没有，一并创建
`touch filename`	创建文件
`vi 编辑`
	`A`	在该行的最后插入
	`a`	在该行最前面插入
	`gg`	直接跳到文件的首行
	`G`	直接跳到文件的末行
	`dd`	删除行，如果8dd，则一次性删除8行
	`yy`	复制当前行，3yy复制3行
	`p`	粘贴
	`/YOU`	查找文件中出现的YOU并定位到第一个找到的地方

#####文件权限的操作
drwxr-xr-x 
<span style="color: red">（也可以用二进制表示111 101 101，即十进制755）</span>

d:	标识节点类型（d:文件夹	-：文件	l:链接）
r:可读	
w:可写（删除文件并不代表你修改了这个文件，所以即使对这个文件没有写权限，也是可以删除的，删除其实是改变了父目录的内容，只要它上层directory有写权限，你就是可以删除的）
x:可执行（可不可以当一个程序来运行）
第一组rwx：	表示拥有者对它的权限
第二组rwx:	表示所属组对它的权限
第三组rwx：	上面用户之外的用户对它的权限

`chmod o-rw xx.file`
让其他人没有read write的权限
也可以用二进制的方法来写：
`chmod -R 700 xxxDirectory`
`chown -R angela:angela aaa/`更改所有者，必须用root才能改

##### 基本用户管理

`useradd angela`	添加用户
`passwd angela`	设置密码
`vi /etc/sudoers` -> 将用户加入到sudoers中
	```
	root	ALL=(ALL) 	ALL
	newuser	ALL=(ALL) 	ALL
	```

`su angela`	切换到angela
`exit`	退出angela

##### 系统命令
`hostname`	查看主机名

`hostname hadoop`	修改主机名，重启后无效

`vi /etc/sysconfig/network`	修改主机名，重启后永久生效

`ifconfig eth0 192.168.11.22`	修改IP，重启后无效

`vi /etc/sysconfig/network-scripts/ifcfg-eth0`	修改IP，重启后永久生效

`uname -a` `uname -r`	查看系统信息/内核版本

`date +%Y-%m-%d`	日期

`mount -t iso9660 -o ro /dev/cdrom /mnt/cdrom` 挂载外部存储设备到文件系统中，其中这个存储type为iso，让其readonly，光驱设备名称 /dev/cdrom 挂载到/mnt/cdrom这个目录	

`unmount /mnt/cdrom` 弹出

`du -sh /mnt/cdrom`	统计文件夹的大小
`df -h`	查看分区

`halt`	关机

##### ssh免密登陆
`ssh-keygen`	生成密钥对

`ssh-copy-id 192.168.11.222` 就会自动把公钥copy到192.168.11.222这个机子的.ssh/authorized_keys文件夹中 

##### 查看文件
`tail -10 install.log`	查看文件尾部的10行
`tail -f install.log`	实时输出文件尾部内容，小f跟踪文件的唯一inode号，就算文件改名后，还是跟踪原来这个inode表示的文件
`tail -F install.log`	大F按照文件名跟踪

##### 后台服务
`service --status-all`	系统中现在所有的后台服务
`service network stop/start/restart`
`chkconfig` 	查看所有服务自启配置
`chkconfig iptables off`	关掉指定服务的自动启动

##### 上传文件到服务器
在secureCRT中使用sftp工具:
`alt+p`调出后用`put`命令上传
`put xxx要上传的文件` 	上传到服务器当前目录
`lcd` 	指定下载到本地的目标路径
`get xxx要下载的文件` 	下载

##### 	解压打包文件

`gzip xxxfile` 	压缩文件成为.gz格式
`gzip -d` 	解压gz文件

`tar -cvf myfirstpackage.tar directory/` 	将directory目录打包到myfirstpackage.tar文件中
-c create -v show detail -f file

`tar -xvf myfirstpackage.tar` 解包文件

**一次性完成打包&压缩**
`tar -zcvf my.tar.gz directory/`
`tar -zxvf my.tar.gz -C d2/` 	解压到指定目录下

##### 	安装文件
0,	更改Mirror到清华
	yum [https://mirror.tuna.tsinghua.edu.cn/help/centos/]：
	首先备份CentOS-Base.repo
	`sudo mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.bak`
	然后vi /etc/yum.repos.d/CentOS-Base.repo
	将下面的写到文件中(CentOS6):
	
		```
		# CentOS-Base.repo
		#
		# The mirror system uses the connecting IP address of the client and the
		# update status of each mirror to pick mirrors that are updated to and
		# geographically close to the client.  You should use this for CentOS updates
		# unless you are manually picking other mirrors.
		#
		# If the mirrorlist= does not work for you, as a fall back you can try the
		# remarked out baseurl= line instead.
		#
		#
		
		[		base]
		name=CentOS-$releasever - Base
		baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/os/$basearch/
		#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=os
		gpgcheck=1
		gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
		
		#released updates
		[updates]
		name=CentOS-$releasever - Updates
		baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/updates/$basearch/
		#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=updates
		gpgcheck=1
		gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
		
		#additional packages that may be useful
		[extras]
		name=CentOS-$releasever - Extras
		baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/extras/$basearch/
		#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=extras
		gpgcheck=1
		gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
		
		#additional packages that extend functionality of existing packages
		[centosplus]
		name=CentOS-$releasever - Plus
		baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos/$releasever/centosplus/$basearch/
		#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=centosplus
		gpgcheck=1
		enabled=0
		gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
		```


	然后更新软件包缓存 ```sudo yum makecache```

1,	在安装jdk的时候如果出现`/lib/ld-linux.so.2: bad ELF interpreter: No such file or directory`
	
		```
		yum -y install glibc.i686
		apt-get update
		apt-get install ia32-libs
		```

2,	更改环境变量
	```
	vi /etc/profile
	:$ # to the end of the file
	o # append another line and goes into insert mode
	export PATH = /root/apps/jdkXXX
	export PATH=$PATH:$JAVA_HOME/bin
	:wq!
	source /etc/profile
	```

3,	`yum`安装
	`yum list | grep XX` 列出所有可用的package和package组
	`yum clean all`	清除所有缓冲数据
	`yum deplist httpd`	列出一个包所有依赖的包
	`yum remove httpd`	删除httpd
	`yum repolist`	看一下现在的repo有哪些

4，手动安装MySQL rpm包

	0，查询rpm包
		`rpm -qa`

	1，上传MySQL-server-5.5.48-1.linux2.6.x86_64.rpm、MySQL-client-5.5.48-1.linux2.6.x86_64.rpm到Linux上
	2，使用rpm命令安装MySQL-server-5.5.48-1.linux2.6.x86_64.rpm，缺少perl依赖
		`rpm -ivh MySQL-server-5.5.48-1.linux2.6.x86_64.rpm `
 
	3，安装perl依赖，上传6个perl相关的rpm包
 
		`rpm -ivh perl-*`
	4，再安装MySQL-server，rpm包冲突
		`rpm -ivh MySQL-server-5.5.48-1.linux2.6.x86_64.rpm`
 
	5，卸载冲突的rpm包
		`rpm -e mysql-libs-5.1.73-5.el6_6.x86_64 --nodeps`
	6，再安装MySQL-client和MySQL-server
		```
		rpm -ivh MySQL-client-5.5.48-1.linux2.6.x86_64.rpm
		rpm -ivh MySQL-server-5.5.48-1.linux2.6.x86_64.rpm
		```
	7，启动MySQL服务，然后初始化MySQL
		```
		service mysql start
		/usr/bin/mysql_secure_installation
		```
	8，测试MySQL
		```
		mysql -u root -pXXXX
		```

5，安装tomcat
	`tar -zxvf apacheXXXXX`
	`cd apacheXXX/bin`
	`./startup.sh`