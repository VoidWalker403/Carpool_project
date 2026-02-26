from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    /api/posts/        -> list, create
    /api/posts/{id}/   -> retrieve, update, delete
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # user can see only their own posts
        return Post.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # auto-assign logged-in user
        serializer.save(user=self.request.user)


