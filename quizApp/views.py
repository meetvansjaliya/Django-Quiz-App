from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Quiz, Question, CreateUserForm, QuizTaker
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
# Create your views here.
lst = []
anslist = []
score = 0

def index(request):
    #fetch quiz from database
    quizes = Quiz.objects.all()
    params = {'quiz': quizes}
    lst.clear()
    anslist.clear()
    return render(request, 'index.html', params)

def signup(request):
    form = CreateUserForm()

    if request.method =="POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created. Please Login.')
        else:
            messages.warning(request, 'Something went wrong. Please try again')
    return render(request, 'signup.html', {'form':form})

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username') 
        password = request.POST.get('password')
        #check if user has entered correct credentials
        user = authenticate(username=username, password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("/")

        else:
            # No backend authenticated the credentials
            messages.warning(request, "Wrong Username or Password. Try Again")
            return render(request, 'login.html')

    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect("/")

def quizView(request, myid):
    if request.user.is_anonymous:
        return redirect("/login")
    
    obj = Question.objects.filter(quiz__id=myid)

    for i in obj:
        anslist.append(i.ans)
    
    paginator = Paginator(obj, 1)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        questions = paginator.page(page)
    except(EmptyPage, InvalidPage):
        questions = paginator.page(paginator.num_pages)

    return render(request, 'quizview.html', {'obj': obj, 'questions':questions})

def saveans(request):
    ans = request.GET['ans']
    lst.append(ans)
    return render(request, 'result.html')

def result(request, user_id):
    score = 0
    for i in range(len(lst)):
        if lst[i] == anslist[i]:
            score += 1
    score = (score/len(lst))*100

    user = User.objects.get(id = user_id)

    obj = QuizTaker.objects.create(
        user_name = user,
        score = score
    )
     
    return render(request, 'result.html', {"score": score})    

def scoreboard(request):
   users = QuizTaker.objects.all()
   return render(request, 'scoreboard.html', {"users": users})