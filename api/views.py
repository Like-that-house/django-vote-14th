from .models import User, Candidate
from .serializers import *
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.filters import OrderingFilter

# Create your views here.

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CandidateViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    filter_backends = [OrderingFilter]
    # ordering_fields = ['-votes'] # 정렬 허용 리스트
    ordering = ['-votes'] # default 정렬 지정


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        candidate = get_object_or_404(Candidate, pk=id)
        return candidate

    def get(self, request, id, format=None):
        candidate = self.get_object(id)
        user = request.user
        if user.voteDone:
           return Response({"message":"voteDone"}, status=status.HTTP_403_FORBIDDEN)

        user.voting_for = candidate
        user.voteDone = True
        candidate.votes += 1
        user.save()
        candidate.save()
        return Response({"message":"Successfully Voted to " + user.voting_for.name}, status=status.HTTP_200_OK)





