# coding:utf-8

import hashlib
import re


def convert_time(input_time):
    """':'で区切られた時間情報を秒に変換する。

    Args:
        input_time:'hh:mm:ss'形式で表現された時間の文字列。'mm:ss','ss'でも可

    Returns:秒

    """
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
    """urlからvideo_idを取得する。

    Args:
        url:video_idを含むurl

    Returns:video_id

    """
    video_id = re.search(r"[/?=]([-\w]{11})", url).group().strip("=").strip("/")
    return video_id


def split_vertical_bar(raw_string):
    """'|'で区切られた文字列を分割する。

    Args:
        raw_string:'|'で区切られた文字列

    Returns:分割されたlist

    """
    return re.split(r"\|", raw_string)


def sort_dict_list(dict_list, sort_key):
    """与えられたキーでdictをソートする

    Args:
        dict_list: ソート対象のdict
        sort_key:ソートするためのキー

    Returns:

    """
    return sorted(dict_list, key=lambda x: x[sort_key])


def get_hashed_password(input_password, input_salt):
    """パスワードをハッシュする。

    Args:
        input_password:ハッシュ前のパスワード
        input_salt:ソルト

    Returns:ハッシュ後のパスワード

    """
    password = bytes(input_password, 'utf-8')
    salt = bytes(input_salt, 'utf-8')
    #    # ソルト(salt)を付け加えてからハッシュ化
    digest = hashlib.pbkdf2_hmac('sha256', password, salt, 100000).hex()
    return digest


def is_favorited_content(input_id, favorited_list):
    """お気に入り登録済みのコンテンツかどうかを判別する。

    Args:
        input_id:判別対象のid
        favorited_list:お気に入りのコンテンツのlist

    Returns:お気に入りか否か

    """
    if input_id in favorited_list:
        return True
    else:
        return False
