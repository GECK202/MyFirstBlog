from django.contrib import admin
from .models import Account, Postcard, Comment, Content

admin.site.register(Account)
admin.site.register(Postcard)
admin.site.register(Comment)
admin.site.register(Content)
