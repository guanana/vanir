from dal import autocomplete
from django import forms
from django.core.exceptions import ValidationError

from vanir.core.token.models import Token
from vanir.order import constants
from vanir.order.models import LimitOrder, MarketOrder, StopLossOrTakeProfitLimitOrder, StopPriceOrder


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

    def clean_quoteOrderQty(self):
        quantity = self.cleaned_data["quoteOrderQty"]
        if quantity <= 0:
            raise ValidationError("Quantity cannot be equal or less than 0")
        return quantity

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise ValidationError("Price cannot be equal or less than 0")
        return price

    def clean(self):
        cleaned_data = super().clean()
        order_obj, modified = cleaned_data.get("account").exchange_obj.order_validation(
            **self.cleaned_data
        )
        if modified:
            cleaned_data["quoteOrderQty"] = order_obj.quantity
        return cleaned_data


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
