from vanir.core.exchange.models import AllowedPairs


def update_pairs_price(records, source):
    # TODO: Check how if this is possible in future, see models.py for reference
    with AllowedPairs.objects.bulk_update_or_create_context(
        ["price"], match_field="pair", batch_size=5000
    ) as bulkit:
        for pair, price in records.items():
            if source:
                bulkit.queue(AllowedPairs(pair=pair, price=price, source=source))
            else:
                bulkit.queue(AllowedPairs(pair=pair, price=price))
    return records
