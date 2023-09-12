from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from dateutil import parser
import json, os, telegram
# import logging
import time

# from utils.utils import fake_utils
# from utils import search_boxname

app = Flask(__name__)
api = Api(app)

chatID = "xxxx"

bot = telegram.Bot("xxxxxxxx")

@app.route('/', methods=['POST'])
def handle_alert():
    try:
        content = json.loads(request.get_data())
        for alert in content['alerts']:
            message = "Status: "+alert['status']+"\n"
            if 'firing' in alert['status']:
                message = "Status: "+alert['status']+"  🔥"+"\n"
            else:
                message = "Status: "+alert['status']+"  ✅"+"\n"

            if 'name' in alert['labels']:
                message += "Instance: "+alert['labels']['instance']+"("+alert['labels']['name']+")\n"
            else:
                message += "Instance: "+alert['labels']['instance']+"\n"
            if 'info' in alert['annotations']:
                message += "Info: "+alert['annotations']['info']+"\n"
            if 'summary' in alert['annotations']:
                message += "Summary: "+alert['annotations']['summary']+"\n"                
            if 'description' in alert['annotations']:
                message += "Description: "+alert['annotations']['description']+"\n"
                if len(alert['annotations']['description'].split(" ")[0]) > 15: 
                    box_id = alert['annotations']['description'].split(" ")[0]
                    box_name = search_boxname(box_id)
                    message += "Box_Name: " + box_name + "\n"
                else:
                    pass

            if alert['status'] == "resolved":
                correctDate = parser.parse(alert['endsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Resolved: "+correctDate
            elif alert['status'] == "firing":
                correctDate = parser.parse(alert['startsAt']).strftime('%Y-%m-%d %H:%M:%S')
                message += "Started: "+correctDate
            bot.sendMessage(chat_id=chatID, text=message)
            time.sleep(0.2)
            return "Alert OK", 200
    except Exception as ex:
        print("error",ex)
        return {"status": "OK"}

if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    app.run(debug=True, host='0.0.0.0', port=10000)
