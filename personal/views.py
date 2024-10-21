from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Category
from django.http import JsonResponse
from django.views.generic import UpdateView
from .forms import PostForm, CommentForm, SignUpForm, ProfileForm, CategoryForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Profile
from django.contrib.auth.models import User
from django.db.models import Count


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
            password = form.cleaned_data['password']

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


def add_category(request):
    return render(request, 'new_category.html',)

def categories_dashboard(request):
    catlist = Category.objects.annotate(post_count=Count('post'))
    return render(request, 'category.html', {'catlist': catlist})




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

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('categories_dashboard'))
        else:
            print('Form is not valid. Errors:', form.errors)
    else:
        form =CategoryForm()
    return render(request, 'add_category.html', {'form': form})

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    fields = ['title',  'description', 'content', 'category', 'image', 'img_desc', 'tags']
    success_url = reverse_lazy('posts_dashboard')


def update_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('posts_dashboard'))  # Redirect to a success page
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {'form': form})

