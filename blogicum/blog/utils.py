from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Count
from .models import Post


def get_page_obj(request, queryset, per_page=10):
    """Возвращает объект пагинации"""
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def filter_published_posts(queryset):
    """Фильтрует опубликованные посты"""
    now = timezone.now()
    return queryset.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=now
    )


def annotate_posts_with_comments(queryset):
    """Аннотирует посты количеством комментариев"""
    return queryset.annotate(comment_count=Count('comments')).order_by('-pub_date')