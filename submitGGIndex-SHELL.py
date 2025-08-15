import requests
import random
import string
import time
from google.oauth2 import service_account
import google.auth.transport.requests
import threading
import PySimpleGUI as sg

# googleJsonFile 文件选择器
def getACToken(googleJsonFile):
    # 加载你的密钥
    credentials = service_account.Credentials.from_service_account_file(
        googleJsonFile,  # 替换为你的密钥文件路径
        scopes=['https://www.googleapis.com/auth/indexing']
    )
    # 获取访问令牌
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)
    access_token = credentials.token
    return access_token
    # print(access_token)



def submit_index_request(url, access_token):
    api_url = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "url": url,
        "type": "URL_UPDATED"
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        window['-OUTPUT-'].print(f"成功提交  {url}")
    else:
        window['-OUTPUT-'].print(f"!!!失败请求 {url}. Error: {response.text}")



# 1.随机二级名,txt中只有主域名 url自己构建
# https://{随机字符n}.google.com/{随机字符n}/{随机字符n}.html # rSD=random.choices(string.ascii_letters, k=5)
# random.choices(string.ascii_lowercase + string.digits, k=6) # vvv
# rLen 随机长度  # k=5 随机长度 随机类型 
def buildUrlsList(topDomains,rLen):
# def buildUrlsList(topDomains,subdNum,rLen):
    urls=[]
    for domain in topDomains:
        
        # for sdi in range(subdNum):
            rSubDM = ''.join(random.choices(string.ascii_lowercase + string.digits, k=rLen))
            for _ in range(200):
                rSitePath=''.join(random.choices(string.ascii_lowercase + string.digits, k=rLen))
                rPageName=''.join(random.choices(string.ascii_lowercase + string.digits, k=rLen))
                # url=f"https://{rSubDM}.{domain}/{rSitePath}/{rPageName}.html" # 蜘蛛池用二级泛域名
                url=f"{domain}/{rSitePath}/{rPageName}.html" # https://emasabc.com.br/emasabc/abcnews.php?9pzyq.html 
                urls.append(url)
    return urls
    # print(111)



# 从txt文件中读取网址列表
topDomainTxtFile='1.txt'
def getTopDMsList(topDomainTxtFile):
    with open(topDomainTxtFile, 'r') as file:
        topDomains = file.read().splitlines()
    return topDomains

# 逐个向Google提交索引请求 
def batchRequestGG(urls,access_token,googleJsonFile):

    totalNums=len(urls)
    urlI=1
    for url in urls:
        if stop_event.is_set():
            break
        print(f"{urlI}/{totalNums}")
        submit_index_request(url, access_token)
        # time.sleep(1)
        urlI=urlI+1
        if urlI % 100 == 0:
            access_token = getACToken(googleJsonFile)

stop_event = threading.Event()

def start_main(window,values):
     while True:
        if stop_event.is_set():
            break

        window['-OUTPUT-'].print(event,values)
        googleJsonFile = values[0]
        topDomainTxtFile = values[1]
        rType = values[2]
        rLen = int(values[3])
        # subdNum = int(values[4])#
        access_token = getACToken(googleJsonFile)
        topDomains = getTopDMsList(topDomainTxtFile)
        urls = buildUrlsList(topDomains, rLen)
        # urls = buildUrlsList(topDomains,subdNum, rLen)
        print(len(urls))
        # print(urls)
        batchRequestGG(urls, access_token,googleJsonFile)

sg.theme('BrightColors') #['Black', 'BlueMono', 'BluePurple', 'BrightColors', 'BrownBlue', 'Dark', 'Dark2', 'DarkAmber', 'DarkBlack', 'DarkBlack1', 'DarkBlue', 'DarkBlue1', 'DarkBlue10', 'DarkBlue11', 'DarkBlue12', 'DarkBlue13', 'DarkBlue14', 'DarkBlue15', 'DarkBlue16', 'DarkBlue17', 'DarkBlue2', 'DarkBlue3', 'DarkBlue4', 'DarkBlue5', 'DarkBlue6', 'DarkBlue7', 'DarkBlue8', 'DarkBlue9', 'DarkBrown', 'DarkBrown1', 'DarkBrown2', 'DarkBrown3', 'DarkBrown4', 'DarkBrown5', 'DarkBrown6', 'DarkBrown7', 'DarkGreen', 'DarkGreen1', 'DarkGreen2', 'DarkGreen3', 'DarkGreen4', 'DarkGreen5', 'DarkGreen6', 'DarkGreen7', 'DarkGrey', 'DarkGrey1', 'DarkGrey10', 'DarkGrey11', 'DarkGrey12', 'DarkGrey13', 'DarkGrey14', 'DarkGrey15', 'DarkGrey2', 'DarkGrey3', 'DarkGrey4', 'DarkGrey5', 'DarkGrey6', 'DarkGrey7', 'DarkGrey8', 'DarkGrey9', 'DarkPurple', 'DarkPurple1', 'DarkPurple2', 'DarkPurple3', 'DarkPurple4', 'DarkPurple5', 
'DarkPurple6', #'DarkPurple7', 'DarkRed', 'DarkRed1', 'DarkRed2', 'DarkTanBlue', 'DarkTeal', 'DarkTeal1', 'DarkTeal10', 'DarkTeal11', 'DarkTeal12', 'DarkTeal2', 'DarkTeal3', 'DarkTeal4', 'DarkTeal5', 'DarkTeal6', 'DarkTeal7', 'DarkTeal8', 'DarkTeal9', 'Default', 'Default1', 'DefaultNoMoreNagging', 'GrayGrayGray', 
'Green', #'GreenMono', 'GreenTan', 'HotDogStand', 'Kayak', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightBlue5', 'LightBlue6', 'LightBlue7', 'LightBrown', 'LightBrown1', 'LightBrown10', 'LightBrown11', 'LightBrown12', 'LightBrown13', 'LightBrown2', 'LightBrown3', 'LightBrown4', 'LightBrown5', 'LightBrown6', 'LightBrown7', 'LightBrown8', 'LightBrown9', 'LightGray1', 'LightGreen', 'LightGreen1', 'LightGreen10', 'LightGreen2', 'LightGreen3', 'LightGreen4', 'LightGreen5', 'LightGreen6', 'LightGreen7', 'LightGreen8', 'LightGreen9', 'LightGrey', 'LightGrey1', 'LightGrey2', 'LightGrey3', 'LightGrey4', 'LightGrey5', 'LightGrey6', 'LightPurple', 'LightTeal', 'LightYellow', 'Material1', 'Material2', 'NeutralBlue', 'Purple', 'Python', 'PythonPlus', 'Reddit', 'Reds', 'SandyBeach', 'SystemDefault', 'SystemDefault1', 'SystemDefaultForReal', 'Tan', 'TanBlue', 'TealMono', 'Topanga']
# 界面设计
layout = [
    [sg.Text('Google Json：'), sg.Input(), sg.FileBrowse()],
    [sg.Text('主域名文件：'), sg.Input(), sg.FileBrowse()],
    
    [sg.Text('随机字符类型：'), sg.Input(default_text='随机字符',readonly=True)],
    [sg.Text('随机字符长度：'), sg.Input(default_text='5')],
    # [sg.Text('每站二级数量：'), sg.Input(default_text='1')], #subdNum

    [sg.Output(size=(70, 16),key="-OUTPUT-")],
    [sg.Button('开始'), sg.Button('停止'), sg.Button('关闭')]
]

# 创建窗口
window = sg.Window('Google Indexing', layout)

# 事件循环
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == '关闭':
        break
    elif event == '开始':
        stop_event.clear()
        thread = threading.Thread(target=start_main, args=( window,values))
        thread.start()
    elif event == '停止':
        window['-OUTPUT-'].print("stop---")
        stop_event.set()

window.close()


#submitGGIndex-SHELL.py 
# pyinstaller -F -w -i td.ico submitGGIndex-SHELL.py