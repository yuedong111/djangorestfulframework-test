from django.shortcuts import render
from .models import School, Student, StudentSorce
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import SchoolSerializer, StudentSerializer, StudentSorceSerializer, AccountSerializer
from rest_framework import generics
from rest_framework import status
from django.contrib.auth.models import User


class AllSchoolView(APIView):

    def get(self, request):
        schools = School.objects.all()
        # many表示返回一个list， 如果不设置，则返回一个
        schools_serializer = SchoolSerializer(schools, many=True)
        return Response(schools_serializer.data)


class StudentList(generics.ListCreateAPIView):
    #queryset是默认返回的列表
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # 创建一个student
    def create(self, request, *args, **kwargs):
        #post 方法
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetail(generics.RetrieveUpdateAPIView):
    serializer_class = StudentSerializer
    # queryset = Student.objects.all()
    lookup_field = 'name'

    # 得到一个数据集
    def get_queryset(self):
        return Student.objects.filter(name=self.kwargs['name'])

    # get方法返回一个student
    def get(self, request, *args, **kwargs):
        # 获取url中的参数
        # http://127.0.0.1:8000/api/students/aaa/?test=123
        # 取test的值
        queryset = self.get_queryset()
        serializer = StudentSerializer(queryset, many=True)
        return Response({
            'data': serializer.data,
            'score': StudentSorceSerializer(StudentSorce.objects.all(), many=True).data
        })

    # 更新某一个学生的信息
    def update(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        serializer = StudentSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(generics.CreateAPIView):
    #继承generics.CreateAPIView只允许http的post方法
    serializer_class = AccountSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)