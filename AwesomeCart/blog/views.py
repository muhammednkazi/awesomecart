from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost

# Create your views here.
def index(request):
    allblogs=Blogpost.objects.all()
    # for i in allblogs:   
    #     print(i)
    return render(request,'blog/index.html',{'allblogs':allblogs})

def blogpost(request,id):
    #sending the requested blogpost
    post=Blogpost.objects.filter(post_id=id)[0]
    print(post)

    #for diplaying previous post if any
    if Blogpost.objects.filter(post_id= id-1):
        prev_post=Blogpost.objects.filter(post_id=id-1)[0]
        print(prev_post)
    else:
        print("no data found")
        prev_post=''


    #for diplaying next post if any
    if Blogpost.objects.filter(post_id=id+1):
        next_post=Blogpost.objects.filter(post_id=id+1)[0]
        print(next_post)
    else:
        print("no data found")
        next_post=''
        
    return render(request,'blog/blogpost.html',{'post':post,'prev_post':prev_post,'next_post':next_post})