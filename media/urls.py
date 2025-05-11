from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    # ... your existing patterns ...
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
from . views import homepage, media_detail, add_reviews, top100
# add_media 

from media.views import *
#afrom .views import add_media, homepage, media_detail

app_name = 'media'

urlpatterns = [
    path("", homepage, name="homepage"),
    path("media/<int:pk>/", media_detail, name="m_detail"),
    #path("add_media/", add_media, name="add_media"),
    path("add_reviews/", add_reviews, name="add_reviews"),
    path("top100/", top100, name="top100"),
    path("media/vote/<int:rating_id>/<str:action>/", views.vote_review, name='vote_review'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('report_comment/<int:comment_id>/', views.report_comment, name='report_comment'), #Abrar
]
