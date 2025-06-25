from django.shortcuts import render
from .models import Expert
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def my_virtual_experts(request):
    experts = Expert.objects.filter(profile__user=request.user)
    return render(request, 'experts/my_virtual_experts.html', {'experts': experts})


@login_required
def create_virtual_expert(request):
    return render(request, 'experts/create_virtual_expert.html')


@login_required
@require_http_methods(["POST"])
def send_data_to_expert(request):
    try:
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        Expert.objects.create(
            profile=request.user.profile,
            name=name,
            description=description,
            slug=name.replace(' ', '-').lower()
        )
        return JsonResponse({'message': 'Virtual expert created successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def delete_expert(request, slug_expert):
    try:
        expert = Expert.objects.get(slug=slug_expert, profile__user=request.user)
        expert.delete()
        return JsonResponse({'message': 'Deleted successfully'}, status=200)
    except Expert.DoesNotExist:
        return JsonResponse({'message': 'Expert not found'}, status=404)