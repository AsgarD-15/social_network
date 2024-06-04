from django.urls import path
from .views import (
    UserSignupView,
    CustomAuthToken,
    UserSearchView,
    FriendRequestView,
    accept_friend_request,
    reject_friend_request,
    list_friends,
    list_pending_requests,
    PendingFriendRequestsView
)

urlpatterns = [
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request/accept/<int:request_id>/', accept_friend_request, name='accept-friend-request'),
    path('friend-request/reject/<int:request_id>/', reject_friend_request, name='reject-friend-request'),
    path('friends/', list_friends, name='list-friends'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='list-pending-requests'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', CustomAuthToken.as_view(), name='api-token-auth'),
]
