class BaseService:
    """This is a template of a a base service.
    All services in the app should follow this rules:
      * Input variables should be done at the __init__ phase
      * Service should implement a single entrypoint without arguments
    
    This is ok:
      @dataclass
      class UserCreator(BaseService):
        first_name: str
        last_name: Optional[str]
        
        def act(self) -> User:
          return User.objects.create(first_name=self.first_name, last_name=self.last_name)
          
        # user = UserCreator(first_name='Ivan', last_name='Petrov')()
          
    This is not ok:
      class UserCreator:
        def __call__(self, first_name: str, last_name: Optional[str]) -> User:
          return User.objects.create(first_name=self.first_name, last_name=self.last_name)
          
    For more service implementation examples, check out https://github.com/tough-dev-school/education-backend/tree/master/src/orders/services
    """      
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
