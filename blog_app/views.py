from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from .models import BlogPost, Comments
from .forms import CreateForm, CommentForm
from users import forms


# Create your views here.
class BlogLoginView(LoginView):
    template_name = 'blog_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy('list-userblog')


class BlogRegistrationView(FormView):
    template_name = 'blog_app/register.html'
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)


@login_required
def listuserblogs(request):
    blogs = BlogPost.objects.filter(owner=request.user)
    search_input = request.GET.get('search-area') or ''
    if search_input:
        blogs = blogs.filter(title__icontains=search_input)
    context = {'blogs': blogs, 'search_input': search_input}
    return render(request, 'blog_app/listuserblog.html', context)


@login_required
def detailuserblogs(request, pk):
    blog = BlogPost.objects.filter(
        owner=request.user).select_related('owner').get(id=pk)
    comment = Comments.objects.filter(blog=blog).select_related('owner')
    form = CommentForm()
    context = {'blog': blog, 'comments': comment, 'form': form}

    if request.method == 'POST':
        extra_fields = Comments(owner=request.user, blog=blog)
        form = CommentForm(request.POST, instance=extra_fields)
        if form.is_valid():
            form.save()
            return redirect('detail-userblog')
    return render(request, 'blog_app/viewuserblog.html', context)


@login_required
def postblog(request):
    if request.method == 'GET':
        form = CreateForm()
        context = {'form': form}
        return render(request, 'blog_app/createblog.html', context)

    elif request.method == 'POST':
        form = CreateForm(request.POST)
        extra_fields = BlogPost(owner=request.user)
        form = CreateForm(request.POST, instance=extra_fields)
        if form.is_valid():
            extra_fields.save()
            return redirect('home')


@login_required
def deleteblog(request, pk):
    blog = BlogPost.objects.get(id=pk)
    context = {'blog': blog}
    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    return render(request, 'blog_app/deleteblog.html', context)


def listblogs(request):
    blogs = BlogPost.objects.select_related('owner').all()
    search_input = request.GET.get('search-area') or ''
    if search_input:
        blogs = blogs.filter(title__icontains=search_input)
    context = {'blogs': blogs, 'search_input': search_input}
    return render(request, 'blog_app/home.html', context)


def detailblogs(request, pk):
    blog = BlogPost.objects.prefetch_related('owner').get(id=pk)
    comment = Comments.objects.filter(blog=blog).select_related('owner')
    if request.method == 'GET':
        form = CommentForm()
        context = {'blog': blog, 'form': form, 'comments': comment}

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        extra_fields = Comments(owner=request.user, blog=blog)
        form = CommentForm(request.POST, instance=extra_fields)
        if form.is_valid():
            form.save()
            return redirect('detail-blog', pk=pk)
    return render(request, 'blog_app/viewblog.html', context)


def deletecomment(request, b, pk):
    comment = Comments.objects.get(id=pk)
    context = {'comment': comment}

    if request.method == 'POST':
        comment.delete()
        return redirect('detail-blog', pk=b)
    return render(request, 'blog_app/deletecomment.html', context)
