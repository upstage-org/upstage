class CustomClientIDMutationMeta(ClientIDMutationMeta):
    ''' We have to subclass the metaclass of ClientIDMutation and inject the errors field.
        we do this because ClientIDMutation subclasses do not inherit the fields on it.
    '''
    def __new__(mcs, name, bases, attrs):
        attrs['errors'] = String()
        return super().__new__(mcs, name, bases, attrs)



class CustomClientIDMutation(ClientIDMutation, metaclass=CustomClientIDMutationMeta):
    ''' Custom ClientIDMutation that has a errors  @fields.'''
    @classmethod
    def mutate(cls, root, args, context, info):
        try:
            return super().mutate(root, args, context, info)

        except MutationException as e:
            return cls(errors=str(e))

class MutationException(Exception):
    '''A Mutation Exception is an exception that is raised
       when an error message needs to be passed back to the frontend client
       our mutation base class will catch it and return it appropriately
    '''
    pass
