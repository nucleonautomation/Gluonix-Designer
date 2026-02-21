class NucleonException(Exception):

    def __init__(self, Message, Data=None):
        super().__init__(Message)
        self.Data = Data