from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.http import JsonResponse
from .forms import PostForm, CommentForm
from django.urls import reverse


# Create your views here.
def index(request):
    Blogg = Post.objects.exclude(status='draft')
    return render(request, 'index.html', {'Blogg': Blogg})


def about(request):
    return render(request, 'about.html')


def post_single(request, post):
    post = get_object_or_404(Post, slug=post, status='published')

    current_path = request.get_full_path()
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            com_form = form.save(commit=False)
            com_form.post = post
            com_form.save()

            return redirect(current_path)
        else:
            print('Form is not valid. Errors:', form.errors)
    return render(request, 'single.html', {'post': post, "form": form})


def upload_file(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        uploaded_file = request.FILES['upload']
        return JsonResponse({'uploaded': True, 'url': 'path/to/uploaded/file'})
    return JsonResponse({'uploaded': False, 'error': 'No file Uploaded'})


def dashboard(request):
    return render(request, 'dashboard.html')


def posts_dashboard(request):
    polist = Post.objects.exclude(status='draft')
    return render(request, 'posts_dashboard.html', {'polist': polist})


def post_list(request):
    polist = Post.objects.exclude(status='draft')
    return render(request, 'post_list.html', {'polist': polist})


def comments_list(request):
    comments = Comment.objects.all()
    return render(request, 'comments.html', {'comments': comments})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a specific page upon successful creation
            return redirect(reverse('posts_dashboard'))
        else:
            print('Form is not valid. Errors:', form.errors)
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})
