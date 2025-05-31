from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

def bypass_yeumoney(url):
    try:
        session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0"}
        res = session.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for script in soup.find_all("script"):
            if "window.location.href" in script.text:
                match = re.search(r'"(http.*?)"', script.text)
                if match:
                    return match.group(1)
        return None
    except:
        return None

def bypass_lootlink(url):
    try:
        res = requests.get(url, allow_redirects=True, timeout=10)
        if res.history:
            return res.url
        return None
    except:
        return None

def bypass_linkvertise(url):
    try:
        match = re.search(r"r=([^&]+)", url)
        if match:
            import base64
            decoded = base64.b64decode(match.group(1)).decode("utf-8")
            return decoded
        return None
    except:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        url = request.form.get("url")

        if "yeumoney.com" in url:
            result = bypass_yeumoney(url)
        elif "lootlink" in url:
            result = bypass_lootlink(url)
        elif "linkvertise" in url:
            result = bypass_linkvertise(url)
        else:
            error = "Trang rút gọn này chưa được hỗ trợ."

        if not result:
            error = "Không thể bypass link. Có thể link đã đổi cấu trúc hoặc cần xử lý JavaScript nâng cao."

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
