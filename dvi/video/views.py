from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CommentForm
from .models import Video, CUser, Comment
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.db.models import Q

def index(request):
    vid=Video.objects.all()
    users=CUser.objects.all()

    #SEARCH
    search_string = request.GET.get('search_string')
    if search_string != None:
        search_list = search_string.split(' ')
        print('search list', search_list)
        my_filter = Q()
        for item in search_list:
            my_filter = my_filter | Q(category__icontains=item) | Q(videotitle__icontains=item) | Q(videodesc__icontains=item)

        if not my_filter:
            messages.info(request, 'No result for your search')
            return redirect('index')

        vid = Video.objects.filter(my_filter)

    else:
        vid = Video.objects.all()

    if 'username' in request.session:
        uname=request.session['username']
        return render(request, 'index.html', {'videos': vid, 'users':users, 'uname': uname})

    return render(request, 'index.html',  {'videos': vid, 'users':users})

def play_video(request, id):
    details = Video.objects.filter(id=id)
    v_id1 = Video.objects.get(id=id)
    comments = Comment.objects.filter(v_id=v_id1)
    users = CUser.objects.all()

    if 'username' in request.session:
        uname=request.session['username']
        return render(request, 'play_video.html', {'details':details, 'uname':uname, 'users':users, 'comments':comments})
    return render(request,'play_video.html', {'details':details, 'users':users, 'comments':comments})

def register(request):
    if request.method=='POST':
        username1 = request.POST['username']
        password1a = request.POST['password1']
        password2a = request.POST['password2']
        displayname1 = request.POST['displayname']
        emailID1 = request.POST['emailID']

        if password1a==password2a:
            cuser = CUser(username=username1, password=password1a, displayname=displayname1, emailID=emailID1)
            cuser.save()
            return redirect('index')
        else:
            error1="Password entered didn't match"
            return render(request, 'register.html',{'error':error1})
    else:
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username1 = request.POST['username']
        password1a = request.POST['password1']

        request.session['username'] = username1
        uname = request.session['username']

        user = CUser(username=username1, password=password1a)
        if user is not None:
            return redirect('index')
        else:
            messages.info(request,'Invalid User')
            return redirect('register')
    else:
        return render(request,'register.html')

def logout(request):
    auth_logout(request)
    users = CUser.objects.all()
    vid = Video.objects.all()
    return render(request, 'index.html', {'users':users, 'videos':vid})

def upload_video(request):
    uname = request.session['username']
    if request.method == 'POST' and request.FILES['videofile'] and request.FILES['thumbnailimg']:
        category1 = request.POST['category']
        videotitle1 = request.POST['videotitle']
        videodesc1 = request.POST['videodesc']
        thumbnailimg1 = request.FILES['thumbnailimg']
        videofile1 = request.FILES['videofile']
        vusername = CUser.objects.get(username=uname)
        print('vusername',vusername)
        form = Video(category=category1, videotitle=videotitle1, videodesc=videodesc1, vusername=vusername, thumbnailimg=thumbnailimg1, videofile=videofile1)
        form.save()
        vid = Video.objects.filter(vusername=vusername)
        users = CUser.objects.filter(username=uname)

        return render(request, 'index.html', {'uname':uname, 'videos':vid, 'users':users})
    else:
        return render(request, 'upload_video.html', {'uname':uname})

def add_comment(request):
    #post=get_object_or_404(Video, slug=slug)
    if request.method == 'GET':
        form = CommentForm(request.GET)
        if form.is_valid():
            #################
            cname1 = request.GET.get('cname')
            content1 = request.GET.get('content')
            v_id = request.GET.get('v_id')
            v_id1 = Video.objects.get(id=v_id)
            comment = Comment(content=content1, v_id=v_id1, cname=cname1)
            comment.save()

            details = Video.objects.filter(id=v_id)
            comments = Comment.objects.filter(v_id=v_id)
            users = CUser.objects.all()
            uname = request.session['username']
            return render(request, 'play_video.html', {'details':details, 'users':users, 'comments':comments, 'uname':uname})
            ##################
        else:
            form = CommentForm()
        return render(request, 'play_video.html',  {'form': form})
