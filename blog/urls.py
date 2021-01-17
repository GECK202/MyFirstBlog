from django.urls import path
from . import views


urlpatterns = [
	path('', views.postcard_list, name='postcard_list'),
	path('postcard/<int:pk>/', views.postcard_detail, name='postcard_detail'),
	path('postcard/new/', views.postcard_new, name='postcard_new'),
	path('postcard/<int:pk>/edit/', views.postcard_edit, name='postcard_edit'),
	path('drafts/', views.postcard_draft_list, name='postcard_draft_list'),
	path('postcard/<int:pk>/publish/', views.postcard_publish, name='postcard_publish'),
	path('postcard/<pk>/remove/', views.postcard_remove, name='postcard_remove'),
	path('postcard/<int:pk>/comment/', views.add_comment_to_postcard, name='add_comment_to_postcard'),
	path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
	path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
	path('register/', views.register, name='register'),
]
