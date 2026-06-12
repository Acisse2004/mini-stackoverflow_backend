import django_filters
from .models import Question


class QuestionFilter(django_filters.FilterSet):
    """
    Filtres pour la liste des questions.
    US006 — tri par date, votes, sans réponse
    US013 — filtrer par tag
    """
    tag = django_filters.CharFilter(field_name='tags__name', lookup_expr='iexact')
    unresolved = django_filters.BooleanFilter(method='filter_unresolved')

    class Meta:
        model = Question
        fields = ['tag', 'unresolved']

    def filter_unresolved(self, queryset, name, value):
        if value:
            # Questions sans meilleure réponse
            return queryset.exclude(answers__is_best=True)
        return queryset
