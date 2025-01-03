from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from . import models
from Makeover.models import Order
from django.shortcuts import render, redirect


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email'].strip().lower()
        password = request.POST['password']
        fullname = request.POST['full_name'].strip().lower().split(' ')
        if fullname:
            first_name = fullname[0].capitalize()
            last_name = fullname[-1].capitalize()
        else:
            first_name, last_name = '', ''

        try:
            user = models.UserModel.objects.create_user(first_name=first_name,
                                                        last_name=last_name,
                                                        email=email,
                                                        password=password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')
        except Exception as e:
            print(e)

    return render(request, 'signup.html')


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST['email'].strip().lower()
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {'error': 'Invalid email or password'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def email_available(request):
    if request.method == 'GET':
        email = request.GET['email'].lower()

        if models.UserModel.objects.filter(email=email).exists():
            return JsonResponse({'available': False})
        else:
            return JsonResponse({'available': True})

    return JsonResponse({'available': False})


def personal_info(request):
    if request.GET.get('request_type') == 'async':
        return render(request, 'profile/personal_info.html')
    return render(request, 'profile/base.html', {'request_type': 'sync'})


def orders(request):
    qs = Order.objects.filter(customer=request.user, payments__status='completed').distinct()
    context = {'orders': qs}
    return render(request, 'profile/orders.html', context)


def profile_manager(request):
    if not request.user.is_authenticated:
        return redirect('login_view')

    view = request.GET.get('view')
    if not view:
        return personal_info(request)

    views = {
        'personalInfo': personal_info(request),
        'orders': orders(request),
        'signOut': login_view(request)
    }

    return views[view]


@csrf_exempt
def update_personal_info(request):
    if request.method == 'POST':
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)

        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip()
        phone = request.POST.get('phone').strip()
        address = request.POST.get('address').strip()
        zipcode = request.POST.get('zip_code').strip()

        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        user.first_name = first_name or user.first_name
        user.last_name = last_name or user.last_name
        user.email = email or user.email
        user.phone = phone or user.phone
        user.address = address or user.address
        user.zipcode = zipcode or user.zipcode

        try:
            user.save()
            return JsonResponse({'message': 'Profile updated successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Failed to update profile: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def update_profile_picture(request):
    if request.method == 'POST':
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)

        profile_pic = request.FILES.get('profile_pic')
        if not profile_pic:
            return JsonResponse({'error': 'Profile picture is required'}, status=400)

        user.profile_pic = profile_pic
        try:
            user.save()
            return JsonResponse({'message': 'Profile picture updated successfully!', 'image_uri': user.profile_pic.url}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Failed to update profile picture: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
