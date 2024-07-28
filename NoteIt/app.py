from flask import Flask,render_template,request,redirect
from flask_mysqldb import MySQL,MySQLdb



app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/",methods=["GET","POST"])
def StoreNote():
    if request.method == "POST":
        title = request.form.get("title")
        note = request.form.get("note")
        with open("NoteIt\\database.txt","a") as f:
            f.write(f"{title},{note}\n")
    return render_template("index.html")

@app.get("/shownote")
def shownote():
    values = []
    with open("NoteIt\\database.txt","r")as f:
        content = f.readlines()
    for note in content:
        title,para = note.split(",",1)
        value = (title,para)
        values.append(value)
    return render_template("shownote.html",data=values)

@app.get("/shownote/<path:title>&<path:para>")
def deletnote(title,para):
    with open("NoteIt\\database.txt","+r")as f:
        content = f.readlines()
        i=0
        for notes in content:
            note_title,note_para = notes.split(",",1)
            if note_title == title  :
                content.pop(i)
                break
            else:
                i+=1
                continue
    with open("NoteIt\\database.txt","w")as f:
        for notes in content:
            f.write(notes)
    return redirect("/shownote")
        

@app.route("/editnote/<path:title>&<path:para>")
def editnote(title="",para=""):
    return render_template("editnote.html",title=title,para=para)

@app.post("/editnote/<path:old_title>&<path:para>")
def updatenote(old_title,para):
    new_title = request.form.get("title")
    new_note = request.form.get("note")
    with open("NoteIt\\database.txt","+r")as f:
        content = f.readlines()
        notelist = list()
        for lines in list(content):
            lines = str(lines)
            cont = lines.split(",",1)
            notelist.append(cont)
        i=0
        for notes in notelist:
            title = notes[0]
            new_notes = []
            if old_title == title:
                new_notes.append(new_title)
                new_notes.append(f"{new_note}\n")
                notelist.remove(notes)
                notelist.insert(i,new_notes)
            i+=1
    with open("NoteIt\\database.txt","w")as f:
        for notes in notelist:
            title = notes[0]
            note = notes[1]
            f.write(f"{title},{note}")
    return redirect("/shownote")

app.run(debug=True,host="0.0.0.0")