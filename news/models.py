from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from .utils import censor_text
from django.urls import reverse
from django.core.validators import MinLengthValidator




class Author(models.Model):
    rating=models.IntegerField(default=0)
    name=models.OneToOneField(User,on_delete=models.CASCADE)




    def update_rating(self):
        post=self.post_set.aggregate(postRating=Sum('rating')) # type: ignore
        pr=0
        pr+=post.get('postRating')

        comment=self.AuUser.comment_set.aggregate(commentRating=Sum('rating')) # type: ignore
        pr_1=0
        pr_1+=comment.get('commentRating')

        self.rating=pr*3+pr_1
        self.save()

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)

    sub=models.ManyToManyField(User,blank=True)
    def subscribe(self):
        pass
    def get_category(self):
        return self.name
    def __str__(self):
        return self.name

    
    
class Post(models.Model):
    author=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='Author')

    
    Choises=(
        ('article','статья'),
        ('new','новость')
    )
    rating=models.IntegerField(default=0)
    data_time=models.DateTimeField(auto_now_add=True)
    choose=models.CharField(max_length=10,choices=Choises,default='new')
    category=models.ManyToManyField(Category,through='Post_Category')
    title=models.CharField(max_length=32,validators=[MinLengthValidator(2)])
    text=models.TextField(validators=[MinLengthValidator(10)])

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -=1
        self.save()
    
    def __str__(self):
        return f'{self.title}: {self.text[:20]} ...'
    
    def save(self, *args, **kwargs):
        self.text = censor_text(self.text)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])     # type: ignore
    
class Post_Category(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

class Comment(models.Model):
    rating=models.IntegerField(default=0)
    text=models.TextField(max_length=256)
    date_time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -=1
        self.save()
    

class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
