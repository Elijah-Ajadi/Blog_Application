from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.http import JsonResponse
from .forms import PostForm, CommentForm, SignUpForm
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Profile
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    Blogg = Post.objects.exclude(status='draft')
    return render(request, 'index.html', {'Blogg': Blogg})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Create profile
            profile = Profile.objects.create(user=user,email=email,)
            profile.save()

            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('login')


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


# def post_list(request):
#     polist = Post.objects.exclude(status='draft')
#     return render(request, 'post_list.html', {'polist': polist})


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
