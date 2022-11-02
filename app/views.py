from http.server import executable
from django.shortcuts import render
import requests
from django.http import JsonResponse, HttpResponse
from bs4 import BeautifulSoup as bs
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import re
import time
import datetime
import json
from app.models import Record
# Create your views here.
def search(request):
    a = wd.Chrome()
    a.get('https://www.sejong.go.kr/bbs/R0071/list.do')
    a.find_element(By.CSS_SELECTOR, 'input[name=searchKeyword]').send_keys('라벨러')
    a.find_element(By.CSS_SELECTOR, 'span.btn--submit >input').click()
    x = a.find_elements(By.CSS_SELECTOR, 'td[data-cell-header = 등록일]')
    list_ = []
    dic ={}
    count = 0
    try:
        for i in x:
            print(i.text)
            upload_time = datetime.datetime.strptime(i.text, '%Y-%m-%d')
            list_.append(upload_time)
        recent_ = min(list_)
        time_delta = datetime.datetime.now()-recent_
        if time_delta<datetime.timedelta(days=10):
            print('찾았다')
            dic = {'응답' : '찾았다'}
            print(dic)
            Record(record_date = datetime.datetime.now().strftime('%Y-%m-%d'), record_response = '10일이내 최근게시물존재').save()
            return JsonResponse(dic, safe=False)
        else:
            print('오래지난 게시물') 
            dic = {'응답' : '오래지난게시물'}
            print(dic)
            Record(record_date = datetime.datetime.now().strftime('%Y-%m-%d'), record_response = '10일이상 된 게시물 있음').save()
            
            return JsonResponse(dic, safe=False)   
    except:
        time.sleep(10)
        dic = {'응답' : '찾지못했다'}
        Record(record_date = datetime.datetime.now().strftime('%Y-%m-%d'), record_response = '찾지못함').save()
        print(dic)
        return JsonResponse(dic, safe=False)   

def alert(request):
    a = Record.objects.all()
    return render(request, 'alert.html', {'list':a})