from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post

def home(request):
    post_list = Post.objects.all().order_by('-created_at')  # Order posts by creation date
    paginator = Paginator(post_list, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')  # Get the current page number from the URL
    posts = paginator.get_page(page_number)  # Get the paginated posts for the current page

    return render(request, 'home/home.html', {'posts': posts})