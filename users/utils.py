from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage


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


def paginateProfiles(request, profiles, pageSize):
    """分页项目信息"""
    pageNo = request.GET.get('pageNo')
    paginator = Paginator(profiles, pageSize)

    # 处理空页和没有页面编号的问题
    try:
        profiles = paginator.page(pageNo)
    except PageNotAnInteger:
        pageNo = 1
    except EmptyPage:
        pageNo = paginator.num_pages
    
    profiles = paginator.page(pageNo)
    # 定制化分页窗口范围
    page_range = getPageRange(pageNo, paginator.num_pages)

    return page_range, profiles



def searchProfiles(request):
    """条件查询用户信息"""
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    skills = Skill.objects.filter(name__icontains=search_query)
        
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
    )

    return search_query, profiles

