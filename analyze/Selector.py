# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import data.KDataDao as kd
from IPython.display import display,clear_output,HTML
import ipywidgets as widgets

class Selector():
    """股票工具类"""

    def __init__(self,select=True):
        self.idx = 0
        self.codes = []
        if select:
            self.select()
        else:
            self.codes = kd.get_stock_codes()
        if len(self.codes) < 1:
            print "no stock find!"
        else:
            self.firgueButton()

    def select(self):
        """筛选股票"""
        print "selecting......"
        codes = kd.get_stock_codes()
        for code in codes:
            list = kd.get_k_data(code, "2016-01-01")
            if len(list) < 3:
                continue
            if self.analyze(list)==True:
                self.codes.append(code)
        print "complete slecet!"

    def analyze(self,list):
        """分析股票"""
        print "analyze需要子类继承"


    def figurePre(self):
        if len(self.codes) < 1:
            return
        self.idx -= 1
        if self.idx < 0:
            self.idx = 0
        self.firgue(self.codes[self.idx])


    def figureNext(self):
        if len(self.codes) < 1:
            return
        self.idx += 1
        if len(self.codes) == self.idx:
            self.idx = len(self.codes) - 1
        self.firgue(self.codes[self.idx])
    def fresh(self):
        if len(self.codes) < 1:
            return
        self.firgue(self.codes[self.idx])
    def firgue(self,code):
        """显示股票,需要子类继承"""
        print "firgue需要子类继承"

    def firgueButton(self):
        """画选按键"""
        nextBtn = widgets.Button(description="next")
        preBtn = widgets.Button(description="pre")
        freshBtn = widgets.Button(description="fresh")
        textBox = widgets.IntText(layout=widgets.Layout(width='50px'))
        text = widgets.HTML(
            value="selecting....",
            placeholder='',
            description='',
            layout=widgets.Layout(top='3px')
        )
        def next_clicked(a):
            self.figureNext()
            text.value = "- " + str(len(self.codes))
            textBox.value = self.idx + 1
        def pre_clicked(a):
            self.figurePre()
            text.value = "- " + str(len(self.codes))
            textBox.value = self.idx + 1
        def fresh_clicked(a):
            self.fresh()
            text.value = "- " + str(len(self.codes))
            textBox.value = self.idx + 1
        def change(change):
            if textBox.value <= 0:
                textBox.value = 1
            if textBox.value > len(self.codes):
                textBox.value = len(self.codes)
            self.idx = textBox.value-1
        nextBtn.on_click(next_clicked)
        preBtn.on_click(pre_clicked)
        freshBtn.on_click(fresh_clicked)
        textBox.observe(change, names='value')
        display(widgets.Box([preBtn, nextBtn, freshBtn, textBox, text]))
        text.value = "- " + str(len(self.codes))
        textBox.value = self.idx + 1