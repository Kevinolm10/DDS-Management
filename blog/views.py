from django.shortcuts import render
from .models import Post
from django.http import HttpResponse

# Create your views here.
def all_posts(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/all_posts.html', context)

def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponse("Post not found", status=404)
    context = {
        'post': post
    }
    return render(request, 'blog/post_detail.html', context)

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        post = Post(title=title, content=content, image=image)
        post.save()
        return HttpResponse("Post created successfully", status=201)
    elif request.method == 'GET':
        # Render a form for creating a new post
        return render(request, 'blog/create_post.html')
    else:
        return HttpResponse("Method not allowed", status=405)

def update_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponse("Post not found", status=404)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        post.title = title
        post.content = content
        if image:
            post.image = image
        post.save()  # Fixed the call to `save()` (was using `Post.save()` incorrectly)
        return HttpResponse("Post updated successfully", status=200)
    elif request.method == 'GET':
        # Render a form for updating the post
        context = {
            'post': post
        }
        return render(request, 'blog/update_post.html', context)
    else:
        return HttpResponse("Method not allowed", status=405)

def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)  # Fixed the variable name (was `Post = Post.objects.get()` which is incorrect)
    except Post.DoesNotExist:
        return HttpResponse("Post not found", status=404)
    if request.method == 'POST':
        post.delete()  # Fixed the delete operation (was `Post.delete()` which is incorrect)
        return HttpResponse("Post deleted successfully", status=200)
    elif request.method == 'GET':
        # Render a confirmation page for deleting the post
        context = {
            'post': post  # Fixed the variable name (was `Post` instead of `post`)
        }
        return render(request, 'blog/delete_post.html', context)
    else:
        return HttpResponse("Method not allowed", status=405)

def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query)  # Fixed the variable name (was `Posts` instead of `posts`)
    else:
        posts = Post.objects.all()
    context = {
        'posts': posts,  # Fixed the variable name (was `Posts` instead of `posts`)
        'query': query
    }
    return render(request, 'blog/search_posts.html', context)

def filter_posts_by_date(request):
    date = request.GET.get('date')
    if date:
        posts = Post.objects.filter(created_at__date=date)  # Fixed the variable name (was `Posts` instead of `posts`)
    else:
        posts = Post.objects.all()
    context = {
        'posts': posts,  # Fixed the variable name (was `Posts` instead of `posts`)
        'date': date
    }   
    return render(request, 'blog/filter_posts_by_date.html', context)
