from django.forms import ValidationError
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer, UserSignupSerializer
from django.db.models import Q
from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

User = get_user_model()

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id, 'email': token.user.email})

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('query', '').strip()
        if '@' in query:
            return User.objects.filter(email__iexact=query)
        else:
            return User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(receiver=user, accepted=False)

class FriendRequestView(generics.ListCreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(Q(sender=user) | Q(receiver=user))

    def perform_create(self, serializer):
        sender = self.request.user
        receiver_id = self.request.data.get('receiver_id')
        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            raise ValidationError({'error': 'Receiver does not exist'})
        if sender == receiver:
            raise ValidationError({'error': 'Cannot send friend request to yourself'})

        recent_requests = FriendRequest.objects.filter(sender=sender, timestamp__gte=datetime.now() - timedelta(minutes=1))
        if recent_requests.count() >= 3:
            raise ValidationError({'error': 'Cannot send more than 3 friend requests per minute'})

        serializer.save(sender=sender, receiver=receiver)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_friend_request(request, request_id):
    try:
        print(request.user, request_id)
        friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request does not exist'}, status=status.HTTP_404_NOT_FOUND)
    friend_request.accepted = True
    friend_request.save()
    return Response({'status': 'friend request accepted'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request does not exist'}, status=status.HTTP_404_NOT_FOUND)
    friend_request.delete()
    return Response({'status': 'friend request rejected'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_friends(request):
    user = request.user
    sent_friend_requests = FriendRequest.objects.filter(sender=user, accepted=True).values_list('receiver_id', flat=True)
    received_friend_requests = FriendRequest.objects.filter(receiver=user, accepted=True).values_list('sender_id', flat=True)
    
    friend_ids = set(sent_friend_requests) | set(received_friend_requests)
    friends = User.objects.filter(id__in=friend_ids)
    
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_pending_requests(request):
    user = request.user
    pending_requests = FriendRequest.objects.filter(receiver=user, accepted=False)
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
