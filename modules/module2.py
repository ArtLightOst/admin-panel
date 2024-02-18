from service import ParentService


class Service(ParentService):

    def public_print(self, data: dict) -> dict:
        response = {
            "tag": "input",
            "type": "text",
            "class": "input1"
        }
        return response


instance = Service()
