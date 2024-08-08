from django.contrib import admin
from .models import Quiz, Question, Choice, UserResponse


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'text')
    search_fields = ('quiz', 'text')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    search_fields = ('question', 'text', 'is_correct')


@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('question', 'selected_choice', 'user')
    search_fields = ('question', 'selected_choice', 'user')

