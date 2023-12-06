from django.urls import path,include
from Guest import views
app_name = "webguest"

urlpatterns = [
    path('userreg/',views.userreg,name="userreg"),
    path('login/',views.login,name="login"),
]