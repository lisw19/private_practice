import re
import json
import shlex
import argparse
import urllib.parse as urlp

from collections import OrderedDict, namedtuple
from six.moves import http_cookies as Cookie

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('url')
parser.add_argument('-d', '--data', '--data-raw')
parser.add_argument('-b', '--data-binary', default=None)
parser.add_argument('-X', default='')
parser.add_argument('-H', '--header', action='append', default=[])
parser.add_argument('--compressed', action='store_true')
parser.add_argument('--insecure', action='store_true')

BASE_INDENT = " " * 4
parsed_content = namedtuple('ParsedContext', ['method', 'url', 'data', 'headers', 'cookies', 'verify'])


def parse_cmd(curl_command):
    """
    解析curl的参数并映射到parsed_content的tuple中
    :param: curl_command: 以curl 开头的命令
    :return: <nametuple> 分割后的结果tuple
    """
    method = "get"
    tokens = shlex.split(curl_command)
    parsed_args = parser.parse_args(tokens)

    post_data = parsed_args.data or parsed_args.data_binary
    if post_data:
        method = 'post'
    if parsed_args.X:
        method = parsed_args.X.lower()

    cookie_dict = OrderedDict()
    quoted_headers = OrderedDict()

    # 解析parsed_args.header
    for curl_header in parsed_args.header:
        if curl_header.startswith(':'):
            occurrence = [m.start() for m in re.finditer(':', curl_header)]
            header_key, header_value = curl_header[:occurrence[1]], curl_header[occurrence[1] + 1:]
        else:
            header_key, header_value = curl_header.split(":", 1)

        if header_key.lower().strip("$") == 'cookie':
            cookie = Cookie.SimpleCookie(header_value)
            for key in cookie:
                cookie_dict[key] = cookie[key].value
        else:
            quoted_headers[header_key] = header_value.strip()

    # result nametuple
    return parsed_content(
        method=method,
        url=parsed_args.url,
        data=post_data,
        headers=quoted_headers,
        cookies=cookie_dict,
        verify=parsed_args.insecure
    )


def curl_parse(curl_command, is_return_py=False, **kargs):
    """
    抽取curl命令并生成python脚本
    :param: curl_command: 以curl 开头的命令
    :param: is_return_py: 是否return 结果为python脚本
    :kargs: 针对request需要额外添加的参数
    """
    parsed_context = parse_cmd(curl_command)

    # post_data处理
    data_token = ''
    data_dict = dict()
    if parsed_context.data:
        data_token = '{}data=\'{}\',\n'.format(
            BASE_INDENT, parsed_context.data)
        data_dict = dict(urlp.parse_qsl(
            parsed_context.data, keep_blank_values=True))

    verify_token = ''
    if parsed_context.verify:
        verify_token = '\n{}verify=False'.format(BASE_INDENT * 3 + ' ' * 7)

    requests_kargs = ''
    for k, v in sorted(kargs.items()):
        requests_kargs += "{}{}={}, \n".format(BASE_INDENT, k, str(v))

    formatter_dict = {
        'method': parsed_context.method,
        'url': parsed_context.url,
        'data': data_dict,
        'headers': dict(parsed_context.headers),
        'cookies': dict(parsed_context.cookies),
        'verify': parsed_context.verify,
        'requests_kargs': kargs
    }

    formatter = {
        'method': parsed_context.method,
        'url': parsed_context.url,
        'data_token': data_token.rstrip(),
        'headers_token': "{}headers={}".format(BASE_INDENT, dict_to_pretty_string(
            parsed_context.headers, indent=14)).rstrip(),
        'cookies_token': "{}cookies={}".format(BASE_INDENT, dict_to_pretty_string(
            parsed_context.cookies, indent=14)).rstrip(),
        'security_token': verify_token.rstrip(),
        'requests_kargs': requests_kargs.rstrip()
    }
    if not is_return_py:
        return formatter_dict
    py_requests_res = """import requests\n\nres = requests.{method}("{url}",
               {requests_kargs}
               {data_token}
               {headers_token},
               {cookies_token},
               {security_token}
              )\nprint(res.text)""".format(**formatter)
    with open('demo.py', 'w') as pyf:
        pyf.write(py_requests_res)
    return {
        'result': '参考当前目录的demo.py'
    }


def dict_to_pretty_string(the_dict, indent=4):
    """
    dict格式化处理
    """
    if not the_dict:
        return "{}"

    return ("\n" + " " * indent).join(
        json.dumps(the_dict, sort_keys=True, indent=indent,
                   separators=(',', ': ')).splitlines())


if __name__ == '__main__':
    cmd = """
curl 'http://bid.chinaemed.com/bid/JsonAllBidList' \
  -H 'Connection: keep-alive' \
  -H 'Pragma: no-cache' \
  -H 'Cache-Control: no-cache' \
  -H 'Accept: application/json, text/javascript, */*; q=0.01' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'Origin: http://bid.chinaemed.com' \
  -H 'Referer: http://bid.chinaemed.com/Bid/List.html/ALLBID' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Cookie: __utmc=158731624; Hm_lvt_df09b7a4cc0f7292a294ca8e514ec44e=1593417570; __utma=158731624.54958172.1593417570.1593417570.1593420510.2; __utmz=158731624.1593420510.2.2.utmcsr=bid.chinaemed.com|utmccn=(referral)|utmcmd=referral|utmcct=/Bid/Detail.html/Dynamic/Province/33335; Hm_lpvt_df09b7a4cc0f7292a294ca8e514ec44e=1593420989; hisArt=%5B%7B%22title%22%3A%222020%E5%B9%B4%E5%86%85%E8%92%99%E5%8F%A4%E8%87%AA%E6%B2%BB%E5%8C%BA%E4%B9%8C%E6%B5%B7%E5%B8%82%E5%8C%BB%E7%96%97%E6%9C%BA%E6%9E%84%E8%8D%AF%E5%93%81%E9%87%87%E8%B4%AD%E5%A4%87%E6%A1%88__%E5%90%84%E7%9C%81%E5%85%AC%E5%91%8A%E5%8A%A8%E6%80%81__%E6%98%93%E8%BF%88%E5%BE%97%E5%8C%BB%E8%8D%AF%E6%8B%9B%E6%8A%95%E6%A0%87%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F%22%2C%22url%22%3A%22http%3A%2F%2Fbid.chinaemed.com%2FBid%2FDetail.html%2FDynamic%2FProvince%2F33299%22%7D%5D' \
  --data-raw 'JqObject=&pageIndex=1' \
  --compressed \
  --insecure
    """
    print(curl_parse(cmd, is_return_py=False))
    # print(curl_parse(cmd, is_return_py=True))
    # from spider.cmd_settings import CMD_POST_TEST
    # from_cmd = CMD_POST_TEST
    # print(curl_parse(from_cmd, is_return_py=True))
