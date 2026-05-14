from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from .utils import get_page_obj, filter_published_posts, annotate_posts_with_comments

User = get_user_model()


def index(request):
    template = 'blog/index.html'
    posts = Post.objects.select_related('author', 'category', 'location')
    posts = filter_published_posts(posts)
    posts = annotate_posts_with_comments(posts)
    page_obj = get_page_obj(request, posts)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        qs = Post.objects.filter(id=post_id)
        qs = filter_published_posts(qs)
        post = get_object_or_404(qs)

    comments = post.comments.all()
    form = CommentForm()
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = category.posts.all()
    posts = filter_published_posts(posts)
    posts = annotate_posts_with_comments(posts)
    page_obj = get_page_obj(request, posts)
    context = {'category': category, 'page_obj': page_obj}
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    author = get_object_or_404(User, username=username)

    posts = author.posts.all()
    if request.user != author:
        posts = filter_published_posts(posts)
    posts = annotate_posts_with_comments(posts)
    page_obj = get_page_obj(request, posts)

    context = {'profile': author, 'page_obj': page_obj}
    return render(request, template, context)


@login_required
def create_post(request):
    template = 'blog/create.html'
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', username=request.user.username)
    context = {'form': form}
    return render(request, template, context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    template = 'blog/create.html'
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    context = {'form': form}
    return render(request, template, context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    template = 'blog/delete.html'
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', username=request.user.username)
    context = {'post': post}
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    # Проверяем, что пост опубликован
    post = get_object_or_404(
        Post,
        id=post_id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id=post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    template = 'blog/comment.html'
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)
    context = {'form': form, 'comment': comment}
    return render(request, template, context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect('blog:post_detail', post_id=post_id)
    if request.method == 'POST':
        comment.delete()
    return redirect('blog:post_detail', post_id=post_id)
