from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from next_prev import next_in_order, prev_in_order
from django.http import HttpResponse , HttpResponseRedirect , JsonResponse
from django.template.loader import render_to_string
from accounts.models import Profile
# Create your views here.

def posts(request):
    query = Post.objects.filter(active=True).order_by('-created')
    paginator = Paginator(query, 12)
    page = request.GET.get('page')
    profile = get_object_or_404(Profile , slug=request.user.username)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "blog" : posts,
        'profile' : profile ,
    }
    return render(request,'blog.html' , context)



def detail(request , slug):
    post  = get_object_or_404(Post , slug=slug)
    profile = get_object_or_404(Profile , slug=request.user.username)
    likes = request.user.likes.all()
    readed = request.user.readed.all()
    is_liked = False
    if post.like.filter(id=request.user.id).exists():
        is_liked = True

    is_readed = False
    if post.readed.filter(id=request.user.id).exists():
        is_readed = True

    post.visits += 1
    post.save()
    next = next_in_order(post)
    pre = prev_in_order(post)

    if next and pre :
        next_article = get_object_or_404(Post , title=pre)
        pre_article = get_object_or_404(Post , title=next)
        context = {
            'post' : post ,
            'next_article' : next_article,
            'pre_article' : pre_article ,
            'likes' : likes ,
            'readed' : readed ,
            'is_liked' : is_liked ,
            'total_likes' : post.total_likes(),
            'is_readed' : is_readed ,
            'profile' : profile ,
        }
    elif next :
        pre_article = get_object_or_404(Post ,title=next)
        context = {
            'post' : post ,
            'pre_article' : pre_article ,
            'likes' : likes ,
            'readed' : readed ,
            'is_liked' : is_liked ,
            'total_likes' : post.total_likes(),
            'is_readed': is_readed ,
            'profile' : profile ,
        }

    elif pre :
        next_article = get_object_or_404(Post , title=pre)
        context = {
            'post' : post ,
            'next_article' : next_article,
            'likes' : likes,
            'readed' : readed,
            'is_liked' : is_liked ,
            'total_likes' : post.total_likes(),
            'is_readed' : is_readed,
            'profile' : profile ,
        }

    else:
        context = {
            'post' : post ,
            'likes' : likes ,
            'readed' : readed ,
            'is_liked' : is_liked ,
            'total_likes' : post.total_likes(),
            'is_readed' : is_readed ,
            'profile' : profile ,
        }
    return render(request , 'Single_post.html' , context)






def like_post(request):
    post = get_object_or_404(Post , id=request.POST.get('id'))
    print(post)
    is_liked = False
    if post.like.filter(id=request.user.id).exists():
        post.like.remove(request.user)
        is_liked = False

    else:
        post.like.add(request.user)
        is_liked = True

    context = {
        'post' : post ,
        'is_liked' : is_liked ,
        'total_likes' : post.total_likes(),

    }
    if request.is_ajax():
        html = render_to_string('like_section.html' , context , request=request)
        return JsonResponse({'form':html})



def read_post(request):
    post = get_object_or_404(Post , id=request.POST.get('id'))
    print(post)
    is_readed = False
    if post.readed.filter(id=request.user.id).exists():
        post.readed.remove(request.user)
        is_readed = False

    else:
        post.readed.add(request.user)
        is_readed = True

    context = {
        'post' : post ,
        'is_readed' : is_readed ,
        'total_likes' : post.total_readed(),

    }
    if request.is_ajax():
        html = render_to_string('read_section.html' , context , request=request)
        return JsonResponse({'form':html})
