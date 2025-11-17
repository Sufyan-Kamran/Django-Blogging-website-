import json

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
        fields = "__all__"
        read_only_fields = ["author"]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def create(self, validated_data):

        # Get tags from initial_data
        tags_data = self.initial_data.get("tags", [])

        # Parse tags if it's a JSON string (from FormData)
        if isinstance(tags_data, str):
            try:
                tags_data = json.loads(tags_data)
            except json.JSONDecodeError:
                tags_data = []

        author = validated_data.pop("author")
        post = Post.objects.create(author=author, **validated_data)

        for tag_name in tags_data:
            if tag_name.strip():  # Skip empty strings
                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                post.tags.add(tag)

        return post

    def update(self, instance, validated_data):
        tags_data = self.initial_data.get("tags", None)

        # Parse JSON string manually
        if tags_data and isinstance(tags_data, str):
            try:
                tags_data = json.loads(tags_data)
            except json.JSONDecodeError:
                tags_data = []

        # Update standard fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Update tags
        if tags_data is not None:
            instance.tags.clear()
            for tag_name in tags_data:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)

        return instance
