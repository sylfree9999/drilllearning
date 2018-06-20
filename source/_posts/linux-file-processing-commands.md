---
title: Linux文本处理sed,awk,cut,sort
date: 2018-06-20 18:14:58
tags: [linux, concept]
---

## CUT
CUT命令可以从一个文本文件或者文本流中提取文本
`echo $PATH | cut -d ':' -f 2,3`将PATH变量取出，返回第二，第三个路径
`echo $PATH | cut -d ':' -f 1-3,5`取1~3和第五个

## SORT
对FILE参数制定的文件中的行排序，并将结果写到标准输出
```

[root@ip-172-31-7-202 ec2-user]# cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync

[root@ip-172-31-7-202 ec2-user]# cat /etc/passwd | sort
adm:x:3:4:adm:/var/adm:/sbin/nologin
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
dbus:x:81:81:System message bus:/:/sbin/nologin
ec2-user:x:500:500:EC2 Default User:/home/ec2-user:/bin/bash

[root@ip-172-31-7-202 ec2-user]# cat /etc/passwd | sort -t ':' -k 3 //以：为分隔符，以第三列字符串模式为排序标准
root:x:0:0:root:/root:/bin/bash
uucp:x:10:14:uucp:/var/spool/uucp:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
bin:x:1:1:bin:/bin:/sbin/nologin

[root@ip-172-31-7-202 ec2-user]# cat /etc/passwd | sort -t ':' -k 3n //以第三列数字模式排序
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin

[root@ip-172-31-7-202 ec2-user]# cat /etc/passwd | sort -t ':' -k 3nr //倒序排列
nfsnobody:x:65534:65534:Anonymous NFS User:/var/lib/nfs:/sbin/nologin
ec2-user:x:500:500:EC2 Default User:/home/ec2-user:/bin/bash
saslauth:x:499:76:"Saslauthd user":/var/empty/saslauth:/sbin/nologin
nobody:x:99:99:Nobody:/:/sbin/nologin

[root@ip-172-31-7-202 ec2-user]# cat /etc/passwd | sort -t ':' -k 7 -u //去重
root:x:0:0:root:/root:/bin/bash
sync:x:5:0:sync:/sbin:/bin/sync
halt:x:7:0:halt:/sbin:/sbin/halt
bin:x:1:1:bin:/bin:/sbin/nologin
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
```

## uniq
uniq只能去重排序过的文件
```
cat testfile | sort | uniq -c //-c显示重复次数
1 friend
3 hello
2 world
```

## sed
### 删除：d命令
`sed -i '2d' example` 删除example文件的第二行并写会原文件，不建议刚开始就用-i写回文件，调试完了以后再加-i
`sed '2,$d' example` 删除example文件的第二行到末尾所有行，正则中$表示末尾，^表示开头
`sed '$d' example` 删除example文件的最后一行
`sed '/test/'d example` 删除example文件所有包含test的行,//代表模式
### 替换：s命令
`sed 's/test/mytest/g' example` 在整行范围内把test替换成mytest，如果没有g标记，则只有每行第一个匹配的test会被替换成mytest
`sed -n 's/^test/mytest/p' example` (-n)选项和p标志一起使用表示只打印那些发生替换的行。也就是说如果某一行开头的test被替换成mytest，就打印它。
`sed 's/^192.168.0.1/&localhost/' example` &符号表示替换字符串被找到的部分再加上新的。所有以192.168.0.1开头的行都会被替换成它自己加localhost，即192.168.0.1localhost。
`sed -n 's/\(love\)able/\1rs/p' example` love被标记为1，所有loveable会被替换成lovers，且替换的行会被打印出来，\1代表第一组	

## awk
`last -n 5 | awk '{print $1}'` 打印出第一列的登录人名
awk工作流程：读入有'\n'换行符分割的一条记录，然后将记录按指定的域分隔符划分域，填充域，$0表示所有域，$1表示第一个域，$n表示第n个域。
默认域分隔符是"空白键"或者"[tab]键",所以$1表示登录用户，$3表示登录用户ip,以此类推

`cat /etc/passwd | awk -F ':' '{print $1"\t"$7}'`指定分隔符,且账户与shell之间以tab键分割

`cat /etc/passwd | awk -F ':' 'BEGIN {print "name,shell"} {print $1","$7} END {print "endtest,/bin/bash"}'`
awk还可以分Begin 中间 End三个部分

```
[root@ip-172-31-7-202 ec2-user]# cat /etc/passwd | awk -F ':' 'BEGIN {print "name,shell"} {print $1","$7} END {print "endtest,/bin/bash"}'
name,shell
root,/bin/bash
bin,/sbin/nologin
daemon,/sbin/nologin
adm,/sbin/nologin
lp,/sbin/nologin
sync,/bin/sync
shutdown,/sbin/shutdown
halt,/sbin/halt
mail,/sbin/nologin
uucp,/sbin/nologin
operator,/sbin/nologin
games,/sbin/nologin
gopher,/sbin/nologin
ftp,/sbin/nologin
nobody,/sbin/nologin
rpc,/sbin/nologin
ntp,/sbin/nologin
saslauth,/sbin/nologin
mailnull,/sbin/nologin
smmsp,/sbin/nologin
rpcuser,/sbin/nologin
nfsnobody,/sbin/nologin
sshd,/sbin/nologin
dbus,/sbin/nologin
ec2-user,/bin/bash
mysql,/bin/bash
endtest,/bin/bash
```