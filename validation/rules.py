import pandas as pd

class PricePositiveRule:

    def validate(self, row):

        if pd.notna(row["price"]) and row["price"] < 0:
            return "negative_price"

        return None


class UserPresentRule:

    def validate(self, row):

        if pd.isna(row["user_id"]):
            return "missing_user"

        return None


class EventTypeRule:

    VALID_EVENT_TYPES = {
        "view",
        "cart",
        "purchase",
        "remove_from_cart"
    }

    def validate(self, row):

        if row["event_type"] not in self.VALID_EVENT_TYPES:
            return "invalid_event_type"

        return None