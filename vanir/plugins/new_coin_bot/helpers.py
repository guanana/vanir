from vanir.core.token.models import Token


def token_already_exists(symbol):
    try:
        Token.objects.get(symbol=symbol)
        return True
    except Token.DoesNotExist:
        return False
