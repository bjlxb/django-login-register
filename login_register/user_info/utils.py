# -*- coding: utf-8 -*-
import random


class IpUtil(object):

    def get_ip(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        if not ip:
            ip = '0.0.0.0'
        return ip


class RandomUtil(object):

    def num_random(self):
        nums = '1234567890'
        random_num = []
        for i in range(6):
            random_num.append(random.choice(nums))
        random_str = "".join(random_num)
        return random_str
