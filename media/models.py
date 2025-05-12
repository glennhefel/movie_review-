from django.db import models
from django.contrib.auth.models import User #Kuro
# Create your models here.
from django.conf import settings # Add this line to the the bottom of the imports 
from .models import * #Abrar

media_li=[
    ("Anime", "Anime"),
    ("Movies", "Movies"),
    ("TV_series", "TV_series")
]

genre_li=[
    ("action","action"),
    ("psychological","psychological"), ("comedy","comedy"), ("romance","romance"), ("sci-fi","sci-fi"), ("cyberpunk","cyberpunk"), 


]

class Media(models.Model):
    title = models.CharField(max_length=250)
    release_date = models.DateField(auto_now=False, auto_now_add=False) #Kuro
    media = models.CharField(max_length=10 , choices=media_li)
    #certificate = models.CharField(max_length=3)
    #duration = models.DurationField()
    genre = models.CharField(max_length=30, choices=genre_li)
    director = models.CharField(max_length=250)
    description = models.CharField(max_length=1000, default="Theres nothing here...") #kuro
    #star1 = models.CharField(max_length=250)
    #star2 = models.CharField(max_length=250)
    #star3 = models.CharField(max_length=250)
    #star4 = models.CharField(max_length=250)
    #overview = models.TextField(max_length=1000)
    poster = models.URLField(max_length=500)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        return self.ratings.all().aggregate(models.Avg('rating')).get('rating__avg',0.0)
    
    @property
    def total_votes(self):
        return self.ratings.all().aggregate(models.Count('rating')).get('rating__count',0)

class Rating(models.Model):
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    #Kuro
    
    comment = models.TextField(default="(This guy wrote nothing)")
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    ###
    def __str__(self):
        return f"{self.media} - {self.user}"

#Kuro
class Hanekawa(models.Model):
    RATE_CHOICES = (
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=4, choices=RATE_CHOICES)

   

####
#Abrar
class CommentReport(models.Model):
    Report_reasons = [
        ('hate_speech', 'Hate Speech'),
        ('spam', 'Spam'),
        ('abusive', 'abusive language'),
        ('offensive', 'Offensive content'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Rating, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=Report_reasons)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Report by {self.user.username} on comment {self.comment.id}"
    
    