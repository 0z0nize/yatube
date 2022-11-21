from django.conf import settings
from django.core.paginator import Paginator


def pager(page_n, queryset):
    paginator = Paginator(queryset, settings.POST_IN_PAGE)
    return paginator.get_page(page_n)
