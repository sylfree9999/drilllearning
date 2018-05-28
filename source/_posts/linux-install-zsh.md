---
title: Ubuntu EC2 install Oh My Zsh
date: 2018-05-22 15:40:12
tags: [linux, practice]
---

* 	`sudo apt-get install zsh`
*	wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh
*	sudo chsh -s /bin/zsh
*	Check whether your bash is correct: `$ cat /etc/passwd`
*	You should have root and ubuntu set as:
```
root:x:0:0:root:/root:/bin/zsh
ubuntu:x:1000:1000:Ubuntu,,,:/home/ubuntu:/bin/zsh
```
*	If not, manually change for ubuntu user:
```
sudo -s
chsh -s /bin/zsh ubuntu
```
* 	If you change the theme, be sure to install the theme first