from django import forms

from .models import Postcard, Comment, Content


class PostcardForm(forms.ModelForm):

	class Meta:
		model = Postcard
		fields = ('title',)

class ContentForm(forms.ModelForm):

	class Meta:
		model = Content
		fields = ('name', 'type', 'color', 'pos_x',)

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('author', 'text',)
