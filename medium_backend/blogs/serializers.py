from rest_framework import serializers

from .models import Comment, Like, Post, Tag


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "comment", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Comment.objects.create(author=user, **validated_data)


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = "__all__"


class TagSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    likes = LikeSerializer(many=True, read_only=True)
    tags = TagSerialzer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "category",
            "likes_count",
            "likes",
            "comments",
            "tags",
            "image",
            "created_at",
            "updated_at",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        tags_data = self.initial_data.get("tags", [])
        author = validated_data.pop("author")
        post = Post.objects.create(author=author, **validated_data)

        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        return post

    def update(self, instance, validated_data):
        # Extract tags from initial data
        tags_data = self.initial_data.get("tags", [])

        # Update standard fields
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.category = validated_data.get("category", instance.category)
        instance.save()

        # Update tags
        if tags_data is not None:
            instance.tags.clear()  # remove old tags
            for tag_name in tags_data:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance
