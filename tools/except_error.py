class UrlNotHttpError(Exception):
    """
    http or https not in url error
    """

    def __init__(self, err='target url error'):
        Exception.__init__(self, err)


class GetLabalSelectorError(Exception):
    """
    get labal selector error when use xpath
    """

    def __init__(self, err='labalSelector must be a lxml.etree._Element or html type'):
        Exception.__init__(self, err)


class ExtractorDataNullError(Exception):
    """
    抽取的数据为空
    """

    def __init__(self, err='Please check extractor data, it must not be null'):
        Exception.__init__(self, err)


class DownloadError(Exception):
    """
    下载异常
    """

    def __init__(self, err='download error'):
        Exception.__init__(self, err)


class JSRenderError(Exception):
    """
    JS渲染异常
    """
    pass


class ResponseError(Exception):
    """
    请求响应获取失败异常
    """
    pass


class CheckError(Exception):
    """
    数据校验异常
    """
    pass
