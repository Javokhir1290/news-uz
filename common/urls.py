from django.urls import path
from .views import *
from .auth_views import auth, otp, logout

urlpatterns = [
    path('', index, name='home'),
    path('view/<int:pk>/', view, name='view'),
    path('contact/', contact, name='contact'),
    path('search/', search, name='search'),
    path('category/<slug>/', category, name='category'),
    path('add_to_subs/<str:path>/', add_to_subs, name='subs_add'),


    #login + register
    path("auth/", auth, name='auth'),
    path("otp/", otp, name='otp'),
    path('logout/', logout, name='logout'),
]