class Service:

    def methods(self):
        return [f for f in dir(self) if not f.startswith("_") and f.startswith("public")]

    def public_print(self):
        print(2)

    def shadow_print(self, data: dict) -> dict:
        print(data)
        # Тут должен выполняться системный код, результат выполнения парситься и формируется json (спецификацию определю позже)
        return {"Скрытый 2": 2}


instance = Service()
