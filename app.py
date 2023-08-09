from flask import Flask, request, render_template, make_response
import bypasser
import threading
import re
import os
from texts import ddllist, gdrivetext, otherstext, ddltext, shortnertext, HELP_TEXT  # Import variables from texts.py

app = Flask(__name__)

# Function to handle link bypassing
def loop_thread(url):
    urls = []
    urls.append(url)

    if not url:
        return None

    link = ""
    for ele in urls:
        if re.search(r"https?:\/\/(?:[\w.-]+)?\.\w+\/\d+:", ele):
            handle_index(ele)
            return
        elif bypasser.ispresent(ddllist, ele):
            try:
                temp = ddl.direct_link_generator(ele)
            except Exception as e:
                temp = "**Error**: " + str(e)
        else:
            try:
                temp = bypasser.shortners(ele)
            except Exception as e:
                temp = "**Error**: " + str(e)
        print("bypassed:", temp)
        if temp:
            link = link + temp + "\n\n"

    return link
    # ... (rest of the function remains unchanged)

# Function to store the shortened links in cookies
def store_shortened_links(link):
    result = bypasser.scrapeIndex(ele)
    # ... (rest of the function remains unchanged)

# Main route to display the form and handle the link bypassing
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        result = loop_thread(url)
        shortened_links = request.cookies.get('shortened_links')
        return render_template("index.html", result=result, shortened_links=shortened_links.split(","))
    return render_template("index.html", result=None, shortened_links=None)

if __name__ == "__main__":
    print("Web Application Starting")
    app.run()
