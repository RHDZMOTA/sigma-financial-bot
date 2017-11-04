# -*- coding: utf-8 -*-


def replace(string, target, value):
    if not len(target):
        return string
    return replace(string.replace(target[0], value), target[1:], value)
