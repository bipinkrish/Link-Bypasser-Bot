import re
import requests
import base64
from urllib.parse import unquote, urlparse, parse_qs
import time
import cloudscraper
from bs4 import BeautifulSoup
from lxml import etree
import hashlib
import json
from dotenv import load_dotenv
load_dotenv()


###############################################################
# psa 

def try2link_bypass(url):
	client = cloudscraper.create_scraper(allow_brotli=False)
	
	url = url[:-1] if url[-1] == '/' else url
	
	params = (('d', int(time.time()) + (60 * 4)),)
	r = client.get(url, params=params, headers= {'Referer': 'https://newforex.online/'})
	
	soup = BeautifulSoup(r.text, 'html.parser')
	inputs = soup.find(id="go-link").find_all(name="input")
	data = { input.get('name'): input.get('value') for input in inputs }	
	time.sleep(7)
	
	headers = {'Host': 'try2link.com', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://try2link.com', 'Referer': url}
	
	bypassed_url = client.post('https://try2link.com/links/go', headers=headers,data=data)
	return bypassed_url.json()["url"]
		

def try2link_scrape(url):
	client = cloudscraper.create_scraper(allow_brotli=False)	
	h = {
	'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
	}
	res = client.get(url, cookies={}, headers=h)
	url = 'https://try2link.com/'+re.findall('try2link\.com\/(.*?) ', res.text)[0]
	return try2link_bypass(url)
    

def psa_bypasser(psa_url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    r = client.get(psa_url)
    soup = BeautifulSoup(r.text, "html.parser").find_all(class_="dropshadowboxes-drop-shadow dropshadowboxes-rounded-corners dropshadowboxes-inside-and-outside-shadow dropshadowboxes-lifted-both dropshadowboxes-effect-default")
    links = ""
    for link in soup:
        try:
            exit_gate = link.a.get("href")
            links = links + try2link_scrape(exit_gate) + '\n'
        except: pass
    return links


##################################################################################################################
# rocklinks

def rocklinks(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'rocklinks.net' in url:
        DOMAIN = "https://blog.disheye.com"
    else:
        DOMAIN = "https://rocklinks.net"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    if 'rocklinks.net' in url:
        final_url = f"{DOMAIN}/{code}?quelle=" 
    else:
        final_url = f"{DOMAIN}/{code}"

    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(10)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("


################################################
# igg games

def decodeKey(encoded):
        key = ''

        i = len(encoded) // 2 - 5
        while i >= 0:
            key += encoded[i]
            i = i - 2
        
        i = len(encoded) // 2 + 4
        while i < len(encoded):
            key += encoded[i]
            i = i + 2

        return key

def bypassBluemediafiles(url, torrent=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Alt-Used': 'bluemediafiles.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',

    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    script = str(soup.findAll('script')[3])
    encodedKey = script.split('Create_Button("')[1].split('");')[0]


    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': url,
        'Alt-Used': 'bluemediafiles.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    params = { 'url': decodeKey(encodedKey) }
    
    if torrent:
        res = requests.get('https://dl.pcgamestorrents.org/get-url.php', params=params, headers=headers)
        soup = BeautifulSoup(res.text,"html.parser")
        furl = soup.find("a",class_="button").get("href")

    else:
        res = requests.get('https://bluemediafiles.com/get-url.php', params=params, headers=headers)
        furl = res.url
        if "mega.nz" in furl:
            furl = furl.replace("mega.nz/%23!","mega.nz/file/").replace("!","#")

    #print(furl)
    return furl

def igggames(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup = soup.find("div",class_="uk-margin-medium-top").findAll("a")

    bluelist = []
    for ele in soup:
        bluelist.append(ele.get('href'))
    bluelist = bluelist[6:-1]

    links = ""
    for ele in bluelist:
        if "bluemediafiles" in ele:
            links = links + bypassBluemediafiles(ele) + "\n"
        elif "pcgamestorrents.com" in ele:
            res = requests.get(ele)
            soup = BeautifulSoup(res.text,"html.parser")
            turl = soup.find("p",class_="uk-card uk-card-body uk-card-default uk-card-hover").find("a").get("href")
            links = links + bypassBluemediafiles(turl,True) + "\n"
        else:
            links = links + ele + "\n"

    return links[:-1]


###################################################
# script links

def getfinal(domain, url, sess):

    #sess = requests.session()
    res = sess.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup = soup.find("form").findAll("input")
    datalist = []
    for ele in soup:
        datalist.append(ele.get("value"))

    data = {
            '_method': datalist[0],
            '_csrfToken': datalist[1],
            'ad_form_data': datalist[2],
            '_Token[fields]': datalist[3],
            '_Token[unlocked]': datalist[4],
        }

    sess.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': domain,
            'Connection': 'keep-alive',
            'Referer': url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            }

    # print("waiting 10 secs")
    time.sleep(10) # important
    response = sess.post(domain+'/links/go', data=data).json()
    furl = response["url"]
    return furl


def getfirst(url):

    sess = requests.session()
    res = sess.get(url)

    soup = BeautifulSoup(res.text,"html.parser")
    soup = soup.find("form")
    action = soup.get("action")
    soup = soup.findAll("input")
    datalist = []
    for ele in soup:
        datalist.append(ele.get("value"))
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': action,
        'Connection': 'keep-alive',
        'Referer': action,
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    data = {'newwpsafelink': datalist[1], "g-recaptcha-response": RecaptchaV3()}
    response = sess.post(action, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    soup = soup.findAll("div", class_="wpsafe-bottom text-center")
    for ele in soup:
        rurl = ele.find("a").get("onclick")[13:-12]

    res = sess.get(rurl)
    furl = res.url
    # print(furl)
    return getfinal(f'https://{furl.split("/")[-2]}/',furl,sess)


################################################
# ola movies

def olamovies(url):
    
    print("this takes time, you might want to take a break.")
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': url,
            'Alt-Used': 'olamovies.ink',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
        }

    client = cloudscraper.create_scraper(allow_brotli=False)
    res = client.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup = soup.findAll("div", class_="wp-block-button")

    outlist = []
    for ele in soup:
        outlist.append(ele.find("a").get("href"))

    slist = []
    for ele in outlist:
        try:
            key = ele.split("?key=")[1].split("&id=")[0].replace("%2B","+").replace("%3D","=").replace("%2F","/")
            id = ele.split("&id=")[1]
        except:
            continue
        
        count = 3
        params = { 'key': key, 'id': id}
        soup = "None"
        # print("trying","https://olamovies.ink/download/&key="+key+"&id="+id)

        while 'rocklinks.net' not in soup and "try2link.com" not in soup:
            res = client.get("https://olamovies.ink/download/", params=params, headers=headers)
            soup = BeautifulSoup(res.text,"html.parser")
            soup = soup.findAll("a")[0].get("href")
            if soup != "":
                if "try2link.com" in soup or 'rocklinks.net' in soup:
                    # print("added", soup)
                    slist.append(soup)
                else:
                    # print(soup, "not addded")
                    pass
            else:
                if count == 0:
                    # print('moving on')
                    break
                else:
                    count -= 1
                    # print("retrying")
                
            # print("waiting 10 secs")
            time.sleep(10)

    # print(slist)
    final = []
    for ele in slist:
        if "rocklinks.net" in ele:
            final.append(rocklinks(ele))
        elif "try2link.com" in ele:
            final.append(try2link_bypass(ele))
        else:
            # print("passing",ele)
            pass
    #print(final)
    links = ""
    for ele in final:
        links = links + ele + "\n"
    return links[:-1]


###############################################
# katdrive

def parse_info_katdrive(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

def katdrive_dl(url,katcrypt):
    client = requests.Session()
    client.cookies.update({'crypt': katcrypt})
    
    res = client.get(url)
    info_parsed = parse_info_katdrive(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = {'x-requested-with': 'XMLHttpRequest'}
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except:
        return {'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url
    return info_parsed['gdrive_url']


###############################################
# hubdrive

def parse_info_hubdrive(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

def hubdrive_dl(url,hcrypt):
    client = requests.Session()
    client.cookies.update({'crypt': hcrypt})
    
    res = client.get(url)
    info_parsed = parse_info_hubdrive(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = {'x-requested-with': 'XMLHttpRequest'}
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except:
        return {'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url
    return info_parsed['gdrive_url']


#################################################
# drivefire

def parse_info_drivefire(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

def drivefire_dl(url,dcrypt):
    client = requests.Session()
    client.cookies.update({'crypt': dcrypt})
    
    res = client.get(url)
    info_parsed = parse_info_drivefire(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = {'x-requested-with': 'XMLHttpRequest'}
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except:
        return {'error': True, 'src_url': url}
    
    decoded_id = res.rsplit('/', 1)[-1]
    info_parsed = f"https://drive.google.com/file/d/{decoded_id}"
    return info_parsed


##################################################
# kolop

def parse_info_kolop(res):
    info_parsed = {}
    title = re.findall('>(.*?)<\/h4>', res.text)[0]
    info_chunks = re.findall('>(.*?)<\/td>', res.text)
    info_parsed['title'] = title
    for i in range(0, len(info_chunks), 2):
        info_parsed[info_chunks[i]] = info_chunks[i+1]
    return info_parsed

def kolop_dl(url,kcrypt):
    client = requests.Session()
    client.cookies.update({'crypt': kcrypt})
    
    res = client.get(url)
    info_parsed = parse_info_kolop(res)
    info_parsed['error'] = False
    
    up = urlparse(url)
    req_url = f"{up.scheme}://{up.netloc}/ajax.php?ajax=download"
    
    file_id = url.split('/')[-1]
    data = { 'id': file_id }
    headers = { 'x-requested-with': 'XMLHttpRequest'}
    
    try:
        res = client.post(req_url, headers=headers, data=data).json()['file']
    except:
        return {'error': True, 'src_url': url}
    
    gd_id = re.findall('gd=(.*)', res, re.DOTALL)[0]
    info_parsed['gdrive_url'] = f"https://drive.google.com/open?id={gd_id}"
    info_parsed['src_url'] = url

    return info_parsed['gdrive_url']


##################################################
# mediafire

def mediafire(url):

    res = requests.get(url, stream=True)
    contents = res.text

    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]


####################################################
# zippyshare

def zippyshare(url):
    resp = requests.get(url).text
    surl = resp.split("document.getElementById('dlbutton').href = ")[1].split(";")[0]
    parts = surl.split("(")[1].split(")")[0].split(" ")
    val = str(int(parts[0]) % int(parts[2]) + int(parts[4]) % int(parts[6]))
    surl = surl.split('"')
    burl = url.split("zippyshare.com")[0]
    furl = burl + "zippyshare.com" + surl[1] + val + surl[-2]
    return furl


####################################################
# filercrypt

def getlinks(dlc,client):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'application/json, text/javascript, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'http://dcrypt.it',
    'Connection': 'keep-alive',
    'Referer': 'http://dcrypt.it/',
    }

    data = {
        'content': dlc,
    }

    response = client.post('http://dcrypt.it/decrypt/paste', headers=headers, data=data).json()["success"]["links"]
    links = ""
    for link in response:
        links = links + link + "\n"
    return links[:-1]


def filecrypt(url):

    client = cloudscraper.create_scraper(allow_brotli=False)
    headers = {
    "authority": "filecrypt.co",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "dnt": "1",
    "origin": "https://filecrypt.co",
    "referer": url,
    "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36" 
    }
    

    resp = client.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, "html.parser")

    buttons = soup.find_all("button")
    for ele in buttons:
        line = ele.get("onclick")
        if line !=None and "DownloadDLC" in line:
            dlclink = "https://filecrypt.co/DLC/" + line.split("DownloadDLC('")[1].split("'")[0] + ".html"
            break

    resp = client.get(dlclink,headers=headers)
    return getlinks(resp.text,client)


#####################################################
# dropbox

def dropbox(url):
    return url.replace("www.","").replace("dropbox.com","dl.dropboxusercontent.com").replace("?dl=0","")


######################################################
# shareus

def shareus(url):
    token = url.split("=")[-1]
    bypassed_url = "https://us-central1-my-apps-server.cloudfunctions.net/r?shortid="+ token
    response = requests.get(bypassed_url).text
    return response


#######################################################
# shortingly

def shortlingly(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'shortingly.me' in url:
        DOMAIN = "https://go.techyjeeshan.xyz"
    else:
        return "Incorrect Link"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    
    final_url = f"{DOMAIN}/{code}"

    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(5)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("


#######################################################
# Gyanilinks - gtlinks.me

def gyanilinks(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    if 'gtlinks.me' in url:
        DOMAIN = "https://go.bloggertheme.xyz"
    else:
        return "Incorrect Link"

    url = url[:-1] if url[-1] == '/' else url

    code = url.split("/")[-1]
    
    final_url = f"{DOMAIN}/{code}"

    resp = client.get(final_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    
    try: inputs = soup.find(id="go-link").find_all(name="input")
    except: return "Incorrect Link"
    
    data = { input.get('name'): input.get('value') for input in inputs }

    h = { "x-requested-with": "XMLHttpRequest" }
    
    time.sleep(5)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return r.json()['url']
    except: return "Something went wrong :("


#######################################################
# anonfiles

def anonfile(url):

    headersList = { "Accept": "*/*"}
    payload = ""

    response = requests.request("GET", url, data=payload,  headers=headersList).text.split("\n")
    for ele in response:
        if "https://cdn" in ele and "anonfiles.com" in ele and url.split("/")[-2] in ele:
            break

    return ele.split('href="')[1].split('"')[0]


##########################################################
# pixl

def pixl(url):
    count = 1
    dl_msg = ""
    currentpage = 1
    settotalimgs = True
    totalimages = ""
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    soup = BeautifulSoup(resp.content, "html.parser")
    if "album" in url and settotalimgs:
        totalimages = soup.find("span", {"data-text": "image-count"}).text
        settotalimgs = False
    thmbnailanch = soup.findAll(attrs={"class": "--media"})
    links = soup.findAll(attrs={"data-pagination": "next"})
    try:
        url = links[0].attrs["href"]
    except BaseException:
        url = None
    for ref in thmbnailanch:
        imgdata = client.get(ref.attrs["href"])
        if not imgdata.status_code == 200:
            time.sleep(5)
            continue
        imghtml = BeautifulSoup(imgdata.text, "html.parser")
        downloadanch = imghtml.find(attrs={"class": "btn-download"})
        currentimg = downloadanch.attrs["href"]
        currentimg = currentimg.replace(" ", "%20")
        dl_msg += f"{count}. {currentimg}\n"
        count += 1
    currentpage += 1
    fld_msg = f"Your provided Pixl.is link is of Folder and I've Found {count - 1} files in the folder.\n"
    fld_link = f"\nFolder Link: {url}\n"
    final_msg = fld_link + "\n" + fld_msg + "\n" + dl_msg
    return final_msg


############################################################
# sirigan  ( unused )

def siriganbypass(url):
    client = requests.Session()
    res = client.get(url)
    url = res.url.split('=', maxsplit=1)[-1]

    while True:
        try: url = base64.b64decode(url).decode('utf-8')
        except: break

    return url.split('url=')[-1]


############################################################
# shorte

def sh_st_bypass(url):    
    client = requests.Session()
    client.headers.update({'referer': url})
    p = urlparse(url)
    
    res = client.get(url)

    sess_id = re.findall('''sessionId(?:\s+)?:(?:\s+)?['|"](.*?)['|"]''', res.text)[0]
    
    final_url = f"{p.scheme}://{p.netloc}/shortest-url/end-adsession"
    params = {
        'adSessionId': sess_id,
        'callback': '_'
    }
    time.sleep(5) # !important
    
    res = client.get(final_url, params=params)
    dest_url = re.findall('"(.*?)"', res.text)[1].replace('\/','/')
    
    return {
        'src': url,
        'dst': dest_url
    }['dst']


#############################################################
# gofile

def gofile_dl(url,password=""):
    api_uri = 'https://api.gofile.io'
    client = requests.Session()
    res = client.get(api_uri+'/createAccount').json()
    
    data = {
        'contentId': url.split('/')[-1],
        'token': res['data']['token'],
        'websiteToken': '12345',
        'cache': 'true',
        'password': hashlib.sha256(password.encode('utf-8')).hexdigest()
    }
    res = client.get(api_uri+'/getContent', params=data).json()

    content = []
    for item in res['data']['contents'].values():
        content.append(item)
    
    return {
        'accountToken': data['token'],
        'files': content
    }["files"][0]["link"]


################################################################
# sharer pw

def parse_info_sharer(res):
    f = re.findall(">(.*?)<\/td>", res.text)
    info_parsed = {}
    for i in range(0, len(f), 3):
        info_parsed[f[i].lower().replace(' ', '_')] = f[i+2]
    return info_parsed

def sharer_pw(url,Laravel_Session, XSRF_TOKEN, forced_login=False):
    client = cloudscraper.create_scraper(allow_brotli=False)
    client.cookies.update({
        "XSRF-TOKEN": XSRF_TOKEN,
        "laravel_session": Laravel_Session
    })
    res = client.get(url)
    token = re.findall("_token\s=\s'(.*?)'", res.text, re.DOTALL)[0]
    ddl_btn = etree.HTML(res.content).xpath("//button[@id='btndirect']")
    info_parsed = parse_info_sharer(res)
    info_parsed['error'] = True
    info_parsed['src_url'] = url
    info_parsed['link_type'] = 'login'
    info_parsed['forced_login'] = forced_login
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest'
    }
    data = {
        '_token': token
    }
    if len(ddl_btn):
        info_parsed['link_type'] = 'direct'
    if not forced_login:
        data['nl'] = 1
    try: 
        res = client.post(url+'/dl', headers=headers, data=data).json()
    except:
        return info_parsed
    if 'url' in res and res['url']:
        info_parsed['error'] = False
        info_parsed['gdrive_link'] = res['url']
    if len(ddl_btn) and not forced_login and not 'url' in info_parsed:
        # retry download via login
        return sharer_pw(url,Laravel_Session, XSRF_TOKEN, forced_login=True)
    return info_parsed["gdrive_link"]


#################################################################
# gdtot

def gdtot(url: str, GDTot_Crypt: str) -> str:
    client = requests.Session()
    client.cookies.update({"crypt": GDTot_Crypt})
    res = client.get(url)
    base_url = re.match('^.+?[^\/:](?=[?\/]|$\n)', url).group(0)
    res = client.get(f"{base_url}/dld?id={url.split('/')[-1]}")
    url = re.findall(r'URL=(.*?)"', res.text)[0]
    info = {}
    info["error"] = False
    params = parse_qs(urlparse(url).query)
    if "gd" not in params or not params["gd"] or params["gd"][0] == "false":
        info["error"] = True
        if "msgx" in params:
            info["message"] = params["msgx"][0]
        else:
            info["message"] = "Invalid link"
    else:
        decoded_id = base64.b64decode(str(params["gd"][0])).decode("utf-8")
        drive_link = f"https://drive.google.com/open?id={decoded_id}"
        info["gdrive_link"] = drive_link
    if not info["error"]:
        return info["gdrive_link"]
    else:
        return f"{info['message']}"


##################################################################
# adfly

def decrypt_url(code):
    a, b = '', ''
    for i in range(0, len(code)):
        if i % 2 == 0: a += code[i]
        else: b = code[i] + b
    key = list(a + b)
    i = 0
    while i < len(key):
        if key[i].isdigit():
            for j in range(i+1,len(key)):
                if key[j].isdigit():
                    u = int(key[i]) ^ int(key[j])
                    if u < 10: key[i] = str(u)
                    i = j					
                    break
        i+=1
    key = ''.join(key)
    decrypted = base64.b64decode(key)[16:-16]
    return decrypted.decode('utf-8')


def adfly(url):
    client = cloudscraper.create_scraper(allow_brotli=False)
    res = client.get(url).text
    out = {'error': False, 'src_url': url}
    try:
        ysmm = re.findall("ysmm\s+=\s+['|\"](.*?)['|\"]", res)[0]
    except:
        out['error'] = True
        return out
    url = decrypt_url(ysmm)
    if re.search(r'go\.php\?u\=', url):
        url = base64.b64decode(re.sub(r'(.*?)u=', '', url)).decode()
    elif '&dest=' in url:
        url = unquote(re.sub(r'(.*?)dest=', '', url))
    out['bypassed_url'] = url
    return out


##############################################################################################        
# gplinks

def gplinks(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f"{p.scheme}://{p.netloc}/links/go"
    res = client.head(url)
    header_loc = res.headers["location"]
    p = urlparse(header_loc)
    ref_url = f"{p.scheme}://{p.netloc}/"
    h = {"referer": ref_url}
    res = client.get(url, headers=h, allow_redirects=False)
    bs4 = BeautifulSoup(res.content, "html.parser")
    inputs = bs4.find_all("input")
    time.sleep(10) # !important
    data = { input.get("name"): input.get("value") for input in inputs }
    h = {
        "content-type": "application/x-www-form-urlencoded",
        "x-requested-with": "XMLHttpRequest"
    }
    time.sleep(10)
    res = client.post(final_url, headers=h, data=data)
    try:
        return res.json()["url"].replace("/","/")
    except: 
        return "Could not Bypass your URL :("


######################################################################################################
# droplink

def droplink(url):
    api = "https://api.emilyx.in/api"
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    try:
        resp = client.post(api, json={"type": "droplink", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link !"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


#####################################################################################################################
# link vertise

def linkvertise(url):
    api = "https://api.emilyx.in/api"
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    try:
        resp = client.post(api, json={"type": "linkvertise", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link !"
    if res["success"] is True:
        return res["url"]
    else:
        try:
            payload = {"url": url}
            url_bypass = requests.post("https://api.bypass.vip/", data=payload).json()
            bypassed = url_bypass["destination"]
            return bypassed
        except:
            return "Could not Bypass your URL :("


###################################################################################################################
# others

# api from https://github.com/bypass-vip/bypass.vip
def others(url):
    try:
        payload = {"url": url}
        url_bypass = requests.post("https://api.bypass.vip/", data=payload).json()
        bypassed = url_bypass["destination"]
        return bypassed
    except:
        return "Could not Bypass your URL :("


#################################################################################################################
# ouo

# RECAPTCHA v3 BYPASS
# code from https://github.com/xcscxr/Recaptcha-v3-bypass
def RecaptchaV3(ANCHOR_URL="https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr"):
    url_base = 'https://www.google.com/recaptcha/'
    post_data = "v={}&reason=q&c={}&k={}&co={}"
    client = requests.Session()
    client.headers.update({
        'content-type': 'application/x-www-form-urlencoded'
    })
    matches = re.findall('([api2|enterprise]+)\/anchor\?(.*)', ANCHOR_URL)[0]
    url_base += matches[0]+'/'
    params = matches[1]
    res = client.get(url_base+'anchor', params=params)
    token = re.findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]
    params = dict(pair.split('=') for pair in params.split('&'))
    post_data = post_data.format(params["v"], token, params["k"], params["co"])
    res = client.post(url_base+'reload', params=f'k={params["k"]}', data=post_data)
    answer = re.findall(r'"rresp","(.*?)"', res.text)[0]    
    return answer


# code from https://github.com/xcscxr/ouo-bypass/
def ouo(url):
    client = requests.Session()
    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    
    res = client.get(tempurl)
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):
        if res.headers.get('Location'):
            break
        bs4 = BeautifulSoup(res.content, 'lxml')
        inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
        data = { input.get('name'): input.get('value') for input in inputs }
        
        ans = RecaptchaV3()
        data['x-token'] = ans
        h = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        res = client.post(next_url, data=data, headers=h, allow_redirects=False)
        next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"

    return res.headers.get('Location')


####################################################################################################################        
# mdisk

def mdisk(url):
    api = "https://api.emilyx.in/api"
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    try:
        resp = client.post(api, json={"type": "mdisk", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link !"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


###################################################################################################################
# pixeldrain

def pixeldrain(url):
    api = "https://api.emilyx.in/api"
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    try:
        resp = client.post(api, json={"type": "pixeldrain", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link !"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


####################################################################################################################
# we transfer

def wetransfer(url):
    api = "https://api.emilyx.in/api"
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    try:
        resp = client.post(api, json={"type": "wetransfer", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link !"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


##################################################################################################################
# megaup

def megaup(url):
    api = "https://api.emilyx.in/api"
    client = cloudscraper.create_scraper(allow_brotli=False)
    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    try:
        resp = client.post(api, json={"type": "megaup", "url": url})
        res = resp.json()
    except BaseException:
        return "API UnResponsive / Invalid Link !"
    if res["success"] is True:
        return res["url"]
    else:
        return res["msg"]


##################################################################################################################        
# AppDrive or DriveApp etc. Look-Alike Link and as well as the Account Details (Required for Login Required Links only)

def unified(url):

    try:

        Email = "OPTIONAL"
        Password = "OPTIONAL"

        account = {"email": Email, "passwd": Password}
        client = cloudscraper.create_scraper(allow_brotli=False)
        client.headers.update(
            {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
            }
        )
        data = {"email": account["email"], "password": account["passwd"]}
        client.post(f"https://{urlparse(url).netloc}/login", data=data)
        res = client.get(url)
        key = re.findall('"key",\s+"(.*?)"', res.text)[0]
        ddl_btn = etree.HTML(res.content).xpath("//button[@id='drc']")
        info = re.findall(">(.*?)<\/li>", res.text)
        info_parsed = {}
        for item in info:
            kv = [s.strip() for s in item.split(":", maxsplit=1)]
            info_parsed[kv[0].lower()] = kv[1]
        info_parsed = info_parsed
        info_parsed["error"] = False
        info_parsed["link_type"] = "login"
        headers = {
            "Content-Type": f"multipart/form-data; boundary={'-'*4}_",
        }
        data = {"type": 1, "key": key, "action": "original"}
        if len(ddl_btn):
            info_parsed["link_type"] = "direct"
            data["action"] = "direct"
        while data["type"] <= 3:
            boundary = f'{"-"*6}_'
            data_string = ""
            for item in data:
                data_string += f"{boundary}\r\n"
                data_string += f'Content-Disposition: form-data; name="{item}"\r\n\r\n{data[item]}\r\n'
            data_string += f"{boundary}--\r\n"
            gen_payload = data_string
            try:
                response = client.post(url, data=gen_payload, headers=headers).json()
                break
            except BaseException:
                data["type"] += 1
        if "url" in response:
            info_parsed["gdrive_link"] = response["url"]
        elif "error" in response and response["error"]:
            info_parsed["error"] = True
            info_parsed["error_message"] = response["message"]
        else:
            info_parsed["error"] = True
            info_parsed["error_message"] = "Something went wrong :("
        if info_parsed["error"]:
            return info_parsed
        if urlparse(url).netloc == "driveapp.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        info_parsed["src_url"] = url
        if urlparse(url).netloc == "drivehub.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if urlparse(url).netloc == "gdflix.pro" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link

        if urlparse(url).netloc == "drivesharer.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if urlparse(url).netloc == "drivebit.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if urlparse(url).netloc == "drivelinks.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if urlparse(url).netloc == "driveace.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if urlparse(url).netloc == "drivepro.in" and not info_parsed["error"]:
            res = client.get(info_parsed["gdrive_link"])
            drive_link = etree.HTML(res.content).xpath(
                "//a[contains(@class,'btn')]/@href"
            )[0]
            info_parsed["gdrive_link"] = drive_link
        if info_parsed["error"]:
            return "Faced an Unknown Error!"
        return info_parsed["gdrive_link"]
    except BaseException:
        return "Unable to Extract GDrive Link"


#####################################################################################################        
