from django.urls import path,include
from User import views
app_name = "webuser"
urlpatterns = [
    path('home/',views.home,name="home"),
    path('chat/<str:id>',views.chat,name="chat"),
    path('ajaxchat/',views.ajaxchat,name="ajaxchat"),
    path('ajaxchatview/',views.ajaxchatview,name="ajaxchatview"),
    path('deleteaccount/',views.deleteaccount,name="deleteaccount"),
    path('clearchat/',views.clearchat,name="clearchat"),
]