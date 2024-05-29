from django.shortcuts import render, redirect
from .models import Profile, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib.auth.decorators import login_required
from .utils import searchProfiles, paginateProfiles

# Create your views here.


def profiles(request):
    """所有用户信息"""
    search_query, profiles = searchProfiles(request)
    page_range, profiles = paginateProfiles(request, profiles, pageSize=4)

    context = {'profiles': profiles, 'search_query': search_query, 'page_range': page_range}
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    user_profile = Profile.objects.get(id=pk)

    top_skills = user_profile.skill_set.exclude(description__exact="")
    other_skills = user_profile.skill_set.filter(description="")

    context = {'user_profile': user_profile, 'top_skills': top_skills, 'other_skills': other_skills}
    return render(request, 'users/user-profile.html', context)


def loginUser(request):
    """
    用户登陆页面: 
        0.已经登陆的用户直接防御性跳转至profiles 
        1.验证用户是否存在以及校验信息是否正确
        2.用户登陆验证 验证成功 重定向到个人主页
    """
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User named ' + username + ' is not exist!')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            messages.info(request, 'Hello ' + username)
            # 生成sessionid，保持登陆状态
            login(request, user=user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')
        else:
            messages.info(request, "Sorry, username OR password is incorrect.")

    return render(request, 'users/login-register.html')


@login_required(login_url='login')
def logoutUser(request):
    """用户登出"""
    logout(request)
    messages.info(request, "You have just logout.")
    return redirect('login')


def registerUser(request):
    """注册用户(保证用户名称小写，并且完成用户登陆，使其在线状态)"""
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        # 使用提交数据形成表单数据进行校验
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # m2m延时提交数据，保证用户名都是小写
            user_data = form.save(commit=False)
            user_data.username = user_data.username.lower()
            user_data.save()

            messages.success(request, 'User ' + user_data.username + ' has been created successfully.')

            # 注册后让用户登陆，并重定向至account-edit
            login(request, user_data)
            return redirect('account-edit')

        else:
            # form参数校验失败，打印错误信息重新刷新页面
            messages.error(request, "An error has occurred during registration")
    
    context = {'page': page, 'form': form}

    return render(request, 'users/login-register.html', context)


@login_required(login_url='login')
def userAccount(request):
    """用户账号"""
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    """修改账号信息"""
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)



@login_required(login_url='login')
def createSkill(request):
    """为用户创建技能"""
    # form = profile.skill_set
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            profile = request.user.profile
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect('account')
        else:
            messages.error(request, "An error has occurred during creating")

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


def updateSkill(request, pk):
    """更新用户账号的技能"""
    profile = request.user.profile
    selected_skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=selected_skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=selected_skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect('account')
        else:
            messages.error(request, "An error has occurred during updating")

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    """删除用户的技能"""
    object = request.user.profile.skill_set.get(id=pk)
    if request.method == 'POST':
        object.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect('account')
    context = {'obejct': object}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    """获取以登陆用户为接收者的消息和未阅读数量"""
    profile = request.user.profile
    received_messages = profile.messages.all()
    unreadCount = received_messages.filter(is_read=False).count()
    context = {'received_messages': received_messages, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    """获取指定消息内容，"""
    # 防止访问其他用户的信息
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read= True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)



def createMessage(request, pk):
    """创建消息"""
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    # 获取发送者信息，未登陆用户创建信息设置为None
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            
            message.save()

            messages.success(request, "Message was sent successfully")
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)