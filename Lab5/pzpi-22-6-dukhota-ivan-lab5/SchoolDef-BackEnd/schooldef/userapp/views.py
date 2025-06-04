from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import User, Student, Parent, Teacher
from .serializers import *
from .permissions import IsAdmin
from .mixins import ProfileDestroyMixin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        role = instance.role

        if role == 'student' and hasattr(instance, 'student'):
            Parent.objects.filter(student=instance.student).update(student=None)
            instance.student.delete()
        elif role == 'parent' and hasattr(instance, 'parent'):
            instance.parent.delete()
        elif role == 'teacher' and hasattr(instance, 'teacher'):
            instance.teacher.delete()

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def create_user(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'user created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class StudentViewSet(ProfileDestroyMixin, viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdmin]

class ParentViewSet(ProfileDestroyMixin, viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAdmin]

class TeacherViewSet(ProfileDestroyMixin, viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin]

class StudentCreateViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class ParentCreateViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class TeacherCreateViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

