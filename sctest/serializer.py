from rest_framework import serializers
from .models import Student, StudentSorce
from django.contrib.auth.models import User
import re


class SchoolSerializer(serializers.Serializer):
    #定义要返回的字段
    name = serializers.CharField()
    location = serializers.CharField()


class StudentSorceSerializer(serializers.ModelSerializer):
    avg = serializers.SerializerMethodField('get_avg_sorce')

    class Meta:
        model = StudentSorce
        fields = ('math', 'english', 'chiness', 'avg')
    # 自定义方法构造的字段(计算成绩的平均值)
    def get_avg_sorce(self, obj):
        return (obj.math + obj.english + obj.chiness) / 3.0


class StudentSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField('get_student_sorce')

    class Meta:
        model = Student
        fields = ('id', 'student_id', 'name', 'age', 'score')

    # 使用学号查出该学生的成绩
    def get_student_sorce(self, obj):
        return StudentSorceSerializer(StudentSorce.objects.filter(student_id=obj.student_id), many=True).data


class AccountFrom(object):
    def __init__(self, email, username, password, repeat_password):
        self.email = email
        self.username = username
        self.password = password
        self.repeat_password = repeat_password


class AccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def create(self, validated_data):
        User.objects.create_user(username=validated_data.get('username'),
                                 email=validated_data.get('email'),
                                 password=validated_data.get('password'))
        return AccountFrom(username=validated_data.get('username'),
                           email=validated_data.get('email'),
                           password=validated_data.get('password'),
                           repeat_password=validated_data.get('repeat_password'))

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        # User.objects.update()
        instance.save()
        return instance

    def validate_email(self, value):
        try:
            result_email = User.objects.get(email=value)
        except User.DoesNotExist:
            return value
        raise serializers.ValidationError('该邮箱已注册')

    def validate_password(self, value):
        self.password = value
        if re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$', value):
            return value
        else:
            raise serializers.ValidationError('密码必须由6-20个字母和数字组成')

    def validate_repeat_password(self, value):
        self.repeat_password = value
        if self.password and value and self.password != value:
            raise serializers.ValidationError("两次输入的值不相同")
        return value

    def validate_username(self, value):
        if re.match("^[A-Za-z][A-Za-z0-9_.]*$", value):
            return value
        else:
            raise serializers.ValidationError("用户名只能有数字字母下划线组成")