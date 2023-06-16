from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Bid(models.Model):
    bid=models.IntegerField(default=15)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bid")
    def __str__(self) -> str:
      return f'{self.bid}'
class Listing(models.Model):
    title=models.CharField(max_length=64)
    owner=models.CharField(max_length=64)
    url=models.CharField(max_length=800)
    description=models.CharField(max_length=400)
    bid=models.ForeignKey(Bid,on_delete=models.CASCADE,related_name="lisiting",default=None)
    # watchlist = models.ForeignKey(User,blank=True, related_name="watch_listings",on_delete=models.CASCADE,default=None)
    watchlist = models.ManyToManyField(User,related_name="watch_list",blank=True)
    # watchlist = models.CharField(max_length=64,null=True,blank=True)
    # watchlist = models.CharField(max_length=64,blank=True,null=True)
    category=models.CharField(max_length=64,null=True,blank=True)
    is_closed = models.BooleanField(default=False, blank=True, null=True)
    def __str__(self) -> str:
        return f'{self.title}'
class Comment(models.Model):
    comment=models.CharField(max_length=1000)
    writer=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="comments")
    def __str__(self) -> str:
        return f'{self.writer}'
# class watchlist(models.Model):
#     watch_list=models.ForeignKey(User,on_delete=models.CASCADE,related_name="watch_list")
#     listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="comments")
#     def __str__(self) -> str:
#        return f'{self.watch_list}'