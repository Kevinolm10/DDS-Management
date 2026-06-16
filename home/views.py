from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from blog.models import Post
from .models import Contact, Players, agents

def home(request):
    agent_list = agents.objects.all().order_by('-created_at')

    post_list = Post.objects.filter(is_published=True).select_related('category').order_by('-created_at')
    post_paginator = Paginator(post_list, 6)
    post_page_number = request.GET.get('post_page')
    posts = post_paginator.get_page(post_page_number)

    player_list = Players.objects.all().order_by('-created_at')
    player_paginator = Paginator(player_list, 8)
    player_page_number = request.GET.get('player_page')
    players = player_paginator.get_page(player_page_number)

    return render(request, 'home/home.html', {
        'agents': agent_list,
        'posts': posts,
        'players': players
    })

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validate required fields
        if not all([name, email, subject, message]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Please fill in all required fields.'
                })
            messages.error(request, 'Please fill in all required fields.')
            return redirect('home')

        try:
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

            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your message! We will get back to you soon.'
                })

            # Fallback for non-AJAX requests
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('home')

        except Exception as e:
            # Handle any database or other errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Something went wrong. Please try again later.'
                })
            messages.error(request, 'Something went wrong. Please try again later.')
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


# Add players
def add_player(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        club = request.POST.get('club')
        image = request.FILES.get('image')

        if not all([name, position, club, image]):
            messages.error(request, 'Please fill in all fields and upload an image.')
            return redirect('home')

        player = Players(name=name, position=position, club=club, image=image)
        player.save()
        messages.success(request, 'Player added successfully!')
        return redirect('home')

    return render(request, 'home/add_player.html')

# Remove player
def remove_player(request, player_id):
    try:
        player = Players.objects.get(player_id=player_id)
        player.delete()
        messages.success(request, 'Player removed successfully!')
    except Players.DoesNotExist:
        messages.error(request, 'Player not found.')
    return redirect('home')

# Update player
def update_player(request, player_id):
    try:
        player = Players.objects.get(player_id=player_id)
    except Players.DoesNotExist:
        messages.error(request, 'Player not found.')
        return redirect('home')

    if request.method == 'POST':
        player.name = request.POST.get('name')
        player.position = request.POST.get('position')
        player.club = request.POST.get('club')
        image = request.FILES.get('image')
        if image:
            player.image = image
        player.save()
        messages.success(request, 'Player updated successfully!')
        return redirect('home')

    return render(request, 'home/update_player.html', {'player': player})

# View player details
def player_detail(request, player_id):
    try:
        player = Players.objects.get(player_id=player_id)
    except Players.DoesNotExist:
        messages.error(request, 'Player not found.')
        return redirect('home')

    return render(request, 'home/player_detail.html', {'player': player})