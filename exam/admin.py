from django.contrib import admin
from .models import (
    Examination,
    Section,
    Question,
    Add_Question_Link,
    Add_Student_Link,
    Add_Student,
    Response_Table,
    Student_Result,
)

# Register your models here.

admin.site.register(Examination)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Add_Question_Link)
admin.site.register(Add_Student_Link)
admin.site.register(Add_Student)
admin.site.register(Response_Table)
admin.site.register(Student_Result)
