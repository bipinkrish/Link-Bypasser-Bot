from flask import Flask, request, render_template, make_response, send_file
import bypasser
import re
import os
import freewall


app = Flask(__name__)


def handle_index(ele):
    return bypasser.scrapeIndex(ele)


def store_shortened_links(link):
    with open('shortened_links.txt', 'a') as file:
        file.write(link + '\n')


def loop_thread(url):
    urls = []
    urls.append(url)

    if not url:
        return None

    link = ""
    temp = None
    for ele in urls:
        if re.search(r"https?:\/\/(?:[\w.-]+)?\.\w+\/\d+:", ele):
            handle_index(ele)
        elif bypasser.ispresent(bypasser.ddl.ddllist, ele):
            try:
                temp = bypasser.ddl.direct_link_generator(ele)
            except Exception as e:
                temp = "**Error**: " + str(e)
        elif freewall.pass_paywall(ele, check=True):
            freefile = freewall.pass_paywall(ele)
            if freefile:
                try: return send_file(freefile)
                except: pass
        else:
            try:
                temp = bypasser.shortners(ele)
            except Exception as e:
                temp = "**Error**: " + str(e)
        print("bypassed:", temp)
        if temp:
            link = link + temp + "\n\n"

    return link


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        result = loop_thread(url)
        if freewall.pass_paywall(url, check=True): return result
        
        shortened_links = request.cookies.get('shortened_links')
        if shortened_links:
            prev_links = shortened_links.split(',')
        else:
            prev_links = []

        if result:
            prev_links.append(result)
           
            if len(prev_links) > 10: 
                prev_links = prev_links[-10:]  

        shortened_links_str = ','.join(prev_links)        
        resp = make_response(render_template("index.html", result=result, prev_links=prev_links))
        resp.set_cookie('shortened_links', shortened_links_str)

        return resp

    shortened_links = request.cookies.get('shortened_links')
    return render_template("index.html", result=None, prev_links=shortened_links.split(",") if shortened_links else None)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
