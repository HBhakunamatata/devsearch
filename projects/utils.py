from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def getPageRange(pageNo, num_pages):
    """生成分页范围"""
    # avoid the boundary of page_range is invalid 
    startIndex = int(pageNo) - 4
    if startIndex < 1:
        startIndex = 1
    endIndex = int(pageNo) + 5
    if endIndex > num_pages:
        endIndex = num_pages

    return range(startIndex, endIndex + 1)


def paginateProjects(request, projects, pageSize):
    """分页项目信息"""
    pageNo = request.GET.get('pageNo')
    paginator = Paginator(projects, pageSize)

    # 处理空页和没有页面编号的问题
    try:
        projects = paginator.page(pageNo)
    except PageNotAnInteger:
        pageNo = 1
    except EmptyPage:
        pageNo = paginator.num_pages
    
    projects = paginator.page(pageNo)
    # 定制化分页窗口范围
    page_range = getPageRange(pageNo, paginator.num_pages)

    return page_range, projects


def searchProjects(request):
    """条件查询项目列表"""
    search_params = ""
    if request.GET.get('search_query'):
        search_params = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_params)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_params) | 
        Q(description__icontains=search_params) |
        Q(owner__name__icontains=search_params) |
        Q(tags__in=tags)
    )

    return search_params, projects