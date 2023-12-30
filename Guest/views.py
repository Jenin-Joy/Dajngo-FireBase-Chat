from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import firestore,credentials,storage,auth
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
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


def userreg(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            user = firebase_admin.auth.create_user(email=email,password=password)
        except:
            return render(request,"Guest/UserReg.html",{"msg":"Error"})
        db.collection("tbl_user").add({"user_id":user.uid,"user_name":request.POST.get("txt_name"),"user_contact":request.POST.get("txt_contact"),"user_email":request.POST.get("txt_email")})
        return render(request,"Guest/UserReg.html",{"msg":"Account Created.."})
    else:
        return render(request,"Guest/UserReg.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            user = auth.sign_in_with_email_and_password(email,password)
        except:
            return render(request,"Guest/Login.html",{"msg":"Error In Email Or Password.."})
        userid = user["localId"]        
        user = db.collection("tbl_user").where("user_id", "==", userid).stream()
        for u in user:
            udata_id = u.id
        if udata_id:
            request.session["uid"] = udata_id
            return redirect("webuser:home")
        else:
            return render(request,"Guest/Login.html",{"msg":"Error"})
    else:
        return render(request,"Guest/Login.html")

def fpassword(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        reset_link = firebase_admin.auth.generate_password_reset_link(email)
        send_mail(
            'Forgot password ', #subject
            "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + reset_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
        return render(request,"Guest/Forgot_password.html",{"msg":email})
    else:
        return render(request,"Guest/Forgot_password.html")
