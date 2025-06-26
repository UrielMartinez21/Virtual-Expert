import json
from django.shortcuts import get_object_or_404, render
from .models import Expert
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.core.files.storage import default_storage
from sentence_transformers import SentenceTransformer
import fitz
import faiss
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

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


@login_required
def train_virtual_expert(request, slug):
    expert = get_object_or_404(Expert, slug=slug, profile=request.user.profile)
    return render(request, "experts/train_virtual_expert.html", {"expert": expert})


@login_required
@require_http_methods(["POST"])
def send_data_to_train(request):
    try:
        slug = request.POST.get("slug")
        expert = get_object_or_404(Expert, slug=slug, profile=request.user.profile)
        file = request.FILES.get("document")
        if not file:
            return JsonResponse({'message': 'No file provided'}, status=400)

        # Save file
        # file_path = default_storage.save(f"documents/{file.name}", file)
        extension = os.path.splitext(file.name)[1]
        file_path = default_storage.save(f"documents/{slug}{extension}", file)

        # === Step 1: Extract text (PDF only for now)
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        text = ""

        with fitz.open(full_path) as doc:
            for page in doc:
                text += page.get_text()

        # === Step 2: Chunk text
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]

        # === Step 3: Embed chunks
        embeddings = model.encode(chunks)

        # === Step 4: Store in FAISS (basic in-memory store for MVP)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(np.array(embeddings))

        # === Step 5: Save index to disk
        index_path = os.path.join(settings.MEDIA_ROOT, f"indices/{expert.slug}.index")
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(index, index_path)

        chunks_path = os.path.join(settings.MEDIA_ROOT, f"indices/{expert.slug}_chunks.json")
        with open(chunks_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f)
        return JsonResponse({'message': 'Virtual expert trained successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@csrf_exempt
@login_required
@require_http_methods(["DELETE"])
def delete_expert(request, slug_expert):
    try:
        expert = Expert.objects.get(slug=slug_expert, profile__user=request.user)
        expert.delete()
        base_path = os.path.join(settings.MEDIA_ROOT, "indices")
        paths = [
            os.path.join(base_path, f"{slug_expert}.index"),
            os.path.join(base_path, f"{slug_expert}_chunks.json"),
            os.path.join(settings.MEDIA_ROOT, f"documents/{slug_expert}.pdf"),  # optional
        ]
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        return JsonResponse({'message': 'Deleted successfully'}, status=200)
    except Expert.DoesNotExist:
        return JsonResponse({'message': 'Expert not found'}, status=404)