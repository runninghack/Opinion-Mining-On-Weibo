import json
import mysql.connector
from datetime import date, datetime, timedelta


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