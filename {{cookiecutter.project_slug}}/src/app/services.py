class BaseService:
    def __call__(self):
        self.validate()
        return self.action()

    def get_validators(self):
        return []

    def validate(self):
        validators = self.get_validators()
        for validator in validators:
            validator()

    def action(self):
        return
