# coding=gbk
'''
Created on 2014��12��29��

@author: Administrator
'''
import re
import thread
import time
import urllib2
import urllib  



#---------------------�������°ٿ�---------------------
class Spider_Model:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False
        
    # �����Ӷ���  ����ӵ��б���ͬ�·����б�
    def GetPage(self, page):
        myUrl = "http://m.qiushibaike.com/hot/page/" + page  
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
        headers = { 'User-Agent' : user_agent } 
        req = urllib2.Request(myUrl, headers=headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        # encode�������ǽ�unicode����ת��������������ַ���  
        # decode�������ǽ�����������ַ���ת����unicode����  
        unicodePage = myPage.decode("utf-8")
        
        # �ҳ�����class="content"��div���  
        # re.S������ƥ��ģʽ��Ҳ����.����ƥ�任�з�  
        
        myItems = re.findall('<div.*?class="content".*?title="(.*?)">(.*?)</div>', unicodePage, re.S)
        items = []
        for item in myItems:
            # item �е�һ����div�ı��⣬Ҳ����ʱ��  
            # item �еڶ�����div�����ݣ�Ҳ��������  
            items.append([item[0].replace("\n", ""), item[1].replace("\n", "")])
            return items
        # ���ڼ����µĶ���
    def LoadPage(self):
        # ����û�δ����quit��һֱ����  
        while self.enable:
            if len(self.pages) < 2:
                try:
                    myPage = self.GetPage(str(self.page))
                    self.page += 1
                    self.pages.append(myPage)
                except:
                    print '�޷��������°ٿ�'
            else:
                time.sleep(1)
        
    
    def ShowPage(self, nowPage, page):
        for items in nowPage:
            print u'��%dҳ' % page , items[0]  , items[1]  
            myInput = raw_input()  
            if myInput == "quit":  
                self.enable = False  
                break  
    def Start(self):
        self.enable = True
        page = self.page
        
        print '���ڼ��dՈ���ᡣ������'
        # �½�һ���̺߳�̨���ض��Ӳ�����
        thread.start_new_thread(self.LoadPage, ())
        
        
        #----------- ���ش������°ٿ� -----------  
        while self.enable:  
            # ���self��page�����д���Ԫ��  
            if self.pages:  
                nowPage = self.pages[0]  
                del self.pages[0]  
                self.ShowPage(nowPage, page)  
                page += 1  
                
                    
#----------- �������ڴ� -----------  
print u""" 
--------------------------------------- 
   �����ܰ����� 
   �汾��0.1 
   ���ߣ�liuxy 
   ���ڣ�2014-12-29
   ���ԣ�Python 2.7 
   ����������quit�˳��Ķ����°ٿ� 
   ���ܣ����»س�����������յ��ܰ��ȵ� 
--------------------------------------- 
"""
print '�밴�»س�������յ��ܰ����ݣ�'
raw_input(' ')
myModel = Spider_Model()
myModel.Start();
