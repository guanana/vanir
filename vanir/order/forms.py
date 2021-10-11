from dal import autocomplete
from django import forms

from vanir.core.token.models import Token
from vanir.order import constants
from vanir.order.models import (
    LimitOrder,
    MarketOrder,
    StopLossOrTakeProfitLimitOrder,
    StopPriceOrder,
)


class BaseOrderFrom(forms.ModelForm):
    token_from = forms.ModelChoiceField(
        queryset=Token.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="order:tokenfrom_autocomplete",
            forward=["account"],
            attrs={"data-container-css-class": ""},
        ),
        help_text=constants.TOKEN_FROM,
    )
    token_to = forms.ModelChoiceField(
        queryset=Token.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="order:tokento_autocomplete",
            forward=["token_from", "account"],
            attrs={"data-container-css-class": ""},
        ),
    )


class LimitForm(BaseOrderFrom):
    class Meta:
        model = LimitOrder
        fields = (
            "account",
            "token_from",
            "token_to",
            "side",
            "quoteOrderQty",
            "price",
            "timeInForce",
        )


class MarketForm(BaseOrderFrom):
    class Meta:
        model = MarketOrder
        fields = ("account", "token_from", "token_to", "side", "quoteOrderQty")


class StopPriceForm(BaseOrderFrom):
    class Meta:
        model = StopPriceOrder
        fields = (
            "account",
            "token_from",
            "token_to",
            "side",
            "ORDER_TYPE",
            "quoteOrderQty",
            "stopprice",
        )


class StopLossOrTakeProfitLimitForm(BaseOrderFrom):
    class Meta:
        model = StopLossOrTakeProfitLimitOrder
        fields = (
            "account",
            "token_from",
            "token_to",
            "side",
            "quoteOrderQty",
            "ORDER_TYPE",
            "timeInForce",
            "price",
            "stopprice",
        )
