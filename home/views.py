from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from blog.models import Post
from .models import Contact

@cache_page(60 * 15)  # Cache for 15 minutes
def home(request):
    post_list = Post.objects.filter(is_published=True).select_related('category').order_by('-created_at')
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'home/home.html', {'posts': posts})

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to database
        contact = Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Send email notification (optional)
        try:
            send_mail(
                subject=f'New Contact Form Submission: {subject}',
                message=f'''
                New contact form submission from {name}:

                Email: {email}
                Subject: {subject}

                Message:
                {message}
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't fail the form submission
            print(f"Email sending failed: {e}")

        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('home')

    return redirect('home')


@require_GET
def robots_txt(request):
    """Generate robots.txt file"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /summernote/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")