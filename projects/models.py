from django.db import models
import uuid

from users.models import Profile

# Create your models here.

class Project(models.Model):
    """项目模型"""
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True)
    vote_ratio = models.IntegerField(default=0, null=True)
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                          primary_key=True, editable=True)
    
    
    def __str__(self):
        return self.title
    

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']

    
    @property
    def recountVoteResult(self):
        """重新计算并存储投票结果"""
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = ( upVotes / totalVotes ) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()
    

    @property
    def reviewers(self):
        """获取所有已评价用户"""
        query_set = self.review_set.all().values_list('owner__id', flat=True)
        return query_set



class Review(models.Model):
    """项目评价模型，多对一关系：多个评论对应一个项目"""
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)

    def __str__(self):
        return self.value
    
    class Meta:
        # 保证每个用户不会给同一个项目重复评价
        unique_together = [['owner', 'project']]



class Tag(models.Model):
    """项目描述标签"""
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True),
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)

    def __str__(self):
        return self.name