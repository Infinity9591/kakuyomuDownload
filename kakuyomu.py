import requests
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

from webdriver_manager.microsoft import EdgeChromiumDriverManager
def getNovelChapterList():
    chapList=re.findall(chapterListDiv,html,re.DOTALL)[1:]
    print(chapList)
    print('%s chapters detected'%len(chapList))
    return chapList

def getChapterTitle(str):
    chapter_title=re.findall('<p class="widget-episodeTitle js-vertical-composition-item">(.*?)<',str)[0]
    return chapter_title

def DL(fromchap):
    global headers
    i=fromchap
    for chap in chapNumList[fromchap-1:]:
        chapter_url=url+'/episodes/'+chap
        print('chapter: '+str(i)+'  '+chapter_url)

        rep=requests.get(chapter_url)
        html=rep.text
        chapter_title=getChapterTitle(html)
        content=re.findall('<p id="p.*">(.*?)</p>',html)
        contentUPDATED=[]
        for sentence in content:
            sentence = sentence.replace('<br />','\n')
            sentence = sentence.replace('<ruby>','')
            sentence = sentence.replace('</ruby>','')
            sentence = sentence.replace('<rp>','')
            sentence = sentence.replace('</rp>','')
            sentence = sentence.replace('<rt>','')
            sentence = sentence.replace('</rt>','')
            sentence = sentence.replace('<rb>','')
            sentence = sentence.replace('<span>', '')
            sentence = sentence.replace('</span>', '')
            sentence = sentence.replace('<em>', '')
            sentence = sentence.replace('</em>', '')
            #signal character superpose
            sentence = sentence.replace('</rb>','//')
            sentence += '\n'
            contentUPDATED.append(sentence)

        createFile(i,chapter_title,contentUPDATED,chapter_url)
        i+=1

def createDir():
    dirlist=os.listdir(os.getcwd())
    if DirName not in dirlist:
        os.mkdir('%s'%DirName)

def createFile(i,chapter_title,chapter_content,chapter_url):
    file = open('%s\%d_%s.txt' % (DirName, i, chapter_title), 'w+', encoding='utf-8')
    file.write(chapter_url + '\n')
    file.write(chapter_title + '\n')
    for sentence in chapter_content:
        file.write(sentence)
    file.close()


novelNumber=input('give the novel serie number: ')
url='https://kakuyomu.jp/works/%s'%novelNumber
titlediv='href="/works/%s'%novelNumber
chapterListDiv='/works/%s/episodes/(.*?)"'%novelNumber

options = webdriver.EdgeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)

driver.get(url)
time.sleep(3)
buttons = driver.find_elements(By.CSS_SELECTOR, ".Button_button__kcHya.Button_widthfill__fMKti.Button_heightauto__BdNgx")

versions=[]

driver.execute_script("arguments[0].click();", buttons[0])

print('Version:')

i = 0;

for button in buttons:
    try:
        h3element = button.find_element(By.CSS_SELECTOR, ".Heading_heading__lQ85n.Heading_left__RVp4h.Heading_size-1s___G7AX")
        if (h3element) :
            versions.append(button)
        print(h3element.text + ' [' + str(i) + ']')
        time.sleep(1)
        i+=1
    except:
        pass

versionOption = input('select version? [0,1,...]: ')
driver.execute_script("arguments[0].click();", versions[int(versionOption)])

html = driver.page_source
DirName=str(novelNumber)
createDir()
chapNumList=getNovelChapterList()
DL(1)
driver.quit()
