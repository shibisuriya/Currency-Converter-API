import requests
from bs4 import BeautifulSoup
import flask
from flask import request


headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS \
          X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) \
          Chrome/71.0.3578.98 Safari/537.36", \
          "Accept":"text/html,application/xhtml+xml,application/xml; \
          q=0.9,image/webp,image/apng,*/*;q=0.8"}


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    f = str(request.args.get("f"))
    t = request.args.get("t")
    qty = request.args.get("qty")
    url = "https://in.investing.com/currencies/" + f + "-" + t
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    if(r.status_code == 200):
        rate = soup.find("bdo", {"class": "last-price-value"})
        rate = rate.text
        value = (float(rate) * float(qty))
        return {"Rate": rate, "Value": value}
    elif(r.status_code == 404):
        return {"Status code": r.status_code, "Message": "Currency pair is invalid!"} 
    else:
        return {"Status code": r.status_code, "Message": "Unknown error!"}

app.run()
