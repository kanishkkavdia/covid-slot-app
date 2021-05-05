from flask import Flask, render_template,request
import requests
app=Flask(__name__,template_folder="template/")
import datetime
import json
f = open("static\states-and-districts.json",)
data=json.load(f)
base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(20)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]
@app.route("/")
def main():
    return render_template("index.html",data=data,date_str=date_str)
@app.route("/result",methods=["GET","POST"])
def result():
    min_age=int(request.args.get("min_age"))
    state=str(request.args.get("states"))
    district=str(request.args.get("districts"))
    date=str(request.args.get("date"))
    for state_code in range(1,40):
        response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_code))
        json_data = json.loads(response.text)
        for i in json_data["districts"]:
            if i["district_name"]==district:
                district_code=i["district_id"]
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(district_code,date)        
    response = requests.get(URL)
    if response.ok:
        resp_json = response.json()
    #url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=512&date=31-03-2021"
    return render_template("result.html",min_age=min_age,state=state,date=date,district=district,district_code=district_code,resp_json=resp_json)
@app.route("/result2",methods=["GET","POST"])
def result2():
    min_age=int(request.args.get("min_age"))
    pincode=int(request.args.get("pincode"))
    date=str(request.args.get("date"))
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode,date)
    response=requests.get(URL)
    if response.ok:
        resp_json=response.json()
    return render_template("result2.html",resp_json=resp_json,min_age=min_age,date=date)
if __name__=="__main__":
    app.run(debug=True,port=5000)