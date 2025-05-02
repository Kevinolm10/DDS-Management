from django.shortcuts import render, redirect
from .models import Post
from django.http import HttpResponse

# Display all posts
def all_posts(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/all_posts.html', context)

# View details of a single post
def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponse("Post not found", status=404)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)

# Create a new post
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # Create and save the post
        post = Post(title=title, content=content, image=image)
        post.save()

        # Redirect to the created post's detail page
        return redirect('post_detail', post_id=post.id)

    return render(request, 'blog/create_post.html')

# Update an existing post
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
        post.save()

        # Redirect to the updated post's detail page
        return redirect('post_detail', post_id=post.id)

    context = {'post': post}
    return render(request, 'blog/update_post.html', context)

# Delete a post
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponse("Post not found", status=404)

    if request.method == 'POST':
        post.delete()
        # Redirect to all posts page after deletion
        return redirect('all_posts')

    context = {'post': post}
    return render(request, 'blog/delete_post.html', context)

# Search posts by title
def search_posts(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()

    context = {
        'posts': posts,
        'query': query
    }
    return render(request, 'blog/search_posts.html', context)

# Filter posts by creation date
def filter_posts_by_date(request):
    date = request.GET.get('date')
    if date:
        posts = Post.objects.filter(created_at__date=date)
    else:
        posts = Post.objects.all()

    context = {
        'posts': posts,
        'date': date
    }
    return render(request, 'blog/filter_posts_by_date.html', context)
