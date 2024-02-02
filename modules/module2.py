class Service:

    def _methods(self):
        return [f for f in dir(self) if not f.startswith("_")]

    def print(self):
        print(2)


instance = Service()
