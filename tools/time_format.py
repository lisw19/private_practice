import re
import time
import datetime
import traceback
import copy
import chardet
import lxml.html


class TimeFormat(object):
    """
    各类型格式化工具
    """

    @staticmethod
    def mysql_url(dic):
        mysql_url_template = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}'
        return mysql_url_template.format(user=dic['user'],
                                         password=dic['password'],
                                         host=dic['host'], port=dic['port'],
                                         database=dic['database'],
                                         charset=dic['charset'])

    @staticmethod
    def redis_url(dic):
        redis_url_template_h = 'redis://{host}'
        redis_url_template_hp = 'redis://{host}:{port}'
        redis_url_template_hpd = 'redis://{host}:{port}/{db}'
        redis_url_template_phpd = 'redis://:{password}@{host}:{port}/{db}'
        if dic.get('password'):
            return redis_url_template_phpd.format(password=dic['password'],
                                                  host=dic['host'],
                                                  port=dic['port'],
                                                  db=dic['db'])
        elif dic.get('db'):
            return redis_url_template_hpd.format(host=dic['host'],
                                                 port=dic['port'],
                                                 db=dic['db'])
        elif dic.get('port'):
            return redis_url_template_hp.format(host=dic['host'],
                                                port=dic['port'])
        else:
            return redis_url_template_h.format(host=dic['host'])

    @staticmethod
    def chinese_to_arabic_month(cn: str) -> str:
        check = {'一', '二', '三', '四', '五', '六', '七', '八', '九', '壹', '贰', '叁',
                 '肆', '伍', '陆', '柒', '捌', '玖', '貮', '两',
                 '十', '百', '千', '万'}
        digit = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8,
                 '九': 9,
                 '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8,
                 '玖': 9, '貮': 2, '两': 2}

        def _trans(s):
            num = 0
            if s:
                idx_q, idx_b, idx_s = s.find('千'), s.find('百'), s.find('十')
                if idx_q != -1:
                    num += digit[s[idx_q - 1:idx_q]] * 1000
                if idx_b != -1:
                    num += digit[s[idx_b - 1:idx_b]] * 100
                if idx_s != -1:
                    # 十前忽略一的处理
                    num += digit.get(s[idx_s - 1:idx_s], 1) * 10
                if s[-1] in digit:
                    num += digit[s[-1]]
            return num

        def trans(chn):
            chn = chn.replace('零', '')
            idx_y, idx_w = chn.rfind('亿'), chn.rfind('万')
            if idx_w < idx_y:
                idx_w = -1
            num_y, num_w = 100000000, 10000
            if idx_y != -1 and idx_w != -1:
                return trans(chn[:idx_y]) * num_y + _trans(
                    chn[idx_y + 1:idx_w]) * num_w + _trans(chn[idx_w + 1:])
            elif idx_y != -1:
                return trans(chn[:idx_y]) * num_y + _trans(chn[idx_y + 1:])
            elif idx_w != -1:
                return _trans(chn[:idx_w]) * num_w + _trans(chn[idx_w + 1:])
            return _trans(chn)

        cn_a = copy.deepcopy(cn)
        if (set(list(cn_a)) & check):
            cn_a = str(trans(cn_a))
        return cn_a

    @staticmethod
    def chinese_to_arabic(cn: str) -> int:
        # constants for chinese_to_arabic

        CN_NUM = {
            '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7,
            '八': 8, '九': 9, '零': 0, '十': 1,
            '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8,
            '玖': 9, '貮': 2, '两': 2, '拾': 1,
        }

        CN_UNIT = {
            '十': 10,
            '拾': 10,
            '百': 100,
            '佰': 100,
            '千': 1000,
            '仟': 1000,
            '万': 10000,
            '萬': 10000,
            '亿': 100000000,
            '億': 100000000,
            '兆': 1000000000000,
        }

        cn_a = copy.deepcopy(cn)
        for i in cn:
            if CN_NUM.get(i) != None:
                cn_a = cn_a.replace(i, str(CN_NUM.get(i)))

        return cn_a

    @staticmethod
    def regex_date(str_date):
        expression = "(20\d{2}([\.\-/|年月\s]{1,3}\d{1,2}){2}日?(\s?\d{2}:\d{2}(:\d{2})?)?)|(\d{1,2}\s?(分钟|小时|天)前)"
        expression = re.compile(expression)
        date = expression.search(str_date)
        if date:
            return date.group().replace('/', '-').replace('.', '-') \
                .replace('年', '-').replace('月', '-').replace('日', '')

    @staticmethod
    def str_datetime(str_datetime):
        date_format = \
            [
                "%Y-%m-%d",
                "%Y%m%d",
                "%d %m, %Y",
                "%A, %B %d, %Y",
                "%a, %B %d, %Y",
                "%A, %b %d, %Y",
                "%a, %b %d, %Y",
                "%b %d, %Y",
                "%B %d, %Y",
                "%d %b, %Y",
                "%d %B, %Y",
                "%B %d %Y",
                "%d %b %Y",
                "%d %b %Y",
                "%d %B %Y",
                "%y-%m-%d"
            ]
        clock = \
            [
                "",
                "%H:%M:%S",
                "%H:%M",
                "%H"
            ]
        for i in date_format:
            for ii in clock:
                try:
                    df = "%s %s" % (i, ii)
                    return datetime.datetime.strptime(str_datetime.strip(),
                                                      df.strip())
                except ValueError:
                    continue

    @staticmethod
    def time_normalization(date_time):
        if date_time:
            expression_1 = "(20\d{2}([\.\-/|年月\s]{0,3}\d{1,2}){2}日?(\s?\d{2}:\d{2}(:\d{2})?)?)"
            expression_1 = re.compile(expression_1)
            date_time_group_1 = expression_1.search(date_time)

            expression_2 = "({year}([\.\-/|年月\s]{0,3}\d{1,2}){2}日?(\s?\d{2}:\d{2}(:\d{2})?)?)".replace(
                '{year}', str(datetime.datetime.now().year)[-2:])
            expression_2 = re.compile(expression_2)
            date_time_group_2 = expression_2.search(date_time)
            number_head_base_regx = '([\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343\u4e07\u96f6\u3007]*[\s]*|[0-9]*[\s]*)%s'

            expression_3 = re.compile("[M][o][n][a-zA-Z\s0-9:]+[0-9]")
            date_time_group_3 = expression_3.search(date_time)
            date_time_text = str(date_time).strip().replace(' ', '').replace(' ', '')
            if date_time_group_1:
                date_time = date_time_group_1.group().replace('/', '-').replace(
                    '.', '-') \
                    .replace('年', '-').replace('月', '-').replace('日', '')

            elif "月" in date_time:
                try:
                    date_time = date_time.replace('年', '').replace('日', '')
                    ns = copy.deepcopy(date_time)
                    ns = ns.split()
                    for yue in range(len(ns)):
                        if '月' in ns[yue]:
                            ns[yue] = TimeFormat.chinese_to_arabic_month(
                                ns[yue].replace('月', '').replace(',', ''))
                            ns[yue] = '%s,' % ns[yue]
                    ns = ' '.join(ns)
                    date_time = TimeFormat.chinese_to_arabic(ns)
                except Exception as E:
                    pass
            elif "昨天" in date_time_text:
                ns = date_time.replace('昨天', '')
                ns = str(datetime.datetime.now())[:10] + ns
                d = TimeFormat.str_datetime(ns)
                if d:
                    t = d.timetuple()
                    time_stamp = int(time.mktime(t))
                    time_stamp = float(str(time_stamp) + str(
                        "%06d" % d.microsecond)) / 1000000 - 24 * 3600
                    date_time = TimeFormat.timestamp_datetime_str(int(time_stamp))

            elif "前天" in date_time_text:
                ns = date_time.replace('前天', '')
                ns = str(datetime.datetime.now())[:10] + ns
                d = TimeFormat.str_datetime(ns)
                t = d.timetuple()
                time_stamp = int(time.mktime(t))
                time_stamp = float(str(time_stamp) + str(
                    "%06d" % d.microsecond)) / 1000000 - 2 * 24 * 3600
                date_time = TimeFormat.timestamp_datetime_str(int(time_stamp))

            elif '天前' in date_time_text:
                cleaned = re.compile(number_head_base_regx % "天前")
                ns = cleaned.findall(date_time)
                if ns:
                    ns = ns[0]
                    ns = ns.replace('天前', '').replace(' ', '').replace(' ', '')
                    ns = TimeFormat.chinese_to_arabic_month(ns)
                    date_time = (datetime.datetime.now() - datetime.timedelta(
                        days=int(ns), hours=0))
                    date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")

            elif '小时前' in date_time_text:
                cleaned = re.compile(number_head_base_regx % "小时前")
                ns = cleaned.findall(date_time)
                if ns:
                    ns = ns[0]
                    ns = ns.replace('小时前', '').replace(' ', '').replace(' ', '')
                    ns = TimeFormat.chinese_to_arabic_month(ns)
                    date_time = (datetime.datetime.now() - datetime.timedelta(
                        days=0, hours=int(ns)))
                    date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")

            elif '分钟前' in date_time_text:
                cleaned = re.compile(number_head_base_regx % "分钟前")
                ns = cleaned.findall(date_time)
                if ns:
                    ns = ns[0]
                    ns = ns.replace('分钟前', '').replace(' ', '').replace(' ', '')
                    ns = TimeFormat.chinese_to_arabic_month(ns)
                    date_time = (datetime.datetime.now() - datetime.timedelta(
                        days=0, hours=0, minutes=int(ns)))
                    date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
            elif '刚刚' in date_time_text or '刚才' in date_time_text:
                date_time = datetime.datetime.now().strftime('%Y-%m-%d')
            elif date_time_group_2 and not date_time_group_1:
                date_time = date_time_group_2.group()

            elif ('cst' or 'CST' in date_time) and date_time_group_3:
                cst_time = date_time_group_3.group()
                try:
                    date_time = time.strptime(cst_time,
                                              '%a %b %d %H:%M:%S CST %Y')
                    date_time = time.strftime('%Y-%m-%d %H:%M:%S', date_time)
                except Exception as E:
                    pass

            if date_time:
                data = TimeFormat.str_datetime(date_time)
                if data:
                    data = data.strftime("%Y-%m-%d %H:%M:%S")
                    return data

    @staticmethod
    def datetime_str(datetime_instance):
        return datetime_instance.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def timestamp_datetime_str(timestamp):
        """
        格式化时间戳为%Y-%m-%d %H:%M:%S时间格式
        :param timestamp: <str> 时间戳
        :return: <str> 格式为%Y-%m-%d %H:%M:%S时间
        """
        date = datetime.datetime.fromtimestamp(float(timestamp)).strftime(
            '%Y-%m-%d %H:%M:%S')
        return date

    @staticmethod
    def str_datetime_timestamp(str_datetime):
        date = datetime.datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")
        timestamp = time.mktime(date.timetuple())
        return timestamp

    @staticmethod
    def the_other_day(num=5):
        return datetime.datetime.now() - datetime.timedelta(days=num)

    @staticmethod
    def datetime_now_str():
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return now

    @staticmethod
    def pub_time(date):
        redate = re.findall('[0-9]\d*', date)
        if redate:
            redate = redate[0]
        if (not isinstance(redate, list)) and len(
                redate) == 8 and '-' not in date:
            date = datetime.datetime.strptime(redate, "%Y%m%d")
            return date.strftime("%Y-%m-%d")
        else:
            return date

    @staticmethod
    def push_id_generator(data, rc, r_key, logger=None):
        default = {
            'news': 1,
            'wechat': 2
        }
        job_type = data.get('job_type')
        try:
            data['id'] = int(data.get('id')) * 100 + default.get(job_type)
        except Exception as E:
            data['id'] = 0
            data['error_process'] = '推送唯一id生成错误'
            data['error_record'] = str(traceback.format_exc())
            rc.json_push(r_key, data)
            if logger:
                logger.error('推送唯一id生成错误', extra=data)
        return data

    @staticmethod
    def normalize_dom(url, dom_bytes):
        """
        格式化html
        :param url: <str> 网址
        :param dom_bytes: <bytes> html字节码
        :return: <obj> lxml的html对象
        """
        if isinstance(dom_bytes, str):
            dom_bytes = dom_bytes.encode('utf-8')
        if isinstance(dom_bytes, bytes):
            encoding = chardet.detect(dom_bytes)['encoding']
            if not encoding:
                encoding = 'utf-8'
            dom_bytes = dom_bytes.decode(encoding, 'ignore')
            doc = lxml.html.fromstring(dom_bytes)
            doc.make_links_absolute(base_url=url)
            return doc


if __name__ == '__main__':
    a = TimeFormat.time_normalization('')
    # b = Format.time_normalization('2018年06月06日 发布\n 01:00:00')
    # c = Format.time_normalization('2018-07-02 08:00')
    # d = Format.time_normalization("Jun 28, 2018")
    # e = Format.time_normalization("Friday, November 30, 2016")
    # f = Format.time_normalization("10分钟前")
    # g = Format.time_normalization("11小时前")
    # h = Format.time_normalization("昨天")
    # i = Format.time_normalization("前天")
    # j = Format.time_normalization("3天前")
    # k = Format.time_normalization("20 十一月 2018")
    # l = Format.time_normalization("20 十月 二零一八")
    # m = Format.time_normalization("19 June 2018")
    # n = Format.time_normalization("[18-08-14]")
    p = TimeFormat.time_normalization('刚刚')
    print(p)
