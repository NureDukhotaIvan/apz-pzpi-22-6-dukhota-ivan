from rest_framework import serializers
from .models import User, Student, Parent, Teacher



class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'role', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        if validated_data['role'] == 'student':
            Student.objects.create(user=user)
        elif validated_data['role'] == 'teacher':
            Teacher.objects.create(user=user)
        elif validated_data['role'] == 'parent':
            Parent.objects.create(user=user)
        return user


class StudentSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth', 'student_class', 'access_card_number']



class ParentSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')
    student = StudentSerializer()

    class Meta:
        model = Parent
        fields = ['id', 'email', 'first_name', 'last_name', 'student']



class TeacherSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Teacher
        fields = ['id', 'email', 'first_name', 'last_name', 'position', 'access_card_number']



class UserSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(source='student', read_only=True)
    parent_details = ParentSerializer(source='parent', read_only=True)
    teacher_details = TeacherSerializer(source='teacher', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'student_details', 'parent_details', 'teacher_details']


class BaseProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email уже зарегистрирован.")
        return value

    def create_user(self, validated_data, role):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user = User.objects.create_user(email=email, password=password, role=role)
        return user


class StudentCreateSerializer(BaseProfileSerializer):
    class Meta:
        model = Student
        fields = ['email', 'password', 'first_name', 'last_name', 'date_of_birth', 'student_class', 'access_card_number']

    def create(self, validated_data):
        user = self.create_user(validated_data, 'student')
        return Student.objects.create(user=user, **validated_data)


class ParentCreateSerializer(BaseProfileSerializer):
    student_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Parent
        fields = ['email', 'password', 'first_name', 'last_name', 'student_id']

    def create(self, validated_data):
        student_id = validated_data.pop('student_id')
        user = self.create_user(validated_data, 'parent')
        return Parent.objects.create(user=user, student_id=student_id, **validated_data)


class TeacherCreateSerializer(BaseProfileSerializer):
    class Meta:
        model = Teacher
        fields = ['email', 'password', 'first_name', 'last_name', 'position', 'access_card_number']

    def create(self, validated_data):
        user = self.create_user(validated_data, 'teacher')
        return Teacher.objects.create(user=user, **validated_data)
