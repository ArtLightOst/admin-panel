from service import ParentService


class Service(ParentService):

    def public_print(self, data: dict) -> dict:  # TODO: доработать структуру данных для отрисовки
        response = {
            "tag": "input",
            "type": "text",
            "class": "input1"
        }
        return response


instance = Service()
