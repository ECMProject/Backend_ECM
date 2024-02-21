from django.contrib import admin
from eseme.models import Zone, Level, Period, Course, Schedule, Season, Mode, Member, Student

# Register your models here.
admin.site.register(Zone)
admin.site.register(Level)
admin.site.register(Course)
admin.site.register(Schedule)
admin.site.register(Season)
admin.site.register(Mode)
admin.site.register(Member)
admin.site.register(Student)
admin.site.register(Period)

