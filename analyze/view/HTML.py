# -*- coding: utf-8 -*-
from IPython.display import display,clear_output,HTML
import os
package_directory = os.path.dirname(os.path.abspath(__file__))
def show(fileName,params={}):
    """显示HTML
    :param fileName:html文件名
    :param params:参数,dic对象
    """
    #获取HTML
    html = ''
    with open(package_directory+'/html/' + fileName) as htmlFile:
        html = htmlFile.read()
    #替换参数
    for key, value in params.items():
        html = html.replace("_"+str(key)+"_",str(value))
    display(HTML(html))
    return html

# d = {"code":1}
# print show("stock.html",d)