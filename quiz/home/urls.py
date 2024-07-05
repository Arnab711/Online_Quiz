from django.urls import path
from . import views

urlpatterns = [
    path('',views.register_page,name='register'),
    path('login/',views.login_page,name='login'),
    path('home/',views.home,name='home'),
    path('home/quiz/<str:cat_name>',views.quiz,name='quiz'),
    path('home/result/',views.result,name='result'),
    path('home/submit-quiz/',views.submit_quiz,name='submit-quiz'),
    path('home/about/',views.about,name='about')
]
