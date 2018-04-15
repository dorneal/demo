#!/usr/bin/python3
# coding:utf-8
# Filename:test5.py
# Author:Neal
# Time:2018.04.15 15:37
import telnetlib

telnetlib.Telnet("197.210.216.22", port="8080", timeout=30)
