import yaml
import json
import mysql.connector
from datetime import date, datetime, timedelta


def get_data():
    res = []
    for l in open('C:/Users/Ramiel/Desktop/2016_qd/2016 06 07'):
        res.append(l)
    return res


def read_config(fin='./config.yaml'):
    f = open(fin, 'r')
    dataMap = yaml.load(f)
    f.close()
    return dataMap


def enrich_text(t, keywords):
    new_t = t
    for k in keywords:
        if k in new_t:
            new_t = new_t.replace(k, "<b>" + k + "</b>")
    return new_t


def filter_data(weibos):
    res = []
    config = read_config()
    for d in weibos:
        js = json.loads(d)
        text = js['ltp'].split(' ')
        for item in config:
            keywords = item['category']['keywords']
            number = item['category']['number']
            name = item['category']['name']
            if len([word for word in keywords if word in text]) >= number:
                js['text'] = enrich_text(js['text'], keywords)
                js['type'] = name
                js['keywords'] = ('\t'.join([word for word in keywords if word in text])).encode('utf-8')
                res.append(js)
    return res


if __name__ == "__main__":
    db = mysql.connector.connect(host="192.168.8.3", user="root", password="ccpl_817", database="opinion")
    cursor = db.cursor()

    for d in filter_data(get_data()):
        try:
            cmd = ("INSERT INTO posts "
               "(id, date, text, keywords, uname, class) "
               "VALUES (%s, %s, %s, %s, %s, %s)")

            data = (d['sid'], datetime.fromtimestamp(float(d['created_at'])).date(), d['text'], str(d['keywords']), d['uid'], d['type'])

            cursor.execute(cmd, data)

            db.commit()
            print "success"
        except:
            break
            print "failed"
            db.rollback()
    db.close()