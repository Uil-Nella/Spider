# coding=gbk
'''
Created on 2014年12月29日

@author: Administrator
'''
import re
import thread
import time
import urllib2
import urllib  



#---------------------加载糗事百科---------------------
class Spider_Model:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False
        
    # 遍历子段子  并添加到列表中同事返回列表
    def GetPage(self, page):
        myUrl = "http://m.qiushibaike.com/hot/page/" + page  
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
        headers = { 'User-Agent' : user_agent } 
        req = urllib2.Request(myUrl, headers=headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        # encode的作用是将unicode编码转换成其他编码的字符串  
        # decode的作用是将其他编码的字符串转换成unicode编码  
        unicodePage = myPage.decode("utf-8")
        
        # 找出所有class="content"的div标记  
        # re.S是任意匹配模式，也就是.可以匹配换行符  
        
        myItems = re.findall('<div.*?class="content".*?title="(.*?)">(.*?)</div>', unicodePage, re.S)
        items = []
        for item in myItems:
            # item 中第一个是div的标题，也就是时间  
            # item 中第二个是div的内容，也就是内容  
            items.append([item[0].replace("\n", ""), item[1].replace("\n", "")])
            return items
        # 用于加载新的段子
    def LoadPage(self):
        # 如果用户未输入quit则一直运行  
        while self.enable:
            if len(self.pages) < 2:
                try:
                    myPage = self.GetPage(str(self.page))
                    self.page += 1
                    self.pages.append(myPage)
                except:
                    print '无法连接糗事百科'
            else:
                time.sleep(1)
        
    
    def ShowPage(self, nowPage, page):
        for items in nowPage:
            print u'第%d页' % page , items[0]  , items[1]  
            myInput = raw_input()  
            if myInput == "quit":  
                self.enable = False  
                break  
    def Start(self):
        self.enable = True
        page = self.page
        
        print '正在加載請稍後。。。。'
        # 新建一個线程后台加载段子并储存
        thread.start_new_thread(self.LoadPage, ())
        
        
        #----------- 加载处理糗事百科 -----------  
        while self.enable:  
            # 如果self的page数组中存有元素  
            if self.pages:  
                nowPage = self.pages[0]  
                del self.pages[0]  
                self.ShowPage(nowPage, page)  
                page += 1  
                
                    
#----------- 程序的入口处 -----------  
print u""" 
--------------------------------------- 
   程序：糗百爬虫 
   版本：0.1 
   作者：liuxy 
   日期：2014-12-29
   语言：Python 2.7 
   操作：输入quit退出阅读糗事百科 
   功能：按下回车依次浏览今日的糗百热点 
--------------------------------------- 
"""
print '请按下回车浏览今日的糗百内容：'
raw_input(' ')
myModel = Spider_Model()
myModel.Start();
