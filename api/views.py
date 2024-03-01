from .serializers import ProjectSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from projects.models import Project, Review
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    """创建一个review,并更新project的统计数据"""
    profile = request.user.profile
    project = Project.objects.get(id=pk)

    data = request.data

    if data:
        vote_value = data['value']
        review, created = Review.objects.get_or_create(owner=profile, project=project)
        review.value = vote_value
        review.save()

        project.recountVoteResult

    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)