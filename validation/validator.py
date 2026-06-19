class Validator:

    def __init__(self, rules):
        self.rules = rules

    def validate(self, row):

        for rule in self.rules:

            error = rule.validate(row)

            if error:
                return error

        return None