#!/usr/bin/python3
# -*- coding: utf-8 -*-

from util_funct import tweet_ip_address, check_internet


def tweet_ip():
    """" check if internet is up.
         tweet the ip address
    """
    if check_internet():
        tweet_ip_address()


if __name__ == "__main__":
    tweet_ip()

