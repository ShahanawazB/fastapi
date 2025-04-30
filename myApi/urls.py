from django.urls import path
from myApi import views 


urlpatterns = [
    path('hello-view', view=views.HelloApiView.as_view())
]