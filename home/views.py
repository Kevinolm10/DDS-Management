from django.shortcuts import render

from blog.models import Post  # Use capital P for consistency


def home(request):
    posts = Post.objects.all()
    return render(request, 'home/home.html', {'Posts': posts})
