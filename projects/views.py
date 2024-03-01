from django.shortcuts import render, redirect
from .models import Project
from .form import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginateProjects
from django.contrib import messages


# Create your views here.

def projects(request):
    # return HttpResponse('Here are my projects.')
    search_query, projects = searchProjects(request)
    page_range, projects = paginateProjects(request, projects, pageSize=6)
    
    context = {'projects': projects, 'search_query': search_query, 'page_range': page_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    
    # TODO 如果没找到怎么处理？？

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # save the review data
            review = form.save(commit=False)
            review.project = projectObj
            review.owner = request.user.profile
            review.save()
            messages.success(request, "Review has been added successfully")

            # recount the vote result
            projectObj.recountVoteResult

            # refresh the page
            return redirect('project', projectObj.id)
        else:
            messages.error(request, 'some review data is valid')
            
    context = {'project': projectObj, 'form': form}

    return render(request, 'projects/single-project.html', context)


@login_required
def project_create(request):
    """请求项目创建页面"""
    profile = request.user.profile
    project_form = ProjectForm()

    # 请求表达页面使用get，数据提交使用post
    if request.method == 'POST':
        # print(request.POST)
        project_form = ProjectForm(request.POST, request.FILES)
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': project_form}
    return render(request, 'projects/project_form.html', context)


@login_required
def project_update(request, pk):
    """修改项目信息接口"""
    profile = request.user.profile
    selected_project = profile.project_set.get(id=pk)
    project_form = ProjectForm(instance=selected_project)
    
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES, instance=selected_project)
        if project_form.is_valid():
            project_form.save()
            return redirect('projects')
    
    context = {'form': project_form}
    return render(request, 'projects/project_form.html', context)


@login_required
def project_delete(request, pk):
    """删除项目信息接口"""
    profile = request.user.profile
    selected_project = profile.project_set.get(id=pk)
    
    if request.method == 'POST':
        selected_project.delete()
        return redirect('projects')
    
    context = {'obejct': selected_project}
    return render(request, 'delete_template.html', context)