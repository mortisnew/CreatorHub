from django.db.models import Count, Value, FloatField
from django.db.models import (ExpressionWrapper, F,
                              DurationField)
from django.db.models.functions import Now, Extract,Power
from rest_framework.generics import ListAPIView
from core.models import CreatePost
from core.serialiserz import CreatePostSerializer

class HomeViewSet(ListAPIView):
    serializer_class = CreatePostSerializer

    def get_queryset(self):
        return CreatePost.objects.filter(is_allowed=True,
                                         community__memberships__user=self.request.user
                                         ).order_by('-created_at')

class ExploreViewSet(ListAPIView):
    serializer_class = CreatePostSerializer

    def get_queryset(self):
        explore_score =  CreatePost.objects.filter(
            is_allowed=True,
            published_at__isnull=False
        ).annotate(
            like_count=Count('like', distinct=True),
            comment_count=Count('comment', distinct=True)
        ).annotate(
            time_passed=ExpressionWrapper(
                Now() - F('published_at'),
                output_field=DurationField()
            )
        ).annotate(
            hour_passed=ExpressionWrapper(
                Extract(
                    F('time_passed'),
                    'epoch',
                    output_field=FloatField()
                ) / Value(3600.0),
                output_field=FloatField()
            )
        )
        explore_score = explore_score.annotate(
            trend_score=(
                F('like_count') + 2 * F('comment_count') /
                Power(F('hour_passed') + Value(2.0),Value(1.5))
            )
        ).order_by('-trend_score')

        return explore_score