class BaseService:
    def __call__(self):
        self.validate()
        return self.act()

    def get_validators(self):
        return []

    def validate(self):
        validators = self.get_validators()
        for validator in validators:
            validator()

    def act(self):
        return
