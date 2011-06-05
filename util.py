# -*- coding: utf-8 -*-

def to_new_base(number, alph=None):
    """ from number(10-base) to new base. Default to 62 """
    alph = alph or '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base = len(alph)

    res = []
    i = number
    while i != 0:
        i, rem = divmod(i, base)
        res.append(alph[rem])

    return ''.join(reversed(res)) or '0'
