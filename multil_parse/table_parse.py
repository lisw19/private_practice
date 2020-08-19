import lxml
import chardet

from lxml import etree

from tools.except_error import (UrlNotHttpError,
                                GetLabalSelectorError)


def to_xpath(html, expression, base_url=False):
    """
    html 转为dom节点解析
    :param html: html源码
    :param expression: xpath
    :param base_url: base_url
    :return:
    """

    def __etree_to_string(bytes_obj):
        """
        转换lxml dom对象为string
        """
        return etree.tostring(bytes_obj, encoding='utf-8').decode('utf-8')

    def __get_dom(url, html):
        """
        格式化dom树，补全链接绝对路径
        """
        if isinstance(html, str):
            html = html.encode('utf-8')
        encoding = chardet.detect(html)['encoding']
        if not encoding:
            encoding = 'utf-8'
        html = html.decode(encoding, 'ignore')
        dom = lxml.html.fromstring(html)
        dom.make_links_absolute(base_url=url)
        return dom

    if base_url and (isinstance(html, str) or isinstance(html, bytes)):
        html = __get_dom(base_url, html)
    results = html.xpath(expression)
    if not results or not isinstance(results, list):
        return results
    if isinstance(results[0], lxml.html.HtmlElement):
        results = [__etree_to_string(i) for i in results]
    return results


def get_labal_content(
        labal_selector, labal_xpath, first_item=False,
        is_split_labal=False, split_labal=',', html_key='html'):
    """
    get labal content by xpath
    Params:
        labal_selector: origin labal/html
        labal_xpath: xpath to get content
        first_item: if get the first item
        is_split_labal: labal list merge to a string
        split_labal: a string to join labal_result list
    Return:
        that labal content
    """
    if isinstance(labal_selector, lxml.etree._Element):
        labal_result = labal_selector.xpath(labal_xpath)
    elif isinstance(labal_selector, str) and html_key in labal_selector:
        parser = etree.HTMLParser(encoding='utf-8')
        labal_selector = etree.HTML(labal_selector, parser)
        labal_result = labal_selector.xpath(labal_xpath)

    else:
        raise GetLabalSelectorError(
            'labal_selector must be a html or selector type')
    if not labal_result:
        return ''
    if first_item:
        return labal_result[0].strip()
    if is_split_labal:
        labal_result = list(filter(lambda x: x.strip(), labal_result))
        labal_result = list(map(lambda x: x.strip(), labal_result))
        result_labal = split_labal.join(labal_result)
    else:
        result_labal = labal_result
    return result_labal
