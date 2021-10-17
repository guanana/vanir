import pdb


class Orders:
    def __init__(self, **kwargs):
        self.orderid = kwargs.get("orderid", kwargs.get("newClientOrderId"))
        self.symbol = kwargs.get(
            "symbol",
            f'{kwargs.get("token_from").symbol}{kwargs.get("token_to").symbol}',
        )
        self.side = kwargs.get("side")
        self.type = kwargs.get("type")
        self.quantity = kwargs.get("quoteOrderQty")
        self.validated = False

    def correct_precision(self, new_precision):
        pdb.set_trace()
        if len(str(self.quantity).split(".")[1]) > new_precision:
            self.quantity = round(float(self.quantity), new_precision)
            return True
        return False

    @property
    def binance_args(self):
        kwargs = {
            "newClientOrderId": self.orderid,
            "symbol": self.symbol,
            "side": self.side,
            "type": self.type,
            "quantity": self.quantity,
        }
        return kwargs
