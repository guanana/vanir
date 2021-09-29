import django_filters
from django.contrib import auth
from django.db.models import Q
from django_filters import FilterSet

from vanir.core.account.models import Account

UserModel = auth.get_user_model()


class AccountFilterSet(FilterSet):
    # exchange_id = django_filters.ModelMultipleChoiceFilter(
    #     field_name='exchange',
    #     queryset=Exchange.objects.all(),
    #     label='Exchange (ID)',
    # )
    # exchange = django_filters.ModelMultipleChoiceFilter(
    #     field_name='exchange__name',
    #     queryset=Exchange.objects.all(),
    #     to_field_name='name',
    #     label='Exchange (Name)',
    # )
    # user_id = django_filters.ModelMultipleChoiceFilter(
    #     field_name='user',
    #     queryset=UserModel.objects.all(),
    #     label='User (ID)',
    # )
    # user = django_filters.ModelMultipleChoiceFilter(
    #     field_name='user__username',
    #     queryset=UserModel.objects.all(),
    #     label='User (Username)',
    # )
    # token_id = django_filters.ModelMultipleChoiceFilter(
    #     field_name='token',
    #     queryset=Token.objects.all(),
    #     label='Token (id)',
    # )
    # token_symbol = django_filters.ModelMultipleChoiceFilter(
    #     field_name='token__symbol',
    #     queryset=Token.objects.all(),
    #     label='Token (Symbol)',
    # )
    # token = django_filters.ModelMultipleChoiceFilter(
    #     field_name='token__name',
    #     queryset=Token.objects.all(),
    #     label='Token (Name)',
    # )

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(exchange__name__icontains=value)
            | Q(token__name__icontains=value)
            | Q(token__symbol__icontains=value)
        )

    class Meta:
        model = Account
        fields = {
            "name": ["icontains"],
            "api_key": ["iexact"],
            "secret": ["iexact"],
            "tld": ["iexact"],
            "default": ["eq"],
            "testnet": ["eq"],
        }
