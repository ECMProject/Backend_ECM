from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Student, Member, Course, Season, Zone
from .serializers import StudentSerializer, MemberSerializer, CourseSerializer, SeasonSerializer, StudentPutSerializer
from django.db.models import Q, F

# ----------------------- STUDENT VIEWS ----------------------- #
class StudentSeasonsAPIView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Student.objects.filter(stud_member__memb_id=user_id)

class StudentCoursesAPIView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        
        queryset = Student.objects.filter(stud_member__memb_id=user_id)
        queryset = queryset.filter(seas_final__gt = 13)
        queryset = queryset.order_by('stud_season__seas_course__cour_level')
        return queryset

    
class StudentListAPIView(generics.ListAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    
class TeacherListView(generics.ListAPIView):
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        current_teacher = self.kwargs.get('teacher')
        seasons_of_current_teacher = Season.objects.filter(seas_teacher__memb_id=current_teacher)
        students = Student.objects.filter(stud_season__in=seasons_of_current_teacher)
        return students

class StudentUpdateView(generics.UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentPutSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def get(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

class StudentCreateAPIView(generics.CreateAPIView):
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        return Student.objects.all()
    
    def create(self, request):
        data_new = request.data

        data_new['stud_member_id'] = data_new.get('stud_id')
        data_new['stud_season_id'] = data_new.get('seas_id')
        
        serializer = self.get_serializer(data=data_new)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

# ----------------------- MEMBER VIEWS ----------------------- #
class MemberListAPIView(generics.ListAPIView):
    serializer_class = MemberSerializer
    
    def get_queryset(self):
        queryset = Member.objects.all()
        name = self.request.query_params.get('name', None)
        
        if name:
            queryset = queryset.filter(Q(memb_name__icontains=name) | Q(memb_surname__icontains=name))
        
        return queryset

class MemberCreateAPIView(generics.CreateAPIView):
    serializer_class = MemberSerializer

    def create(self, request):
        zone_name = request.data.pop('memb_zone', None)
        
        if zone_name is not None:
            try:
                zone = Zone.objects.get(zone_name=zone_name)
                request.data['memb_zone'] = zone.zone_id
            except Zone.DoesNotExist:
                return Response({"error": "Zone does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------- COURSE VIEWS ----------------------- #
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# ----------------------- SEASON VIEWS ----------------------- #
class SeasonListAPIView(generics.ListAPIView):
    serializer_class = SeasonSerializer
    
    def get_queryset(self):
        queryset = Season.objects.all()
        user_id = self.kwargs['user']
        
        queryset = queryset.filter(seas_period__peri_status=True)
        
        return queryset.exclude(student__stud_member=user_id)

class StudentCreateDeclarativaAPIView(generics.CreateAPIView):
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        cursos_data = request.data.get('cursos', [])
        member_id = request.data.get('member_id')

        for curso_data in cursos_data:
            seas_id = Season.objects.filter(seas_course=curso_data['cour_id']).values_list('seas_id', flat=True).first()
            if not seas_id:
                continue

            student_data = {
                'stud_season': seas_id,
                'stud_member': member_id,
                'seas_final': 17,
            }

            serializer = self.get_serializer(data=student_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        return Response(status=status.HTTP_201_CREATED)

# ----------------------- USER VIEWS ----------------------- #
class LoginAPIView(generics.ListAPIView):
    serializer_class = MemberSerializer
    
    def get_queryset(self):
        dni_param = self.kwargs.get('dni')
        if dni_param:
            queryset = Member.objects.filter(memb_dni=dni_param)
            if queryset.exists():
                return queryset
            else:
                raise NotFound("Member not found with the provided DNI.", status=status.HTTP_404_NOT_FOUND)
        else:
            raise NotFound("DNI parameter is missing in the URL.", status=400)

