import os
import shutil

from tools.time_package import time_section


def docu_list(path, choice_type='.html'):
    """
    get all the document names from path
    parm:
        path:需要遍历的路径
        choice_type:锁定文件类型, 为空时返回文件夹里所有类型文件
    return:
        文件全路径的列表
    """
    doc_nums = []
    if not path.endswith('/'):
        path += '/'
    if not os.path.isdir(path):
        return
    # root为遍历路径，dirs当前遍历路径下的目录，list当前遍历目录下的文件名
    for root, dirs, listt in os.walk(path):
        for i in listt:
            rootPath = '%s%s' % (root, i)
            docType = os.path.splitext(i)[1]
            if not choice_type:
                doc_nums.append(rootPath)
            elif choice_type == docType:
                doc_nums.append(rootPath)
    return doc_nums


def docu_check(path_address, is_make_file=False):
    """
    check if exsited by path
    dir:/home/lvpx/spiders/html/cde/clinical/lList/2018/5/5/
    doc:/home/lvpx/spiders/html/cde/clinical/lList/2018/5/5/2323.html
    """
    if os.path.exists(path_address):
        return
    if os.path.isdir(path_address):
        os.makedirs(path_address)
        return
    dirname = os.path.dirname(path_address)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    if is_make_file:
        fn = open(path_address, 'w')
        fn.close()
    return True


def docu_html_path(root_dir=os.environ.get('CRAWLER_ROOT_PATH') + '/html',
                   file_dir='/cde/chinadrugtrials/list/', time_path_type=False):
    """
    generate html path
    Parms:
        time_path_type: a time-before path or a time-after path
    Return:
        a path including time path
    """
    year = time_section('year')
    month = time_section('month')
    day = time_section('day')
    dayTime = '{0}/{1}/{2}/'.format(year, month, day)
    day_time_be = '/{0}/{1}/{2}'.format(year, month, day)
    if not time_path_type:
        html_dir = root_dir + file_dir + dayTime
    else:
        html_dir = root_dir + day_time_be + file_dir
    docu_check(html_dir)
    return html_dir


def remove_path(target_path):
    """
    删除指定目录文件
    """
    if not os.path.exists(target_path):
        return True
    if os.path.isfile(target_path):
        os.remove(target_path)
    else:
        shutil.rmtree(target_path)
    return True


if __name__ == '__main__':
    # print docu_html_path(file_dir='/market/bidChinaemed/detail/', time_path_type=True)
    # print(docu_html_path(file_dir='/market/bidChinaemed/detail/'))
    # print(docu_html_path(file_dir='/cde/cdeAcceptType/list', time_path_type=True))
    # html_path = docu_html_path(file_dir='/cde/cdeAcceptType/list', time_path_type=True)
    # print(docu_list(html_path))
    # docu_html_path(file_dir='/cde_queue_check/cde/newQueue/chineseDrug/reexamine/', root_dir='./')
    print(docu_list(path='./2019/12/10/file_server/1575973182',
                    choice_type=''))
