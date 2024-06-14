from django.urls import path
from .views import (UserSignup, UserLogin, UserSearch, SendFriendRequest, RespondFriendRequest,
                    FriendList, PendingFriendRequests)

urlpatterns = [
    path('signup/', UserSignup.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('search/', UserSearch.as_view(), name='user-search'),
    path('friend-request/', SendFriendRequest.as_view(), name='send-friend-request'),
    path('friend-request/<int:pk>/', RespondFriendRequest.as_view(), name='respond-friend-request'),
    path('friends/', FriendList.as_view(), name='friend-list'),
    path('pending-requests/', PendingFriendRequests.as_view(), name='pending-requests'),
]
