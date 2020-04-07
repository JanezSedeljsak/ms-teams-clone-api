from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth.models import User
from msclone.tasks.models import Task, SubTask, TaskCollaborators
from rest_framework.permissions import AllowAny
from msclone.tasks.serializers import TaskSerializer, TasksViewSerializer, SubTaskSerializer, TaskCollaboratorSerializer
from django.core import serializers
from django.db.models import Q
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def get_task(request, task_id):

    result = {}

    if not Task.objects.filter(id=task_id).exists():
        return Response({'error': 'The task you are searching for does not exist'}, status=HTTP_404_NOT_FOUND) 

    task = Task.objects.get(id=task_id)

    if request.method == 'GET':   
        task_serializer = TaskSerializer(task)

        result['task'] = task_serializer.data

        if SubTask.objects.filter(task_id=task_id).exists(): 
            subtasks = SubTask.objects.filter(task_id=task_id)
            subtask_serializer = SubTaskSerializer(subtasks, many=True)

            result['subtasks'] = subtask_serializer.data

        if TaskCollaborators.objects.filter(task_id=task_id).exists():
            collaborators =  TaskCollaborators.objects.filter(task_id=task_id)
            collaborators_serializer = TaskCollaboratorSerializer(collaborators, many=True)

            result['collaborators'] = collaborators_serializer.data


    elif request.method == 'PUT':
        task_serializer = TaskSerializer(task, data=request.data)
        if task_serializer.is_valid():
            task_serializer.save()
            result['success'] = True
        else:
            return Response({'error': task_serializer.errors}, status=HTTP_400_BAD_REQUEST) 

    elif request.method == 'DELETE':
        operation = task.delete()
        if operation:
            result['success'] = True
        else:
            result['success'] = False


    return Response(result, status=HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def create_task(request):
    task_skeleton = Task(user=request.user)
    task_serializer = TaskSerializer(task_skeleton, data=request.data)
    if task_serializer.is_valid():
        task_serializer.save()
        return Response(task_serializer.data, status=HTTP_201_CREATED)
    return Response(task_serializer.errors, status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def get_all_tasks(request):

    tasks = Task.objects.all()
    serializer = TasksViewSerializer(tasks, many=True)

    return Response(serializer.data, status=HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_sub_task(request, task_id, subtask_id):

    if not SubTask.objects.filter(Q(id=subtask_id) & Q(task_id=task_id)).exists():
        return Response({'error': 'The sub task you are searching for does not exist'}, status=HTTP_404_NOT_FOUND) 
        
    subtask = SubTask.objects.get(id=subtask_id)
    subtask_serializer = SubTaskSerializer(subtask)
    

    return Response(subtask_serializer.data, status=HTTP_200_OK)



        

    