from flask import Flask, request, render_template, redirect, session
import pandas as pd
import saver
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = ""


@app.route('/', methods=['GET', 'POST'])
def hello_world():

    d = pd.read_csv("data.csv")
    

    if 'd' not in session:
        session['d'] = 0

    if request.method == 'POST':
        p_id = request.form['pic_id']
        label = request.form['label']
        n = saver.findAll(p_id, label)
        session['d'] = n

        return redirect("/")
    else:
        ID = saver.findNotUsed()
       
        lth = len(d)
        d = d.iloc[[ID]]
        data = saver.classReport()
       
        image = "http://static-maps.yandex.ru/1.x/?ll={0},{1}&pt={0},{1}&spn=0.0027,0.0027&l=map".format(float(d["Долгота"]), float(d["Широта"]))
        return render_template('index.html', pic_id=ID, image=image, addr=d["Address_left"].values[0], sess_done=session["d"], total=lth, data=data)


@app.route('/delete')
def delete_visits():
    session.pop('d', None)
    return redirect("/")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))