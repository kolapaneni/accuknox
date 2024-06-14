from django.contrib.auth.models import User
from django.db import models


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'),
                                                      ('rejected', 'Rejected')], default='pending')

    class Meta:
        unique_together = ('from_user', 'to_user')
