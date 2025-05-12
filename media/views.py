from random import randint  

from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Avg, Count
from .models import Media, Rating , Hanekawa #Kuro
import os, json
from datetime import timedelta
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest #Kuro

#for signup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .models import *
from django.core.mail import send_mail  #Abrar

# Create your views here.

module_dir = os.path.dirname(__file__) # get current directory

def homepage(request):
    media = Media.objects.all().order_by("-id")
    context = {"media":media}
    return render(request, "media/homepage.html", context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('media:homepage')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def media_detail(request, pk):
    media = get_object_or_404(Media, pk=pk)
    ###Kuro
    user_reviewed = Rating.objects.filter(user=request.user, media=media).exists()
    # (new review submission)
    if request.method == "POST":
        rating_val = int(request.POST.get("rating"))
        comment_text = request.POST.get("comment", "").strip()
        if not comment_text:
          comment_text = "(This guy wrote nothing)"

        user = request.user

        # Save or update rating
        Rating.objects.update_or_create(
            media=media,
            user=user,
            defaults={"rating": rating_val, "comment": comment_text},
        )
        return redirect("media:m_detail", pk=pk)  # reload the page after submit

    average_rating = media.average_rating
    reviews = Rating.objects.filter(media=media).select_related("user").order_by("-id")
    #Kuro
    for review in reviews:
        review.user_vote = Hanekawa.objects.filter(user=request.user, rating=review).first()

    context = {
        "media": media,
        "average_rating": average_rating,
        "reviews": reviews,
        "user_reviewed": user_reviewed,
    } 
    return render(request, "media/m_details.html", context)
##Kuro

def top100(request):
    media = Media.objects.annotate(
        avr=Avg("ratings__rating"), 
        votes=Count("ratings__rating")  # First calculate average rating
    ).order_by("-avr")[:100]  # Then sort by average and take top 100
    
    context = {"media": media}
    return render(request, "media/homepage.html", context)

def add_reviews(request):
    for j in range(0,10000):
        for i in range(1,5):
            mediaID = randint(1,500)
            mediaRating = randint(1,10)
            add_rev(mediaID, i, mediaRating)
    return redirect("films:homepage")

def add_rev(g_media, g_user, g_rating):
    obj, create = Rating.objects.get_or_create(
        media = get_object_or_404(Media, pk=g_media),
        user = get_object_or_404(User, pk=g_user),
        rating = g_rating,
    )

#Kuro#####

@require_POST   
@login_required

def vote_review(request, rating_id, action):
    if action not in ["up", "down"]:
        return HttpResponseBadRequest("Invalid action")

    rating = get_object_or_404(Rating, id=rating_id)
    user = request.user

    existing_vote = Hanekawa.objects.filter(user=user, rating=rating).first()

    # Remove previous vote
    if existing_vote:
        if existing_vote.vote_type == action:
            # Toggle: same vote clicked again, remove it
            existing_vote.delete()
            if action == "up":
                rating.upvotes -= 1
            else:
                rating.downvotes -= 1
        else:
            # Switch vote
            if existing_vote.vote_type == "up":
                rating.upvotes -= 1
                rating.downvotes += 1
            else:
                rating.downvotes -= 1
                rating.upvotes += 1
            existing_vote.vote_type = action
            existing_vote.save()
    else:
        # New vote
        Hanekawa.objects.create(user=user, rating=rating, vote_type=action)
        if action == "up":
            rating.upvotes += 1
        else:
            rating.downvotes += 1

    rating.save()
    return redirect(request.META.get("HTTP_REFERER", "media:index"))
#Kurooo
class edit_review():
    pass

#Abrar 
@login_required
def report_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Rating, id=comment_id)
        reason = request.POST.get('reason')
        description = request.POST.get('description','')
        CommentReport.objects.create(
            user=request.user,
            comment=comment,
            reason=reason,
            description=description
        )
        return redirect('media:m_detail', pk=comment.media.pk)
    return redirect('media:homepage')

def delete_review(request, review_id):
       review = get_object_or_404(Rating, id=review_id)
    
   
       if review.user != request.user:
         raise Http404("You do not have permission to delete this review.")
    
   
       review.delete()
    
    
       return redirect("media:m_detail", pk=review.media.pk)






