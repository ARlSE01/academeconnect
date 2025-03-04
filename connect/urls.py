from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.homepage),
    path('registration',views.registration),
    path('createpost',views.createpost),

    # path('reg',views.reg)
]