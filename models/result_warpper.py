#!/usr/bin/env python


# encoding: utf-8


class Result:
    def __init__(self):
        self.status = 200
        self.data = None
        self.msg = ''


def ok_data(data):
    result = Result()
    result.status = 200
    result.data = data
    return result


def failure(msg):
    result = Result()
    result.status = 500
    result.msg = msg
    return result