from rest_framework import serializers
from .models import Season, Student, Member, Course

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'
        depth = 1

class StudentSerializer(serializers.ModelSerializer):
    stud_member_id = serializers.IntegerField(write_only=True)
    stud_season_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Student
        fields = ['stud_id', 'stud_member', 'stud_season', 'stud_member_id', 'stud_season_id', 'seas_final',
                  'seas_ses01','seas_ses02','seas_ses03','seas_ses04','seas_ses05','seas_ses06','seas_ses07',
                  'seas_ses08','seas_ses09','seas_ses10','seas_ses11','seas_ses12']
        depth = 2
        
class StudentPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        depth = 2
        
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        depth = 2
        
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
