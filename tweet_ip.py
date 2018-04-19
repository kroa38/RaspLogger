#!/usr/bin/python
# -*- coding: utf-8 -*-
#this code is used to tweet the current local ip address, because
#in dhcp mode we don't know it.

from cloudscope import tweet_ip_addr, check_internet

def tweet_ip():
	"""
	check if internet is up.
	tweet the ip address
	"""
	if check_internet()=="1":
		tweet_ip_addr()
	exit()

tweet_ip()

