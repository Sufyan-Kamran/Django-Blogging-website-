from .models import Post
import django_filters

class PostFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')

    class Meta:
        model = Post
        fields = ["author", "category"]