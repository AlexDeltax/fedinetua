from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def items_pagination(items, request, count=6):
    page = request.GET.get("page")
    paginator = Paginator(items, count)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return items
