class Service:

    def _methods(self):
        return [f for f in dir(self) if not f.startswith("_")]

    def print11111111111111111111111(self):
        print(1)

    def print22222222222222222222222(self):
        print(1)

    def print33333333333333333333333(self):
        print(1)


instance = Service()
