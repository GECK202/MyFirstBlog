from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Postcard, Comment, Content, Account

from django.template.base import TemplateSyntaxError

from .forms import PostcardForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseNotFound
#from django.contrib.auth.models import User
from django.http import Http404
from django.conf import settings

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm


def postcard_list(request):
	if request.user.is_anonymous:
		postcards = Postcard.objects.none()
	else:
		postcards = Postcard.objects.filter(author = request.user).filter(published_date__lte = timezone.now()).order_by('-published_date')
	return render(request, 'blog/postcard_list.html', {'postcards':postcards})

def postcard_detail(request, pk):
	try:
		postcard = Postcard.objects.get(pk=pk)
	except Postcard.DoesNotExist:
		raise Http404("Страница не найдена!")
	if (postcard.author != request.user) and (postcard.is_open == False):
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	#post = get_object_or_404(Post, is_open=True, pk=pk)
	return render(request, 'blog/postcard_detail.html', {'postcard': postcard})

@login_required
def postcard_new(request):
	if request.method == "POST":
		form = PostcardForm(request.POST)
		if form.is_valid():
			postcard = form.save(commit=False)
			postcard.author = request.user
			#post.published_date = timezone.now()
			postcard.save()
			return redirect('postcard_detail', pk=postcard.pk)
	else:
		form = PostcardForm()
	return render(request, 'blog/postcard_edit.html', {'form': form})

@login_required
def postcard_edit(request, pk):
	postcard = get_object_or_404(Postcard, pk=pk)
	if postcard.author != request.user:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	if request.method == "POST":
		form = PostcardForm(request.POST, instance=postcard)
		if form.is_valid():
			postcard = form.save(commit=False)
			postcard.author = request.user
			#post.published_date = timezone.now()
			postcard.save()
			return redirect('postcard_detail', pk=postcard.pk)
	else:
		act_fig = {'0':"Пусто",'add':"Добавить",'delete':"Удалить"}
		act_key = request.GET.get("act_fig", '0')
		if (act_key == 'add'):
			fig = Content()
			fig.postcard = postcard;
			colorList = {'Aqua':0x44aa88,'Purple':0x8844aa,'Gold':0xaa8844}
			color_name = request.GET.get("select_color")
			color = colorList[color_name]
			colort = request.GET.get("colorinput")
			fig.textcolor = colort
			fig.color = int(color)
			fig.type = request.GET.get("select_figure")
			fig.name = fig.type + " " + color_name
			fig.save()
		elif (act_key == 'delete'):
			try:
				id = int(request.GET.get("textinput", 0))
				fig = Content.objects.get(id=id)
				#raise TemplateSyntaxError("Undefined variable or unknown value for: %s" % "other")
				fig.delete()
			except ValueError:
				n = 1
				#return HttpResponseNotFound("<h2>Empty selector</h2>")
			except Content.DoesNotExist:
				n = 2
				#return HttpResponseNotFound("<h2>Figure not found</h2>")
		form = PostcardForm(instance=postcard)
	return render(request, 'blog/postcard_edit.html', {'form': form,'postcard': postcard, 'act_fig': act_fig[act_key]})

@login_required
def postcard_draft_list(request):
	postcards = Postcard.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/postcard_draft_list.html', {'postcards': postcards})

@login_required
def postcard_publish(request, pk):
	postcard = get_object_or_404(Postcard, pk=pk)
	postcard.publish()
	return redirect('postcard_detail', pk=pk)

@login_required
def postcard_remove(request, pk):
	postcard = get_object_or_404(Postcard, pk=pk)
	postcard.delete()
	return redirect('postcard_list')

def add_comment_to_postcard(request, pk):
	postcard = get_object_or_404(Postcard, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = postcard
			comment.save()
			return redirect('postcard_detail', pk=postcard.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_postcard.html', {'form': form})

@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('postcard_detail', pk=comment.postcard.pk)

@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.delete()
	return redirect('postcard_detail', pk=comment.postcard.pk)


def register(request):
	# Массив для передачи данных шаблонны
	data = {}
	# Проверка что есть запрос POST
	if request.method == 'POST':
		# Создаём форму
		form = UserCreationForm(request.POST)
		# Валидация данных из формы
		if form.is_valid():
			# Сохраняем пользователя
			form.save()
			# Передача формы к рендару
			data['form'] = form
			# Передача надписи, если прошло всё успешно
			data['res'] = "Всё прошло успешно"
			# Рендаринг страницы
			return render(request, 'blog/register.html', data)
	else: # Иначе
		# Создаём форму
		form = UserCreationForm()
		# Передаём форму для рендеринга
		data['form'] = form
		# Рендаринг страницы
		return render(request, 'blog/register.html', data)