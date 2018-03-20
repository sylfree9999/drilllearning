---
title: DNS Resolution in Private Subnet with VPN to on-premises network
date: 2018-03-20 14:39:44
tags: [DNS, concept, practice]
---

### DNS Forwarding Definition

DNS forwarding is the process by which particular sets of DNS queries are handled by a designated server, rather than being handled by the initial server contacted by the client. Usually, all DNS servers that handle address resolution within the network are configured to forward requests for addresses that are outside the network to a dedicated forwarder.
[reference doc](http://social.dnsmadeeasy.com/blog/understanding-dns-forwarding/)

### Issue

AWS EC2 instances in private subnet cannot resolve dns names.
But EC2 instances can communicate with corporate network through VPN, the corporate network is able to correctly resolve dns.

### Solution

Change private subnet dns server to corporate dns server.

+ How to see current network dns server:

	+ windows: `ipconfig/all --> dns server`
	+ linux:
		`cat /etc/resolv.conf` can show your DNS servers

+ How to check if corporate dns is success or not:
	+ windows: 
		+ `nslookup`
		+ type `server 10.82.XX.XX`, where `10.82.XX.XX` is your corporate dns server ip address
		+ type any dns name, like baidu.com, bing.com, and press `Enter`
		+ check if the ip address is returned:
		{% asset_img nslookup.png %}
	+ linux(centos):
		+ normally `dig baidu.com`
		+ check if ip address is returned:
		{% asset_img dig.png %}
		+ resolve use specific DNS server, like Google's
		```linux
		dig @8.8.8.8 baidu.com
		```
		+ If you are just looking for IP address, you can add `+short` at the end
		```linux
		dig @8.8.8.8 baidu.com +short
		```

	
