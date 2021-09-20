from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template import loader

from vanir.account.models import Account
from vanir.exchange.utils import SUPPORTED_EXCHANGES
from vanir.utils.helpers import get_nav_menu


def get_exchange(pk):
    account = Account.objects.get(pk=pk)
    try:
        classname = SUPPORTED_EXCHANGES[account.exchange.name]
    except KeyError:
        raise ValidationError(
            f"Please create an account with a supported Exchange to get extra functionalities"
            f"{[item for item in SUPPORTED_EXCHANGES.keys()]}"
        )
    return classname(account)


def exchange_view_render(template_name, response, request):
    template = loader.get_template(template_name)
    context = {
        "con": response,
    }
    context = get_nav_menu(context)
    return HttpResponse(template.render(context, request))
