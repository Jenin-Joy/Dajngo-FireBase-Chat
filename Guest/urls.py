from django.urls import path,include
from Guest import views
app_name = "webguest"

urlpatterns = [
    path('userreg/',views.userreg,name="userreg"),
    path('',views.login,name="login"),
    path('fpassword/',views.fpassword,name="fpassword"),
]