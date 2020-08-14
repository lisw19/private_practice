import zlib
import base64
import zipfile
import os
import time

from tools.docu_path import remove_path


def compress_encrypt(target_str):
    """
    针对target_str字符串压缩运用zlib加密，
    目的是为了让字符串更短，但不流失原有信息
    :param:target_str: 目标字符串
    :return: <str>
    """
    if isinstance(target_str, str):
        _tar_str = target_str.encode('utf-8')
    elif isinstance(target_str, bytes):
        _tar_str = target_str
    else:
        raise TypeError('target_str should be str/bytes!')
    _compress_res = zlib.compress(_tar_str)
    compress_res = base64.b64encode(_compress_res)
    return compress_res


def decompress_encrypt(target_str):
    """
    针对target_str字符串(经过compress_encrypt加密压缩)压缩解密，
    目的是还原压缩前的原有信息
    :param:target_str: 目标字符串
    :return: <str>
    """
    assert isinstance(target_str, str), 'param type error!'
    _decompress_res = base64.b64decode(target_str)
    return zlib.decompress(_decompress_res)


def unzip_single(source_dir, dest_dir, password=None):
    """
    解压zip文件
    :param source_dir: zip文件路径
    :param dest_dir: 解压到dest_dir
    :param password: 压缩文件密码
    :return: False/True
    """
    if not os.path.exists(source_dir):
        print("[UnZip]error:{} non-existent".format(source_dir))
        return False
    if not os.path.isdir(source_dir) and not zipfile.is_zipfile(source_dir):
        print("[UnZip]error:{} unlawful".format(source_dir))
        return False
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    if password:
        password = password.encode()
    print("[UnZip]start:source_file:{} to:{}".format(source_dir, dest_dir))
    zf = zipfile.ZipFile(source_dir)
    try:
        zf.extractall(path=dest_dir, pwd=password)
    except Exception as e:
        print('[UnZip]error: {}'.format(repr(e)))
        zf.close()
        return False
    zf.close()
    return True


def to_zip(source_dir, dest_dir):
    """
    解压zip文件
    :param source_dir: 待zip文件绝对路径
    :param dest_dir: 压缩后文件地址
    :return: False/True
    """
    print('[TO_ZIP]待压缩文件：「{}」'.format(source_dir))

    def write_all_file_to_zip(source_dir, zip_file):
        """
        递归读取abs_dir文件夹中所有文件，并塞进zip_file文件中
        :param abs_dir: 文件夹的绝对路径
        :param zip_file:
        :return:
        """
        cur_abs_path = os.path.abspath(os.path.dirname(__file__))
        if os.path.isfile(source_dir):
            rel_file_path = source_dir.replace(cur_abs_path + '/', '')
            zip_file.write(rel_file_path)
            return True
        for f in os.listdir(source_dir):
            absFile = os.path.abspath(source_dir) + '/{}'.format(f)
            if os.path.isdir(absFile):
                # 改成相对路径，否则解压zip是/User/xxx开头的文件。
                rel_file_path = absFile.replace(cur_abs_path + '/', '')
                zip_file.write(rel_file_path)
                write_all_file_to_zip(absFile, zip_file)
            else:
                # 改成相对路径
                rel_file_path = absFile.replace(cur_abs_path + '/', '')
                zip_file.write(rel_file_path)
        return True

    cur_abs_path = os.path.abspath(os.path.dirname(__file__))
    commod = r"cp -rf {} {}".format(source_dir, cur_abs_path)
    os.popen(commod)
    source_dir = cur_abs_path + '/{}'.format(source_dir.split('/')[-1]).replace('\\', '')
    time.sleep(1.5)
    if not os.path.exists(source_dir):
        print("[ZIP]error:{} non-existent".format(source_dir))
        return False
    print("[ZIP]start:source_file:{} to:{}".format(source_dir, dest_dir))
    zip_file = zipfile.ZipFile(dest_dir, "w", zipfile.ZIP_DEFLATED)
    # ZIP_STOREED：只是作为一种存储，实际上并未压缩
    # ZIP_DEFLATED：用的是gzip压缩算法
    # ZIP_BZIP2：用的是bzip2压缩算法
    # ZIP_LZMA：用的是lzma压缩算法"""
    try:
        write_all_file_to_zip(source_dir, zip_file)
    except Exception as e:
        print("[ZIP]Error:{}, {}:%s".format(type(e), e))
    finally:
        remove_path(source_dir)
        zip_file.close()
        time.sleep(1.5)
    return True
