from urllib import request
from django.shortcuts import redirect, render
from .models import (
    Add_Student,
    Add_Student_Link,
    Examination,
    Section,
    Question,
    Student_Result,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from users.models import AdminUser, UserProfile
from .models import Examination, Add_Question_Link, Question, Response_Table
from urllib.request import urlopen
from datetime import datetime
import json
from django.contrib import messages
import pytz
import time

from django.core.mail import EmailMultiAlternatives
from django.conf import settings


# Create your views here.

@login_required(login_url='login')
def admin_page(request):
    try:
        admin_user = AdminUser.objects.get(user=request.user)
    except Exception:
        admin_user = None
    if not admin_user:
        return JsonResponse({"msg": "You Dont have access to this page"})
    my_exam = Examination.objects.filter(company=admin_user)
    all_staff = UserProfile.objects.filter(
        company_assign=admin_user, user_type='staff')
    all_students = UserProfile.objects.filter(
        company_assign=admin_user, user_type='student')
    context = {"my_exam": my_exam, "total_staff": all_staff.count,
               "total_student": all_students.count()}
    return render(request, "admin_page.html", context)


@login_required(login_url='login')
def staff_page(request):
    userprofile = UserProfile.objects.get(user=request.user)
    company_assign = userprofile.company_assign
    allotted_exam = Examination.objects.filter(company=company_assign)
    context = {"company_assign": company_assign,
               "allotted_exam": allotted_exam}
    return render(request, "staff_page.html", context)


@login_required(login_url='login')
def staff_student_marksheet(request, pk):
    exam = Examination.objects.get(id=pk)
    student_marksheet = Student_Result.objects.filter(exam_associated=exam)
    context = {"student_marksheet": student_marksheet, "exam": exam}
    return render(request, "staff_students_marksheet.html", context)


def staff_each_student_marksheet(request, pk, id):
    user = User.objects.get(id=id)
    exam = Examination.objects.get(id=pk)
    userprofile = UserProfile.objects.get(user=user)
    questions = Question.objects.filter(associated_exam=exam)
    total_question = questions.count()
    student_response = Response_Table.objects.filter(
        user=userprofile, exam_associated=exam)

    st_response = {}
    for response in student_response:
        question_id = response.question.id
        actual_response = response.answer
        st_response[question_id] = actual_response
    # print(st_response)
    final = []
    for question in questions:
        temp = {}
        question_id = question.id
        answer = 'Not Attempted'
        try:
            json_answer = st_response[question_id]
            answer = json_answer
        except:
            pass

        temp['question'] = question
        temp['answer'] = answer
        final.append(temp)
    context = {"total_question": total_question, "final": final, "user": user}
    return render(request, 'staff_each_student_marksheet.html', context)


@login_required(login_url='login')
def student_home(request):
    UTC = pytz.utc
    userprofile = UserProfile.objects.get(user=request.user)
    exam_allotted = Add_Student.objects.filter(user=userprofile)
    current_time = datetime.now(UTC)
    context = {"exam_allotted": exam_allotted, "current_time": current_time}
    return render(request, "student_home.html", context)


@login_required(login_url='login')
def student_exam_page(request, pk):
    current_exam = Examination.objects.get(id=pk)
    userprofile = UserProfile.objects.get(user=request.user)
    questions = Question.objects.filter(associated_exam=current_exam)
    questions_count = questions.count()
    section = Section.objects.filter(exam_associated=current_exam)
    user_response_data = Response_Table.objects.filter(
        user=userprofile, exam_associated=current_exam
    )
    exam_end_time = current_exam.exam_end_time
    millisec = exam_end_time.timestamp() * 1000
    user_atempt = []
    for subject in section:
        this_sec_question = []
        myquestions = questions.filter(section_dropdown=subject)
        if len(myquestions) > 0:
            for each_qs in myquestions:
                user_response = user_response_data.filter(question=each_qs)
                answer = "no"
                if user_response:
                    answer = user_response[0].answer
                temp = {"question": each_qs, "answer": answer}
                this_sec_question.append(temp)
        user_atempt.append([subject, this_sec_question])
    # print("attemp", user_atempt)
    context = {
        "current_exam": current_exam,
        "questions_count": questions_count,
        "user_atempt": user_atempt,
        "millisec": millisec
    }
    return render(request, "student_exam_page.html", context)


@login_required(login_url='login')
def create_exam(request):
    loggedin_user = AdminUser.objects.get(user=request.user)
    if request.method == "POST":
        exam_name = request.POST.get("exam_name")
        Examination.objects.create(
            company=loggedin_user,
            exam_name=exam_name,
        )
        return redirect("admin_page")
    context = {}
    return render(request, "admin_page.html", context)


@login_required(login_url='login')
def each_exam_page(request, pk):
    exam = Examination.objects.get(id=pk)
    students = Add_Student.objects.filter(associated_exam=exam)
    questions = Question.objects.filter(associated_exam=exam)
    total_student = students.count()
    if request.method == "POST":
        start_exam = request.POST.get("start_exam")
        end_exam = request.POST.get("end_exam")
        exam.exam_start_time = start_exam
        exam.exam_end_time = end_exam
        exam.save()
    exam_id = exam.id
    context = {"exam": exam, "exam_id": exam_id,
               "total_student": total_student,
               "total_questions": questions.count()}
    return render(request, "each_exam_page.html", context)


@login_required(login_url='login')
def question_upload(request, pk):
    exam_associated = Examination.objects.get(id=pk)
    if request.method == "POST":
        question_link = request.POST.get("question_link")
        input = request.POST.get("confirm")
        if input == "confirm":
            try:
                existing_question_link = Add_Question_Link.objects.filter(
                    exam_associated=exam_associated
                )
            except:
                existing_question_link = None
            if existing_question_link is not None:
                existing_question_link.delete()
            Add_Question_Link.objects.create(
                exam_associated=exam_associated,
                link=question_link,
            )
            url = question_link
            response = urlopen(url)
            data_json = json.loads(response.read())
            all_question = Question.objects.filter(
                associated_exam=exam_associated)
            if all_question:
                all_question.delete()
            all_section = Section.objects.filter(
                exam_associated=exam_associated)
            if all_section:
                all_section.delete()
            for data in data_json:
                sections_data = data[0]
                add_section = Section.objects.create(
                    exam_associated=exam_associated, section=sections_data
                )
                section_query = Section.objects.get(id=add_section.id)
                all_section_question = data[1]
                for questions_data in all_section_question:
                    Question.objects.create(
                        associated_exam=exam_associated,
                        section_dropdown=section_query,
                        question_text=questions_data["Question_Text"],
                        question_image=questions_data["Question_image"],
                        option_a=questions_data["A"],
                        option_a_image=questions_data["A_image"],
                        option_b=questions_data["B"],
                        option_b_image=questions_data["B_image"],
                        option_c=questions_data["C"],
                        option_c_image=questions_data["C_image"],
                        option_d=questions_data["D"],
                        option_d_image=questions_data["D_image"],
                        correct_answer=questions_data["Correct_Answer"],
                        marks=questions_data["Marks"],
                    )
            return redirect("exam_page", pk=pk)
        else:
            messages.info(request, "You Entered Wrong Input")
    return render(request, "each_exam_page.html")


@login_required(login_url='login')
def add_students(request, pk):
    exam_associated = Examination.objects.get(id=pk)
    company = AdminUser.objects.get(user=request.user)
    if request.method == "POST":
        student_link = request.POST.get("link")
        input = request.POST.get("student_confirm")
        if input == "confirm":
            try:
                existing_students_link = Add_Student_Link.objects.filter(
                    exam_associated=exam_associated
                )
            except:
                existing_students_link = None
            if existing_students_link is not None:
                existing_students_link.delete()
            Add_Student_Link.objects.create(
                exam_associated=exam_associated,
                link=student_link,
            )
            all_users = Add_Student.objects.filter(
                associated_exam=exam_associated)
            for user_item in all_users:
                user = User.objects.get(id=user_item.user.user.id)
                user.delete()
                print("user: ", user)
            url = student_link
            response = urlopen(url)
            data_json = json.loads(response.read())
            for data in data_json:
                new_user, created = User.objects.get_or_create(
                    username=data["Email"],
                )
                new_user.set_password(str(data["Registration"]))
                new_user.email = data["Email"]
                new_user.first_name = data["Name"]
                new_user.save()
                user_profile, created = UserProfile.objects.get_or_create(
                    user=new_user,
                )
                user_profile.company_assign = company
                user_profile.user_type = "student"
                user_profile.save()
                Add_Student.objects.get_or_create(
                    user=user_profile,
                    associated_exam=exam_associated,
                )
                Student_Result.objects.get_or_create(
                    user=user_profile,
                    exam_associated=exam_associated,
                )

                text_content = f"Your Username & Password for login in exam portal : Email: {data['Email']} Password: {str(data['Registration'])}"
                # Create the email object
                email_message = EmailMultiAlternatives(
                    'Password For Exam Portal',              # Subject
                    text_content,         # Body (plain text)
                    settings.EMAIL_HOST_USER,  # From email
                    [data["Email"]],              # To email
                )
                # Send the email
                email_message.send()
            return redirect("exam_page", pk=pk)
        else:
            messages.info(request, "You Entered Wrong Input")
    context = {}
    return render(request, "each_exam_page.html", context)


@login_required(login_url='login')
def mark_answer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("data", data)
        user_answers_data = data["data_obj"]
        current_exam = Examination.objects.get(
            id=int(user_answers_data[0]["exam_id"]))
        question_id = int(user_answers_data[0]["question"])
        question = Question.objects.get(id=question_id)
        user_data = UserProfile.objects.get(user=request.user)
        user_response_data = Response_Table.objects.filter(
            user=user_data, question=question, exam_associated=current_exam
        ).first()
        if user_response_data:
            user_response_data.delete()
            if question.correct_answer == user_response_data.answer:
                student_report = Student_Result.objects.get(
                    user=user_data, exam_associated=current_exam
                )
                student_report.marks -= int(question.marks)
                student_report.save()
            Response_Table.objects.create(
                user=user_data,
                exam_associated=current_exam,
                question=question,
                answer=user_answers_data[0]["user_answer"],
            )
            if question.correct_answer == user_answers_data[0]["user_answer"]:
                student_report = Student_Result.objects.get(
                    user=user_data, exam_associated=current_exam
                )
                student_report.marks += int(question.marks)
                student_report.save()
        else:
            Response_Table.objects.create(
                user=user_data,
                exam_associated=current_exam,
                question=question,
                answer=user_answers_data[0]["user_answer"],
            )
            if question.correct_answer == user_answers_data[0]["user_answer"]:
                student_report = Student_Result.objects.get(
                    user=user_data, exam_associated=current_exam
                )
                student_report.marks += int(question.marks)
                student_report.save()

        print("data: ", user_answers_data)
        time.sleep(1)
        return JsonResponse({"msg": "success"})
    context = {}
    return render(request, "student_exam_page.html", context)


@login_required(login_url='login')
def clear_answer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        clear_data = data["data_obj"]
        print("clear", clear_data)
        question_id = clear_data[0]["question"]
        current_exam = Examination.objects.get(id=clear_data[0]["exam_id"])
        question = Question.objects.get(id=question_id)
        user_data = UserProfile.objects.get(user=request.user)
        user_response_data = Response_Table.objects.filter(
            user=user_data, question=question, exam_associated=current_exam
        ).first()
        if user_response_data:
            user_response_data.delete()
            if question.correct_answer == user_response_data.answer:
                student_report = Student_Result.objects.get(
                    user=user_data, exam_associated=current_exam
                )
                student_report.marks -= int(question.marks)
                student_report.save()
            time.sleep(1)
            return JsonResponse({"msg": "success"})
    return render(request, "student_exam_page.html")


@login_required(login_url='login')
def student_response_page(request, pk):
    exam = Examination.objects.get(id=pk)
    questions = Question.objects.filter(associated_exam=exam)
    user_data = Add_Student.objects.filter(associated_exam=exam)
    # userprofile = UserProfile.objects.filter(id=user_data.user.id)
    user_response_data = Response_Table.objects.filter(exam_associated=exam)
    final_data = []
    temp_question = ["question"]
    temp_section = ["section"]
    temp_question_image = ["question_image"]
    for each_question in questions:
        question_text = each_question.question_text
        question_image = each_question.question_image
        question_section = each_question.section_dropdown
        temp_question.append(question_text)
        temp_section.append((question_section))
        temp_question_image.append(question_image)
    final_data.append(temp_section)
    final_data.append(temp_question)
    final_data.append(temp_question_image)
    for each_user in user_data:
        temp = [each_user.user.user.first_name]
        for qst in questions:
            final = ""
            user_response = user_response_data.filter(
                user=each_user.user, question=qst)
            if user_response:
                final = user_response[0].answer
            temp.append(final)
        final_data.append(temp)
    context = {
        "exam": exam,
        "final_data": final_data,
    }
    return render(request, "student_response_page.html", context)


@login_required(login_url='login')
def students_of_this_exam(request, pk):
    exam = Examination.objects.get(id=pk)
    students = Add_Student.objects.filter(associated_exam=exam)
    context = {"students": students, "exam": exam}
    return render(request, "added_student.html", context)


@login_required(login_url='login')
def questions_of_this_exam(request, pk):
    exam = Examination.objects.get(id=pk)
    questions = Question.objects.filter(associated_exam=exam)
    context = {"questions": questions, "exam": exam}
    return render(request, "added_question.html", context)


@login_required(login_url='login')
def student_marksheet(request, pk):
    exam = Examination.objects.get(id=pk)
    student_marksheet = Student_Result.objects.filter(exam_associated=exam)
    context = {"exam": exam, "student_marksheet": student_marksheet}
    return render(request, "student_marksheet.html", context)


@login_required(login_url='login')
def individual_student_marksheet(request, id, pk):
    user = User.objects.get(id=id)
    exam = Examination.objects.get(id=pk)
    userprofile = UserProfile.objects.get(user=user)
    questions = Question.objects.filter(associated_exam=exam)
    total_question = questions.count()
    student_response = Response_Table.objects.filter(
        user=userprofile, exam_associated=exam)

    st_response = {}
    for response in student_response:
        question_id = response.question.id
        actual_response = response.answer
        st_response[question_id] = actual_response
    # print(st_response)
    final = []
    for question in questions:
        temp = {}
        question_id = question.id
        answer = 'Not Attempted'
        try:
            json_answer = st_response[question_id]
            answer = json_answer
        except:
            pass

        temp['question'] = question
        temp['answer'] = answer
        final.append(temp)

    # print("final: ", final)
    context = {"user": user, "exam": exam, "questions": questions,
               "student_response": student_response,
               "final": final, "total_question": total_question}
    return render(request, "each_student_marksheet.html", context)
