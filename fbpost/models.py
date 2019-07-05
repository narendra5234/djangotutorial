from django.db import models
import datetime
from django.utils import timezone


# Create your models here.
class User(models.Model):
    # user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=30)
    pic_url = models.URLField()


class Post(models.Model):
    # post_id = models.IntegerField(primary_key=True)
    post_datetime = models.DateTimeField()
    post_content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')


class Comment(models.Model):
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_comments', default=None,
    #                                    null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_at = models.DateTimeField()
    comment_content = models.TextField()


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reply')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply')
    reply_at = models.DateTimeField()
    reply_content = models.TextField()


class Reactions(models.Model):
    common_reactions = [
        ('LIKE', 'LIKE'),
        ('LOVE', 'LOVE'),
        ('HAHA', 'HAHA'),
        ('WOW', 'WOW'),
        ('SAD', 'SAD')]

    react_type = models.CharField(max_length=10, choices=common_reactions)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reaction', default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reaction')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reaction', default=None, null=True)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='reaction', default=None, null=True)
