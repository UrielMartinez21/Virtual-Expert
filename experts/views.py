from django.shortcuts import render
from .models import Expert
from django.contrib.auth.decorators import login_required


@login_required
def my_virtual_experts(request):
    experts = Expert.objects.filter(profile__user=request.user)
    return render(request, 'experts/my_virtual_experts.html', {'experts': experts})


@login_required
def create_virtual_expert(request):
    return render(request, 'experts/create_virtual_expert.html')