from rest_framework import serializers

from accounts.models import CustomUser
from .models import Quiz, Question, Choice, UserResponse


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'questions']


class UserResponseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = UserResponse
        fields = ['id', 'question', 'selected_choice', 'user']


class QuizResponseSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    selected_choice = serializers.IntegerField()
