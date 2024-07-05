from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from .models import *
import random
from django.urls import reverse
from urllib.parse import urlencode
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
# Create your views here.

def home(request):
    context = {'categories': Category.objects.all()}
    if request.method == 'GET' and 'category' in request.GET:
        cat_name = request.GET['category']
        obj = Category.objects.get(category_name=cat_name)
        return redirect(f'quiz/{obj.category_name}')
    return render(request, 'home.html', context)

def quiz(request,cat_name):
   try:
        question_objs=list(Question.objects.filter(category__category_name__icontains=cat_name))
        random.shuffle(question_objs)
        data=[]
        for q in question_objs:
            data.append(
                {
                "category": q.category.category_name,
                "question": q.question,
                "marks" :  q.marks,
                'answers': q.get_answers()
                }
            )
        payload= {'status' : True , 'data':data}
        print(payload)
        return render(request,'quiz.html',payload)
        
   except Exception as e:
        print(e)
        return HttpResponse('Something went wrong')
    

def submit_quiz(request):
    score=0
    total_marks=0
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('question'):
                ans=Answer.objects.get(uid__icontains=value)
                total_marks+=ans.question.marks
                if ans.is_correct:
                    score+=ans.question.marks

        print("User Score ",score)
        print("Total Marks ",total_marks)
        base_url = reverse('result')
        query_string =  urlencode({'score': score , 'total_marks':total_marks })
        url = '{}?{}'.format(base_url, query_string) 
        return redirect(url)  
    return redirect('home')


def result(request):
    if(request.method=='GET'):
        score=int(request.GET['score'])
        total_marks=int(request.GET['total_marks'])

    percentage = (score / total_marks) * 100
    incorrect_percentage = 100 - percentage
    context = {
        'score': score,
        'total_marks': total_marks,
        'percentage': percentage,
        'incorrect_percentage': incorrect_percentage
    }
    return render(request, 'result.html', context)


def register_page(request):
    return render(request,'register.html')


def login_page(request):
    return render(request,'login.html')



def about(request):
    return render(request,'about.html')