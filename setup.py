#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyInstaller.__main__ import run
import sys

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    opts = ['-F',
            '-w',
            '-y',
            '--paths=C:/python/python3.7.3/Lib/site-packages/cv2',
            # '--paths=D:\\ProgramData\\Anaconda3\\Lib\\site-packages\\PyQt5\\Qt\\plugins',
            # '--paths=D:\\ProgramData\\Anaconda3\\Lib\\site-packages\\newspaper3k-0.2.6-py3.6.egg\\newspaper',
            # '--add-data', 'D:\\ProgramData\\Anaconda3\\Lib\\site-packages\\PyQt5\\Qt\\plugins\\styles\\*;'
            #               './PyQt5/Qt/plugins/styles',
            # '--add-data', 'conf/*;conf/',
            # '--add-data', 'icon/*;icon/',
            # '--add-data', 'mgc/*;mgc/',
            '--clean',
            '--icon=images/icon.ico',
            'face_server.py']
    run(opts)