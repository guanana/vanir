from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template import loader

from vanir.account.models import Account
from vanir.exchange.helpers.main import BasicExchange
from vanir.exchange.utils import SUPPORTED_EXCHANGES


def get_exchange(pk) -> BasicExchange:
    """
    Return the Exchange object corresponding to the exchange selected in the account
    """
    account = Account.objects.get(pk=pk)
    try:
        classname = SUPPORTED_EXCHANGES[account.exchange.name.split(" ")[0]]
    except KeyError:
        raise ValidationError(
            f"Please create an account with a supported Exchange to get extra functionalities"
            f"{[item for item in SUPPORTED_EXCHANGES.keys()]}"
        )
    return classname(account)


def exchange_view_render(template_name, response, request, **kwargs):
    template = loader.get_template(template_name)
    context = {"con": response, **kwargs}
    return HttpResponse(template.render(context, request))
