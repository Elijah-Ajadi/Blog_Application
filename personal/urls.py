from django.urls import path
from personal import views
from.views import PostUpdateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('about.html', views.about, name='about'),
    path('<slug:post>/', views.post_single, name='post_single'),
    # path('post_list.html', views.post_list, name='post_list'),
    path('add_post.html', views.post_create, name='post_create'),
    path('posts_dashboard.html', views.posts_dashboard, name='posts_dashboard'),
    path('comments.html', views.comments_list, name='comments_list'),
    path('signup.html', views.signup, name='signup'),
    path('login.html', views.login, name='login'),
    path('logout.html', views.logout, name='logout'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('update_profile.html', views.update_profile, name='update_profile'),
]
