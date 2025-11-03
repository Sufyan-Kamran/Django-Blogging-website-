from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics, filters
from .models import Post, Comment, Like
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .filters import PostFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404


# handling with apiview
class PostView(APIView):
    def get_permissions(self):
        """
        Apply authentication only for create, update, and delete requests.
        Allow anyone to view posts.
        """
        if self.request.method in ["POST", "PATCH", "DELETE"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, post_id=None, *args, **kwargs):
        if post_id:
            queryset = Post.objects.get(id=post_id)
            post_serializer = PostSerializer(queryset, many=False)
            return Response(post_serializer.data)

        queryset = Post.objects.all().order_by("-created_at")
        post_serializer = PostSerializer(queryset, many=True)

        return Response(post_serializer.data)

    def post(self, request):
        data = request.data.copy()
        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        if post.author != request.user:
            return Response({"error": "You can only update your own post."}, status=403)

        data = request.data.copy()

        serializer = PostSerializer(post, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        if post.author != request.user:
            return Response({"error": "You can only delete your own post."}, status=403)

        post.delete()
        return Response({"sucess": f"post {post.title} is deleted"})


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        data["author"] = user.id

        serializer = CommentSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.author != request.user:
            return Response(
                {"error": "You can only edit your own comments."}, status=403
            )

        serializer = CommentSerializer(
            comment, data=request.data, partial=True, context={"request": request}
        )

        if serializer.is_valid():
            comment.comment = serializer.validated_data.get("comment", comment.comment)
            comment.save()
            return Response(CommentSerializer(comment).data, status=200)

        return Response(serializer.errors, status=400)

    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if comment.author != request.user:
            return Response(
                {"error": "You can only delete your own comments."}, status=403
            )

        comment.delete()
        return Response(
            {"message": "Comment deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class LikeView(APIView):
    def post(self, request):
        data = request.data.copy()
        data["author"] = request.user.id

        serializer = LikeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "liked successfully."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        post_id = request.data.get("post_id")
        like = Like.objects.filter(post_id=post_id, author=request.user).first()

        if not like:
            return Response({"error": "You didn't like this post."}, status=403)

        like.delete()
        return Response(
            {"message": "like removed successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class TagView(APIView):
    def get(self, request):
        return Response({"data": request.data})


class PostSearchView(generics.ListAPIView):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PostFilter
    search_fields = ["title", "content", "tags__name"]

