from django.shortcuts import get_object_or_404, render
from .models import Expert
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import os
import json
import fitz
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from django.core.files.storage import default_storage
from experts import basic_answer_from_context

model = SentenceTransformer('all-MiniLM-L6-v2')


@login_required
def my_virtual_experts(request):
    experts = Expert.objects.filter(profile__user=request.user)
    return render(request, 'experts/my_virtual_experts.html', {'experts': experts})


# ===========================| Create virtual experts |===========================
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


# ===========================| Train Virtual Expert |===========================
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

        # === Delete previous files (PDF, index, chunks)
        index_path = os.path.join(settings.MEDIA_ROOT, f"indices/{slug}.index")
        chunks_path = os.path.join(settings.MEDIA_ROOT, f"indices/{slug}_chunks.json")
        doc_path_pdf = os.path.join(settings.MEDIA_ROOT, f"documents/{slug}.pdf")

        for path in [index_path, chunks_path, doc_path_pdf]:
            if os.path.exists(path):
                os.remove(path)

        file = request.FILES.get("document")
        if not file:
            return JsonResponse({'message': 'No file provided'}, status=400)

        # Save file
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


# ===========================| CRUD |===========================
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


# ===========================| CRUD |===========================
@login_required
def chat_virtual_expert(request, slug):
    expert = get_object_or_404(Expert, slug=slug, profile=request.user.profile)
    answer = None
    question = None

    if request.method == "POST":
        question = request.POST.get("question")
        if not question:
            return render(request, "experts/chat_virtual_expert.html", {"expert": expert, "error": "Question required"})

        # Load index and chunks
        index_path = os.path.join(settings.MEDIA_ROOT, f"indices/{slug}.index")
        chunks_path = os.path.join(settings.MEDIA_ROOT, f"indices/{slug}_chunks.json")

        if not os.path.exists(index_path) or not os.path.exists(chunks_path):
            return render(request, "experts/chat_virtual_expert.html", {"expert": expert, "error": "No data available for this expert."})

        index = faiss.read_index(index_path)
        with open(chunks_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        # Embed the question
        question_vector = model.encode([question])
        D, I = index.search(np.array(question_vector), k=5)  # top 5 chunks
        context = "\n".join([chunks[i] for i in I[0]])

        # Compose prompt (simple for now)
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        answer = basic_answer_from_context(prompt)
        print(f"Question: {question}\nAnswer: {answer}")

    return render(request, "experts/chat_virtual_expert.html", {
        "expert": expert,
        "question": question,
        "answer": answer
    })