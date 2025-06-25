from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# =========================== | Create a new user | ===========================
def register_user(request):
    return render(request, 'users/register_user.html')


@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    try:
        # Data for user model
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Data for profile model
        max_experts = 1
        max_documents = 1
        plan_type = 'free'

        # Validate user
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists'}, status=400)

        # Create user and profile
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        Profile.objects.create(
            user=user,
            max_experts=max_experts,
            max_documents_per_expert=max_documents,
            plan_type=plan_type
        )

        # Automatically log in the user after creation
        login(request, user)
        return JsonResponse({'message': 'User created successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


# =========================== | Login and logout | ===========================
def login_user(request):
    return render(request, 'users/login_user.html')

@csrf_exempt
@require_http_methods(["POST"])
def send_data_to_login(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


def logout_user(request):
    logout(request)
    return redirect('login_user')


# =========================== | Dashboard | ===========================
@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html')
