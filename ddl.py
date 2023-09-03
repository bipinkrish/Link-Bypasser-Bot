from base64 import standard_b64encode
from json import loads
from math import floor, pow
from re import findall, match, search, sub
from time import sleep
from urllib.parse import quote, unquote, urlparse
from uuid import uuid4

from bs4 import BeautifulSoup
from cfscrape import create_scraper
from lxml import etree
from requests import get, session

from json import load
from os import environ

with open('config.json', 'r') as f: DATA = load(f)
def getenv(var): return environ.get(var) or DATA.get(var, None)


UPTOBOX_TOKEN = getenv("UPTOBOX_TOKEN")
ndus = getenv("TERA_COOKIE")
if ndus is None: TERA_COOKIE = None
else: TERA_COOKIE = {"ndus": ndus}


ddllist = ['1drv.ms','1fichier.com','4funbox','akmfiles','anonfiles.com','antfiles.com','bayfiles.com','disk.yandex.com',
		   'fcdn.stream','femax20.com','fembed.com','fembed.net','feurl.com','filechan.org','filepress','github.com','hotfile.io',
		   'hxfile.co','krakenfiles.com','layarkacaxxi.icu','letsupload.cc','letsupload.io','linkbox','lolabits.se','mdisk.me',
		   'mediafire.com','megaupload.nz','mirrobox','mm9842.com','momerybox','myfile.is','naniplay.com','naniplay.nanime.biz',
		   'naniplay.nanime.in','nephobox','openload.cc','osdn.net','pixeldrain.com','racaty','rapidshare.nu','sbembed.com',
		   'sbplay.org','share-online.is','shrdsk','solidfiles.com','streamsb.net','streamtape','terabox','teraboxapp','upload.ee',
		   'uptobox.com','upvid.cc','vshare.is','watchsb.com','we.tl','wetransfer.com','yadi.sk','zippyshare.com']


def is_share_link(url):
	return bool(match(r'https?:\/\/.+\.gdtot\.\S+|https?:\/\/(filepress|filebee|appdrive|gdflix|driveseed)\.\S+', url))


def get_readable_time(seconds):
	result = ''
	(days, remainder) = divmod(seconds, 86400)
	days = int(days)
	if days != 0:
		result += f'{days}d'
	(hours, remainder) = divmod(remainder, 3600)
	hours = int(hours)
	if hours != 0:
		result += f'{hours}h'
	(minutes, seconds) = divmod(remainder, 60)
	minutes = int(minutes)
	if minutes != 0:
		result += f'{minutes}m'
	seconds = int(seconds)
	result += f'{seconds}s'
	return result


fmed_list = ['fembed.net', 'fembed.com', 'femax20.com', 'fcdn.stream', 'feurl.com', 'layarkacaxxi.icu',
			 'naniplay.nanime.in', 'naniplay.nanime.biz', 'naniplay.com', 'mm9842.com']

anonfilesBaseSites = ['anonfiles.com', 'hotfile.io', 'bayfiles.com', 'megaupload.nz', 'letsupload.cc',
					  'filechan.org', 'myfile.is', 'vshare.is', 'rapidshare.nu', 'lolabits.se',
					  'openload.cc', 'share-online.is', 'upvid.cc']


def direct_link_generator(link: str):
	""" direct links generator """
	domain = urlparse(link).hostname
	if 'yadi.sk' in domain or 'disk.yandex.com' in domain:
		return yandex_disk(link)
	elif 'mediafire.com' in domain:
		return mediafire(link)
	elif 'uptobox.com' in domain:
		return uptobox(link)
	elif 'osdn.net' in domain:
		return osdn(link)
	elif 'github.com' in domain:
		return github(link)
	elif 'hxfile.co' in domain:
		return hxfile(link)
	elif '1drv.ms' in domain:
		return onedrive(link)
	elif 'pixeldrain.com' in domain:
		return pixeldrain(link)
	elif 'antfiles.com' in domain:
		return antfiles(link)
	elif 'streamtape' in domain:
		return streamtape(link)
	elif 'racaty' in domain:
		return racaty(link)
	elif '1fichier.com' in domain:
		return fichier(link)
	elif 'solidfiles.com' in domain:
		return solidfiles(link)
	elif 'krakenfiles.com' in domain:
		return krakenfiles(link)
	elif 'upload.ee' in domain:
		return uploadee(link)
	elif 'akmfiles' in domain:
		return akmfiles(link)
	elif 'linkbox' in domain:
		return linkbox(link)
	elif 'shrdsk' in domain:
		return shrdsk(link)
	elif 'letsupload.io' in domain:
		return letsupload(link)
	elif 'zippyshare.com' in domain:
		return zippyshare(link)
	elif 'mdisk.me' in domain:
		return mdisk(link)
	elif any(x in domain for x in ['wetransfer.com', 'we.tl']):
		return wetransfer(link)
	elif any(x in domain for x in anonfilesBaseSites):
		return anonfilesBased(link)
	elif any(x in domain for x in ['terabox', 'nephobox', '4funbox', 'mirrobox', 'momerybox', 'teraboxapp']):
		return terabox(link)
	elif any(x in domain for x in fmed_list):
		return fembed(link)
	elif any(x in domain for x in ['sbembed.com', 'watchsb.com', 'streamsb.net', 'sbplay.org']):
		return sbembed(link)
	elif is_share_link(link):
		if 'gdtot' in domain:
			return gdtot(link)
		elif 'filepress' in domain:
			return filepress(link)
		else:
			return sharer_scraper(link)
	else:
		return f'No Direct link function found for\n\n{link}\n\nuse /ddllist'


def mdisk(url):
	header = {
		'Accept': '*/*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate, br',
		'Referer': 'https://mdisk.me/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
	}
	id = url.split("/")[-1]
	URL = f'https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={id}'
	return get(url=URL, headers=header).json()['source']


def yandex_disk(url: str) -> str:
	""" Yandex.Disk direct link generator
	Based on https://github.com/wldhx/yadisk-direct """
	try:
		link = findall(r'\b(https?://(yadi.sk|disk.yandex.com)\S+)', url)[0][0]
	except IndexError:
		return "No Yandex.Disk links found\n"
	api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
	cget = create_scraper().request
	try:
		return cget('get', api.format(link)).json()['href']
	except KeyError:
		return (
			"ERROR: File not found/Download limit reached")


def uptobox(url: str) -> str:
	""" Uptobox direct link generator
	based on https://github.com/jovanzers/WinTenCermin and https://github.com/sinoobie/noobie-mirror """
	try:
		link = findall(r'\bhttps?://.*uptobox\.com\S+', url)[0]
	except IndexError:
		return ("No Uptobox links found")
	link = findall(r'\bhttps?://.*\.uptobox\.com/dl\S+', url)
	if link: return link[0]
	cget = create_scraper().request
	try:
		file_id = findall(r'\bhttps?://.*uptobox\.com/(\w+)', url)[0]
		if UPTOBOX_TOKEN:
			file_link = f'https://uptobox.com/api/link?token={UPTOBOX_TOKEN}&file_code={file_id}'
		else:
			file_link = f'https://uptobox.com/api/link?file_code={file_id}'
		res = cget('get', file_link).json()
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")
	if res['statusCode'] == 0:
		return res['data']['dlLink']
	elif res['statusCode'] == 16:
		sleep(1)
		waiting_token = res["data"]["waitingToken"]
		sleep(res["data"]["waiting"])
	elif res['statusCode'] == 39:
		return (
			f"ERROR: Uptobox is being limited please wait {get_readable_time(res['data']['waiting'])}")
	else:
		return (f"ERROR: {res['message']}")
	try:
		res = cget('get', f"{file_link}&waitingToken={waiting_token}").json()
		return res['data']['dlLink']
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")


def mediafire(url: str) -> str:
	final_link = findall(r'https?:\/\/download\d+\.mediafire\.com\/\S+\/\S+\/\S+', url)
	if final_link: return final_link[0]
	cget = create_scraper().request
	try:
		url = cget('get', url).url
		page = cget('get', url).text
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")
	final_link = findall(r"\'(https?:\/\/download\d+\.mediafire\.com\/\S+\/\S+\/\S+)\'", page)
	if not final_link:return ("ERROR: No links found in this page")
	return final_link[0]


def osdn(url: str) -> str:
	""" OSDN direct link generator """
	osdn_link = 'https://osdn.net'
	try:
		link = findall(r'\bhttps?://.*osdn\.net\S+', url)[0]
	except IndexError:
		return ("No OSDN links found")
	cget = create_scraper().request
	try:
		page = BeautifulSoup(
			cget('get', link, allow_redirects=True).content, 'lxml')
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")
	info = page.find('a', {'class': 'mirror_link'})
	link = unquote(osdn_link + info['href'])
	mirrors = page.find('form', {'id': 'mirror-select-form'}).findAll('tr')
	urls = []
	for data in mirrors[1:]:
		mirror = data.find('input')['value']
		urls.append(sub(r'm=(.*)&f', f'm={mirror}&f', link))
	return urls[0]


def github(url: str) -> str:
	""" GitHub direct links generator """
	try:
		findall(r'\bhttps?://.*github\.com.*releases\S+', url)[0]
	except IndexError:
		return ("No GitHub Releases links found")
	cget = create_scraper().request
	download = cget('get', url, stream=True, allow_redirects=False)
	try:
		return download.headers["location"]
	except KeyError:
		return ("ERROR: Can't extract the link")


def hxfile(url: str) -> str:
	sess = session()
	try:
		headers = {
			'content-type': 'application/x-www-form-urlencoded',
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36',
		}

		data = {
			'op': 'download2',
			'id': urlparse(url).path.strip("/")(url),
			'rand': '',
			'referer': '',
			'method_free': '',
			'method_premium': '',
		}

		response = sess.post(url, headers=headers, data=data)
		soup = BeautifulSoup(response,"html.parser")

		if (btn := soup.find(class_="btn btn-dow")):
			return btn["href"]
		if (unique := soup.find(id="uniqueExpirylink")):
			return unique["href"]
		
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")


def letsupload(url: str) -> str:
	cget = create_scraper().request
	try:
		res = cget("POST", url)
	except Exception as e:
		return (f'ERROR: {e.__class__.__name__}')
	direct_link = findall(r"(https?://letsupload\.io\/.+?)\'", res.text)
	if direct_link: return direct_link[0]
	else:
		return ('ERROR: Direct Link not found')


def anonfilesBased(url: str) -> str:
	cget = create_scraper().request
	try:
		soup = BeautifulSoup(cget('get', url).content, 'lxml')
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")
	sa = soup.find(id="download-url")
	if sa: return sa['href']
	return ("ERROR: File not found!")


def fembed(link: str) -> str:
	sess = session()
	try:
		url = url.replace("/v/", "/f/")
		raw = session.get(url)
		api = search(r"(/api/source/[^\"']+)", raw.text)
		if api is not None:
			result = {}
			raw = sess.post(
				"https://layarkacaxxi.icu" + api.group(1)).json()
			for d in raw["data"]:
				f = d["file"]
				head = sess.head(f)
				direct = head.headers.get("Location", url)
				result[f"{d['label']}/{d['type']}"] = direct
			dl_url = result

		count = len(dl_url)
		lst_link = [dl_url[i] for i in dl_url]
		return lst_link[count-1]
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")


def sbembed(link: str) -> str:
	sess = session()
	try: 
		raw = sess.get(link)
		soup = BeautifulSoup(raw,"html.parser")

		result = {}
		for a in soup.findAll("a", onclick=compile(r"^download_video[^>]+")):
			data = dict(zip(["id", "mode", "hash"], findall(
				r"[\"']([^\"']+)[\"']", a["onclick"])))
			data["op"] = "download_orig"

			raw = sess.get("https://sbembed.com/dl", params=data)
			soup = BeautifulSoup(raw,"html.parser")

			if (direct := soup.find("a", text=compile("(?i)^direct"))):
				result[a.text] = direct["href"]
		dl_url = result

		count = len(dl_url)
		lst_link = [dl_url[i] for i in dl_url]
		return lst_link[count-1]
	
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")


def onedrive(link: str) -> str:
	""" Onedrive direct link generator
	Based on https://github.com/UsergeTeam/Userge """
	link_without_query = urlparse(link)._replace(query=None).geturl()
	direct_link_encoded = str(standard_b64encode(
		bytes(link_without_query, "utf-8")), "utf-8")
	direct_link1 = f"https://api.onedrive.com/v1.0/shares/u!{direct_link_encoded}/root/content"
	cget = create_scraper().request
	try:
		resp = cget('head', direct_link1)
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")
	if resp.status_code != 302:
		return (
			"ERROR: Unauthorized link, the link may be private")
	return resp.next.url


def pixeldrain(url: str) -> str:
	""" Based on https://github.com/yash-dk/TorToolkit-Telegram """
	url = url.strip("/ ")
	file_id = url.split("/")[-1]
	if url.split("/")[-2] == "l":
		info_link = f"https://pixeldrain.com/api/list/{file_id}"
		dl_link = f"https://pixeldrain.com/api/list/{file_id}/zip?download"
	else:
		info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
		dl_link = f"https://pixeldrain.com/api/file/{file_id}?download"
	cget = create_scraper().request
	try:
		resp = cget('get', info_link).json()
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")
	if resp["success"]:
		return dl_link
	else:
		return (
			f"ERROR: Cant't download due {resp['message']}.")


def antfiles(url: str) -> str:
	sess = session()
	try:
		raw = sess.get(url)
		soup = BeautifulSoup(raw,"html.parser")

		if (a := soup.find(class_="main-btn", href=True)):
			return "{0.scheme}://{0.netloc}/{1}".format(urlparse(url), a["href"])

	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")


def streamtape(url: str) -> str:
	response = get(url)

	if (videolink := findall(r"document.*((?=id\=)[^\"']+)", response.text)):
		nexturl = "https://streamtape.com/get_video?" + videolink[-1]
		try: return nexturl
		except Exception as e: return (f"ERROR: {e.__class__.__name__}")


def racaty(url: str) -> str:
	""" Racaty direct link generator
	By https://github.com/junedkh """
	cget = create_scraper().request
	try:
		url = cget('GET', url).url
		json_data = {
			'op': 'download2',
			'id': url.split('/')[-1]
		}
		res = cget('POST', url, data=json_data)
	except Exception as e:
		return (f'ERROR: {e.__class__.__name__}')
	html_tree = etree.HTML(res.text)
	direct_link = html_tree.xpath("//a[contains(@id,'uniqueExpirylink')]/@href")
	if direct_link:
		return direct_link[0]
	else:
		return ('ERROR: Direct link not found')


def fichier(link: str) -> str:
	""" 1Fichier direct link generator
	Based on https://github.com/Maujar
	"""
	regex = r"^([http:\/\/|https:\/\/]+)?.*1fichier\.com\/\?.+"
	gan = match(regex, link)
	if not gan:
		return (
			"ERROR: The link you entered is wrong!")
	if "::" in link:
		pswd = link.split("::")[-1]
		url = link.split("::")[-2]
	else:
		pswd = None
		url = link
	cget = create_scraper().request
	try:
		if pswd is None:
			req = cget('post', url)
		else:
			pw = {"pass": pswd}
			req = cget('post', url, data=pw)
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")
	if req.status_code == 404:
		return (
			"ERROR: File not found/The link you entered is wrong!")
	soup = BeautifulSoup(req.content, 'lxml')
	if soup.find("a", {"class": "ok btn-general btn-orange"}):
		dl_url = soup.find("a", {"class": "ok btn-general btn-orange"})["href"]
		if dl_url: return dl_url
		return (
			"ERROR: Unable to generate Direct Link 1fichier!")
	elif len(soup.find_all("div", {"class": "ct_warn"})) == 3:
		str_2 = soup.find_all("div", {"class": "ct_warn"})[-1]
		if "you must wait" in str(str_2).lower():
			numbers = [int(word) for word in str(str_2).split() if word.isdigit()]
			if numbers:  return (
					f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute.")
			else:
				return (
					"ERROR: 1fichier is on a limit. Please wait a few minutes/hour.")
		elif "protect access" in str(str_2).lower():
			return (
				"ERROR: This link requires a password!\n\n<b>This link requires a password!</b>\n- Insert sign <b>::</b> after the link and write the password after the sign.\n\n<b>Example:</b> https://1fichier.com/?smmtd8twfpm66awbqz04::love you\n\n* No spaces between the signs <b>::</b>\n* For the password, you can use a space!")
		else:
			return (
				"ERROR: Failed to generate Direct Link from 1fichier!")
	elif len(soup.find_all("div", {"class": "ct_warn"})) == 4:
		str_1 = soup.find_all("div", {"class": "ct_warn"})[-2]
		str_3 = soup.find_all("div", {"class": "ct_warn"})[-1]
		if "you must wait" in str(str_1).lower():
			numbers = [int(word) for word in str(str_1).split() if word.isdigit()]
			if numbers: return (
					f"ERROR: 1fichier is on a limit. Please wait {numbers[0]} minute.")
			else:
				return (
					"ERROR: 1fichier is on a limit. Please wait a few minutes/hour.")
		elif "bad password" in str(str_3).lower():
			return (
				"ERROR: The password you entered is wrong!")
		else:
			return (
				"ERROR: Error trying to generate Direct Link from 1fichier!")
	else:
		return (
			"ERROR: Error trying to generate Direct Link from 1fichier!")


def solidfiles(url: str) -> str:
	""" Solidfiles direct link generator
	Based on https://github.com/Xonshiz/SolidFiles-Downloader
	By https://github.com/Jusidama18 """
	cget = create_scraper().request
	try:
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
		}
		pageSource = cget('get', url, headers=headers).text
		mainOptions = str(
			search(r'viewerOptions\'\,\ (.*?)\)\;', pageSource).group(1))
		return loads(mainOptions)["downloadUrl"]
	except Exception as e:
		return (f"ERROR: {e.__class__.__name__}")


def krakenfiles(url: str) -> str:
	sess = session()
	try:
		res = sess.get(url)
		html = etree.HTML(res.text)
		if post_url:= html.xpath('//form[@id="dl-form"]/@action'):
			post_url = f'https:{post_url[0]}'
		else:
			sess.close()
			return ('ERROR: Unable to find post link.')
		if token:= html.xpath('//input[@id="dl-token"]/@value'):
			data = {'token': token[0]}
		else:
			sess.close()
			return ('ERROR: Unable to find token for post.')
	except Exception as e:
		sess.close()
		return (f'ERROR: {e.__class__.__name__} Something went wrong')
	try:
		dl_link = sess.post(post_url, data=data).json()
		return dl_link['url']
	except Exception as e:
		sess.close()
		return (f'ERROR: {e.__class__.__name__} While send post request')


def uploadee(url: str) -> str:
	""" uploadee direct link generator
	By https://github.com/iron-heart-x"""
	cget = create_scraper().request
	try:
		soup = BeautifulSoup(cget('get', url).content, 'lxml')
		sa = soup.find('a', attrs={'id': 'd_l'})
		return sa['href']
	except:
		return (
			f"ERROR: Failed to acquire download URL from upload.ee for : {url}")


def terabox(url) -> str:
	sess = session()
	while True:
		try: 
			res = sess.get(url)
			print("connected")
			break
		except: print("retrying")
	url = res.url

	key = url.split('?surl=')[-1]
	url = f'http://www.terabox.com/wap/share/filelist?surl={key}'
	sess.cookies.update(TERA_COOKIE)

	while True:
		try: 
			res = sess.get(url)
			print("connected")
			break
		except Exception as e: print("retrying")

	key = res.url.split('?surl=')[-1]
	soup = BeautifulSoup(res.content, 'lxml')
	jsToken = None

	for fs in soup.find_all('script'):
		fstring = fs.string
		if fstring and fstring.startswith('try {eval(decodeURIComponent'):
			jsToken = fstring.split('%22')[1]

	while True:
		try:
			res = sess.get(f'https://www.terabox.com/share/list?app_id=250528&jsToken={jsToken}&shorturl={key}&root=1')
			print("connected")
			break
		except: print("retrying")
	result = res.json()

	if result['errno'] != 0: return f"ERROR: '{result['errmsg']}' Check cookies"
	result = result['list']
	if len(result) > 1: return "ERROR: Can't download mutiple files"
	result = result[0]

	if result['isdir'] != '0':return "ERROR: Can't download folder"
	return result.get('dlink',"Error")


def filepress(url):
	cget = create_scraper().request
	try:
		url = cget('GET', url).url
		raw = urlparse(url)

		gd_data = {
			'id': raw.path.split('/')[-1],
			'method': 'publicDownlaod',
		}
		tg_data = {
			'id': raw.path.split('/')[-1],
			'method': 'telegramDownload',
		}
		
		api = f'{raw.scheme}://{raw.hostname}/api/file/downlaod/'
		
		gd_res = cget('POST', api, headers={'Referer': f'{raw.scheme}://{raw.hostname}'}, json=gd_data).json()
		tg_res = cget('POST', api, headers={'Referer': f'{raw.scheme}://{raw.hostname}'}, json=tg_data).json()
		
	except Exception as e:
		return f'Google Drive: ERROR: {e.__class__.__name__} \nTelegram: ERROR: {e.__class__.__name__}'
	
	gd_result = f'https://drive.google.com/uc?id={gd_res["data"]}' if 'data' in gd_res else f'ERROR: {gd_res["statusText"]}'
	tg_result = f'https://tghub.xyz/?start={tg_res["data"]}' if 'data' in tg_res else "No Telegram file available "
	
	return f'Google Drive: {gd_result} \nTelegram: {tg_result}'
		   

def gdtot(url):
	cget = create_scraper().request
	try:
		res = cget('GET', f'https://gdbot.xyz/file/{url.split("/")[-1]}')
	except Exception as e:
		return (f'ERROR: {e.__class__.__name__}')
	token_url = etree.HTML(res.content).xpath(
		"//a[contains(@class,'inline-flex items-center justify-center')]/@href")
	if not token_url:
		try:
			url = cget('GET', url).url
			p_url = urlparse(url)
			res = cget(
				"GET", f"{p_url.scheme}://{p_url.hostname}/ddl/{url.split('/')[-1]}")
		except Exception as e:
			return (f'ERROR: {e.__class__.__name__}')
		drive_link = findall(r"myDl\('(.*?)'\)", res.text)
		if drive_link and "drive.google.com" in drive_link[0]:
			return drive_link[0]
		else:
			return (
				'ERROR: Drive Link not found, Try in your broswer')
	token_url = token_url[0]
	try:
		token_page = cget('GET', token_url)
	except Exception as e:
		return (
			f'ERROR: {e.__class__.__name__} with {token_url}')
	path = findall('\("(.*?)"\)', token_page.text)
	if not path:
		return ('ERROR: Cannot bypass this')
	path = path[0]
	raw = urlparse(token_url)
	final_url = f'{raw.scheme}://{raw.hostname}{path}'
	return sharer_scraper(final_url)


def sharer_scraper(url):
	cget = create_scraper().request
	try:
		url = cget('GET', url).url
		raw = urlparse(url)
		header = {
			"useragent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.548.0 Safari/534.10"}
		res = cget('GET', url, headers=header)
	except Exception as e:
		return (f'ERROR: {e.__class__.__name__}')
	key = findall('"key",\s+"(.*?)"', res.text)
	if not key:
		return ("ERROR: Key not found!")
	key = key[0]
	if not etree.HTML(res.content).xpath("//button[@id='drc']"):
		return (
			"ERROR: This link don't have direct download button")
	boundary = uuid4()
	headers = {
		'Content-Type': f'multipart/form-data; boundary=----WebKitFormBoundary{boundary}',
		'x-token': raw.hostname,
		'useragent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.548.0 Safari/534.10'
	}

	data = f'------WebKitFormBoundary{boundary}\r\nContent-Disposition: form-data; name="action"\r\n\r\ndirect\r\n' \
		f'------WebKitFormBoundary{boundary}\r\nContent-Disposition: form-data; name="key"\r\n\r\n{key}\r\n' \
		f'------WebKitFormBoundary{boundary}\r\nContent-Disposition: form-data; name="action_token"\r\n\r\n\r\n' \
		f'------WebKitFormBoundary{boundary}--\r\n'
	try:
		res = cget("POST", url, cookies=res.cookies,
				   headers=headers, data=data).json()
	except Exception as e:
		return (f'ERROR: {e.__class__.__name__}')
	if "url" not in res:
		return (
			'ERROR: Drive Link not found, Try in your broswer')
	if "drive.google.com" in res["url"]:
		return res["url"]
	try:
		res = cget('GET', res["url"])
	except Exception as e:
		return (f'ERROR: {e.__class__.__name__}')
	html_tree = etree.HTML(res.content)
	drive_link = html_tree.xpath("//a[contains(@class,'btn')]/@href")
	if drive_link and "drive.google.com" in drive_link[0]:
		return drive_link[0]
	else:
		return (
			'ERROR: Drive Link not found, Try in your broswer')


def wetransfer(url):
	cget = create_scraper().request
	try:
		url = cget('GET', url).url
		json_data = {
			'security_hash': url.split('/')[-1],
			'intent': 'entire_transfer'
		}
		res = cget(
			'POST', f'https://wetransfer.com/api/v4/transfers/{url.split("/")[-2]}/download', json=json_data).json()
	except Exception as e:
		return (f'ERROR: {e.__class__.__name__}')
	if "direct_link" in res:
		return res["direct_link"]
	elif "message" in res:
		return (f"ERROR: {res['message']}")
	elif "error" in res:
		return (f"ERROR: {res['error']}")
	else:
		return ("ERROR: cannot find direct link")


def akmfiles(url):
	cget = create_scraper().request
	try:
		url = cget('GET', url).url
		json_data = {
			'op': 'download2',
			'id': url.split('/')[-1]
		}
		res = cget('POST', url, data=json_data)
	except Exception as e:
		return (f'ERROR: {e.__class__.__name__}')
	html_tree = etree.HTML(res.content)
	direct_link = html_tree.xpath("//a[contains(@class,'btn btn-dow')]/@href")
	if direct_link:
		return direct_link[0]
	else:
		return ('ERROR: Direct link not found')


def shrdsk(url):
	cget = create_scraper().request
	try:
		url = cget('GET', url).url
		res = cget(
			'GET', f'https://us-central1-affiliate2apk.cloudfunctions.net/get_data?shortid={url.split("/")[-1]}')
	except Exception as e:
		return (f'ERROR: {e.__class__.__name__}')
	if res.status_code != 200:
		return (
			f'ERROR: Status Code {res.status_code}')
	res = res.json()
	if ("type" in res and res["type"].lower() == "upload" and "video_url" in res):
		return res["video_url"]
	return ("ERROR: cannot find direct link")


def linkbox(url):
	cget = create_scraper().request
	try:
		url = cget('GET', url).url
		res = cget(
			'GET', f'https://www.linkbox.to/api/file/detail?itemId={url.split("/")[-1]}').json()
	except Exception as e:
		return (f'ERROR: {e.__class__.__name__}')
	if 'data' not in res:
		return ('ERROR: Data not found!!')
	data = res['data']
	if not data:
		return ('ERROR: Data is None!!')
	if 'itemInfo' not in data:
		return ('ERROR: itemInfo not found!!')
	itemInfo = data['itemInfo']
	if 'url' not in itemInfo:
		return ('ERROR: url not found in itemInfo!!')
	if "name" not in itemInfo:
		return (
			'ERROR: Name not found in itemInfo!!')
	name = quote(itemInfo["name"])
	raw = itemInfo['url'].split("/", 3)[-1]
	return f'https://wdl.nuplink.net/{raw}&filename={name}'


def zippyshare(url):
	cget = create_scraper().request
	try:
		url = cget('GET', url).url
		resp = cget('GET', url)
	except Exception as e:
		return (f'ERROR: {e.__class__.__name__}')
	if not resp.ok:
		return (
			'ERROR: Something went wrong!!, Try in your browser')
	if findall(r'>File does not exist on this server<', resp.text):
		return (
			'ERROR: File does not exist on server!!, Try in your browser')
	pages = etree.HTML(resp.text).xpath(
		"//script[contains(text(),'dlbutton')][3]/text()")
	if not pages:
		return ('ERROR: Page not found!!')
	js_script = pages[0]
	uri1 = None
	uri2 = None
	method = ''
	omg = findall(r"\.omg.=.(.*?);", js_script)
	var_a = findall(r"var.a.=.(\d+)", js_script)
	var_ab = findall(r"var.[ab].=.(\d+)", js_script)
	unknown = findall(r"\+\((.*?).\+", js_script)
	unknown1 = findall(r"\+.\((.*?)\).\+", js_script)
	if omg:
		omg = omg[0]
		method = f'omg = {omg}'
		mtk = (eval(omg) * (int(omg.split("%")[0]) % 3)) + 18
		uri1 = findall(r'"/(d/\S+)/"', js_script)
		uri2 = findall(r'\/d.*?\+"/(\S+)";', js_script)
	elif var_a:
		var_a = var_a[0]
		method = f'var_a = {var_a}'
		mtk = int(pow(int(var_a), 3) + 3)
		uri1 = findall(r"\.href.=.\"/(.*?)/\"", js_script)
		uri2 = findall(r"\+\"/(.*?)\"", js_script)
	elif var_ab:
		a = var_ab[0]
		b = var_ab[1]
		method = f'a = {a}, b = {b}'
		mtk = eval(f"{floor(int(a)/3) + int(a) % int(b)}")
		uri1 = findall(r"\.href.=.\"/(.*?)/\"", js_script)
		uri2 = findall(r"\)\+\"/(.*?)\"", js_script)
	elif unknown:
		method = f'unknown = {unknown[0]}'
		mtk = eval(f"{unknown[0]}+ 11")
		uri1 = findall(r"\.href.=.\"/(.*?)/\"", js_script)
		uri2 = findall(r"\)\+\"/(.*?)\"", js_script)
	elif unknown1:
		method = f'unknown1 = {unknown1[0]}'
		mtk = eval(unknown1[0])
		uri1 = findall(r"\.href.=.\"/(.*?)/\"", js_script)
		uri2 = findall(r"\+.\"/(.*?)\"", js_script)
	else:
		return ("ERROR: Direct link not found")
	if not any([uri1, uri2]):
		return (
			f"ERROR: uri1 or uri2 not found with method {method}")
	domain = urlparse(url).hostname
	return f"https://{domain}/{uri1[0]}/{mtk}/{uri2[0]}"
