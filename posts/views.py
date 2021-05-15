from django.http import HttpResponse
from django.views.generic import View
from django.views.generic import DeleteView
from django.core.paginator import Paginator
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from nekidaem.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core import mail



class MyView(View):
    template_name = 'index.html'
    def get(self, request):
        post_list = Post.objects.all()
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render (request, self.template_name, {'page': page})


class PostView(View):
    template_name = 'post_view.html'
    def get(self, request, pk):
        username = request.user
        post = get_object_or_404(Post, pk=pk)
        return render (request, self.template_name, {'post': post, 'username': username})

connection = mail.get_connection()

connection.open()
class NewView(View):
    form_class = PostForm
    template_name = 'new.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            co = 0
            xe = Follow.objects.all().filter(author=request.user)
            res = xe.count()
            while co != res:
                x = Follow.objects.all().filter(author=request.user)[co]
                x = x.user
                x = x.email
                email1 = mail.EmailMessage(
                            'Привет, почитай новости, там что-то интересное!',
                            f'http://127.0.0.1:8000/{post.id}',
                            'from@yourdjangoapp.com',
                            [x],
                            connection=connection,
                        )
                email1.send()
                co += 1
            return redirect('index')

        return render(request, self.template_name, {'form': form})


class ProfileView(View):
    template_name = 'profile.html'
    def get(self, request, username):
        author = get_object_or_404(User, username=username)
        author_posts = author.posts.all()
        paginator = Paginator(author_posts, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        following = (request.user.is_authenticated
                    and Follow.objects.filter(user=request.user,
                                            author=author).exists())
        context = {'username': author,
                   'author_posts': author_posts,
                   'page': page,
                   'following': following,
                   }
        return render(request, 'profile.html', context)

def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author=profile, pk=post_id)
    if request.user != profile:
        return redirect('post_profile', username=username, post_id=post_id)
    # добавим в form свойство files
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("post_view",
                            pk=post_id)

    return render(
        request, 'new.html', {'form': form, 'post': post},
    )



def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.id is not post.author.id:
        return redirect('post_view', pk=post_id)
    u = Post.objects.get(pk=post_id).delete()
    return redirect('index')   


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {'page': page})


@login_required
def profile_follow(request, username):
    author = User.objects.get(username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user,
                                     author=author)
        return redirect(reverse('profile', args=[username]))
    return redirect(reverse('profile', args=[username]))


@login_required
def profile_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=unfollow_user).delete()
    return redirect('profile', username=username) 