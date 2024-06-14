from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, status, permissions, filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import FriendRequest
from .pagination import UserSearchPagination
from .serializers import UserSerializer, UserDetailSerializer, FriendRequestSerializer
from django.utils import timezone
from datetime import timedelta


class UserSignup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        request.data['email'] = request.data['email'].lower()
        return super().create(request, *args, **kwargs)


class UserLogin(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserSearch(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'username']
    queryset = User.objects.all()
    pagination_class = UserSearchPagination


class SendFriendRequest(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        from_user = request.user
        to_user_id = request.data.get('to_user')
        to_user = User.objects.get(id=to_user_id)

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago).count()
        if recent_requests >= 3:
            return Response({'error': 'Rate limit exceeded'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)
        if not created:
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)


class RespondFriendRequest(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = FriendRequest.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        user_status = request.data.get('status')
        if user_status in ['accepted', 'rejected']:
            instance.status = user_status
            instance.save()
            return Response(FriendRequestSerializer(instance).data)
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class FriendList(generics.ListAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(Q(from_user=user, status='accepted') | Q(to_user=user, status='accepted'))
        user_ids = [fr.to_user.id if fr.from_user == user else fr.from_user.id for fr in friends]
        return User.objects.filter(id__in=user_ids)


class PendingFriendRequests(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')
