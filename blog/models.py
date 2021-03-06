from django.conf import settings
from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

class Account(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)


class Postcard(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
	title = models.CharField(max_length=200)
	text = models.TextField(blank=True, null=True)
	is_open = models.BooleanField(default = False)
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

class Content(models.Model):
	postcard = models.ForeignKey(Postcard, on_delete=models.CASCADE, related_name='contents')
	color = models.PositiveIntegerField(default = 0x44aa88)
	textcolor = models.CharField(max_length = 10, default = '#ff0000')
	type = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	pos_x = models.SmallIntegerField(default = 0)

	def __str__(self):
		return self.name

class Comment(models.Model):
	post = models.ForeignKey('blog.Postcard', on_delete=models.CASCADE, related_name='comments')
	author = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	approved_comment = models.BooleanField(default=False)

	def approve(self):
		self.approved_comment = True
		self.save()

	def __str__(self):
		return self.text

	def approved_comments(self):
		return self.comments.filter(approved_comment=True)
