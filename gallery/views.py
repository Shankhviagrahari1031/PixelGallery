
from django.shortcuts import render, redirect, get_object_or_404
from .models import GalleryImage


def home(request):
    query = request.GET.get('q', '')
    images = GalleryImage.objects.all().order_by('-uploaded_at')

    if query:
        images = images.filter(title__icontains=query)

    return render(
        request,
        'gallery/home.html',
        {
            'images': images,
            'query': query,
        }
    )


def upload_image(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        image = request.FILES.get('image')

        if title and image:
            GalleryImage.objects.create(
                title=title,
                image=image
            )

    return redirect('home')


def delete_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)

    if request.method == 'POST':
        image.image.delete(save=False)
        image.delete()

    return redirect('home')
