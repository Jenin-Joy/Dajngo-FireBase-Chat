from django.shortcuts import render
import firebase_admin
from firebase_admin import storage,auth,firestore,credentials
import pyrebase
from datetime import datetime
# Create your views here.

db = firestore.client()

config = {
  "apiKey": "AIzaSyBg6B0rqBRKNM_bCtfKXTOJKbLtImTezb8",
  "authDomain": "django-firebase-chat-6fbd8.firebaseapp.com",
  "projectId": "django-firebase-chat-6fbd8",
  "storageBucket": "django-firebase-chat-6fbd8.appspot.com",
  "messagingSenderId": "370675729038",
  "appId": "1:370675729038:web:58b02265c420208ff47fdf",
  "measurementId": "G-DX3SSN5JD7",
  "databaseURL":""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
sd = firebase.storage()

def home(request):
    users = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    ousers = db.collection("tbl_user").where("user_id", "!=", users["user_id"]).stream()
    user = []
    for i in ousers:
        user.append({"us":i.to_dict(),"id":i.id})
    return render(request,"User/HomePage.html",{"user":user})

def chat(request,id):
    to_user = db.collection("tbl_user").document(id).get().to_dict()
    return render(request,"User/Chat.html",{"user":to_user,"tid":id})

def ajaxchat(request):
    image = request.FILES.get("file")
    tid = request.POST.get("tid")
    if image:
        path = "ChatFiles/" + image.name
        sd.child(path).put(image)
        d_url = sd.child(path).get_url(None)
        db.collection("tbl_chat").add({"chat_content":"","chat_time":datetime.now(),"user_from":request.session["uid"],"user_to":request.POST.get("tid"),"chat_file":d_url})
        return render(request,"User/Chat.html",{"tid":tid})
    else:
        db.collection("tbl_chat").add({"chat_content":request.POST.get("msg"),"chat_time":datetime.now(),"user_from":request.session["uid"],"user_to":request.POST.get("tid"),"chat_file":""})
        return render(request,"User/Chat.html",{"tid":tid})

def ajaxchatview(request):
    tid = request.GET.get("tid")
    user_ref = db.collection("tbl_chat")
    chat = db.collection("tbl_chat").order_by("chat_time").stream()
    data = []
    for c in chat:
        cdata = c.to_dict()
        if ((cdata["user_from"] == request.session["uid"]) | (cdata["user_to"] == request.session["uid"])) & ((cdata["user_from"] == tid) | (cdata["user_to"] == tid)):
            data.append(cdata)
    return render(request,"User/ChatView.html",{"data":data,"tid":tid})