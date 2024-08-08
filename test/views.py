from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.models import CustomUser
from .models import Quiz, Question, Choice, UserResponse
from .serializers import QuizSerializer, UserResponseSerializer, QuizResponseSerializer


class QuizListView(APIView):
    def get(self, request):
        quizzes = Quiz.objects.all()
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)


class QuizDetailView(APIView):
    def get(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
            serializer = QuizSerializer(quiz)
            return Response(serializer.data)
        except Quiz.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SubmitResponseView(APIView):
    def post(self, request):
        serializer = UserResponseSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Evaluates quiz and calculates score
class EvaluateQuizView(APIView):
    def post(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)

        responses = request.data.get('responses')
        if not responses:
            return Response({'error': 'No responses provided'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = QuizResponseSerializer(data=responses, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        correct_answers = 0

        for response in serializer.validated_data:
            question_id = response.get('question')
            selected_choice_id = response.get('selected_choice')
            try:
                choice = Choice.objects.get(id=selected_choice_id, question_id=question_id)
                if choice.is_correct:
                    correct_answers += 1
            except Choice.DoesNotExist:
                continue

        total_questions = quiz.questions.count()
        if total_questions > 0:
            score = (correct_answers / total_questions) * 100
        else:
            score = 0

        return Response({'score': score})


# Retrieve quiz results for a specific user
class QuizResultView(APIView):
    def get(self, request, quiz_id, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        quiz = get_object_or_404(Quiz, id=quiz_id)

        user_responses = UserResponse.objects.filter(user=user, question__quiz=quiz)
        correct_answers = sum(1 for response in user_responses if response.selected_choice.is_correct)
        total_questions = quiz.questions.count()
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

        return Response({
            'quiz_id': quiz.id,
            'user_id': user.id,
            'score': score,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
        }, status=status.HTTP_200_OK)
