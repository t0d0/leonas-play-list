# coding:utf-8

import hashlib
import re


def convert_time(input_time):
    result_time = 0
    splited_time = re.split("[:：]", input_time)
    if len(splited_time) == 3:
        result_time += int(splited_time[0]) * 3600
        result_time += int(splited_time[1]) * 60
        result_time += int(splited_time[2])
        return result_time
    elif len(splited_time) == 2:
        result_time += int(splited_time[0]) * 60
        result_time += int(splited_time[1])
        return result_time
    elif len(splited_time) == 1:
        result_time += int(splited_time[0])
        return result_time
    else:
        raise Exception


def get_video_id(url):
    video_id = re.search(r"[/?=]([-\w]{11})", url).group().strip("=").strip("/")
    return video_id


def split_vertical_bar(raw_string):
    return re.split(r"\|", raw_string)


def sort_dict_list(dict_list, sort_key):
    return sorted(dict_list, key=lambda x: x[sort_key])


def get_hashed_password(input_password, input_salt):
    password = bytes(input_password, 'utf-8')
    salt = bytes(input_salt, 'utf-8')
    #    # ソルト(salt)を付け加えてからハッシュ化
    digest = hashlib.pbkdf2_hmac('sha256', password, salt, 100000).hex()
    return digest


def is_favorited_content(input_id, favorited_list):
    if input_id in favorited_list:
        return True
    else:
        return False
