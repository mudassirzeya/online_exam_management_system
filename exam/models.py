from django.db import models
from users.models import AdminUser, UserProfile
from datetime import datetime

# Create your models here.


class Examination(models.Model):
    company = models.ForeignKey(
        AdminUser, null=True, blank=True, on_delete=models.CASCADE
    )
    exam_name = models.CharField(max_length=100, null=True, blank=True)
    exam_start_time = models.DateTimeField(
        auto_now_add=False, blank=True, null=True, default=datetime.now())
    exam_end_time = models.DateTimeField(
        auto_now_add=False, blank=True, null=True, default=datetime.now())


class Section(models.Model):
    exam_associated = models.ForeignKey(
        Examination, null=True, blank=True, on_delete=models.CASCADE
    )
    section = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.section


class Add_Question_Link(models.Model):
    exam_associated = models.ForeignKey(
        Examination, null=True, blank=True, on_delete=models.CASCADE
    )
    link = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.link


class Add_Student_Link(models.Model):
    exam_associated = models.ForeignKey(
        Examination, null=True, blank=True, on_delete=models.CASCADE
    )
    link = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.link


class Question(models.Model):
    associated_exam = models.ForeignKey(
        Examination, null=True, blank=True, on_delete=models.CASCADE
    )
    section_dropdown = models.ForeignKey(
        Section, null=True, on_delete=models.CASCADE)
    question_text = models.TextField(null=True, blank=True)
    question_image = models.TextField(null=True, blank=True)
    option_a = models.TextField(null=True, blank=True)
    option_a_image = models.TextField(null=True, blank=True)
    option_b = models.TextField(null=True, blank=True)
    option_b_image = models.TextField(null=True, blank=True)
    option_c = models.TextField(null=True, blank=True)
    option_c_image = models.TextField(null=True, blank=True)
    option_d = models.TextField(null=True, blank=True)
    option_d_image = models.TextField(null=True, blank=True)
    correct_answer = models.TextField(null=True, blank=True)
    marks = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return str(self.section_dropdown) + "-" + str(self.id)


class Add_Student(models.Model):
    user = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.CASCADE
    )
    associated_exam = models.ForeignKey(
        Examination, null=True, blank=True, on_delete=models.CASCADE
    )


class Response_Table(models.Model):
    user = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.CASCADE
    )
    exam_associated = models.ForeignKey(
        Examination, null=True, blank=True, on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question, null=True, blank=True, on_delete=models.CASCADE
    )
    answer = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.user)


class Student_Result(models.Model):
    user = models.ForeignKey(
        UserProfile, null=True, blank=True, on_delete=models.CASCADE
    )
    exam_associated = models.ForeignKey(
        Examination, null=True, blank=True, on_delete=models.CASCADE
    )
    marks = models.PositiveBigIntegerField(null=True, blank=True, default=0)
