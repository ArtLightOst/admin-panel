from service import ParentService, create_button, create_input


class Service(ParentService):

    def public_print(self, data: dict) -> list[dict]:  # TODO: доработать структуру данных для отрисовки
        response = [
            {"tag": "p",
             "textContent": "1",
             "id": "p1",
             "childs": [
                 {"tag": "p",
                  "textContent": "1.1",
                  "id": "p11",
                  "childs": [
                      *create_input(
                          id="input1",
                          caption="Создано функцией"
                      )
                  ]},

                 create_button(
                     id="button1",
                     caption="Создано функцией",
                     module='module1',
                     method='print')
             ]},
            {"tag": "p",
             "textContent": "2",
             "id": "p2",
             "childs": [
                 {"tag": "p",
                  "textContent": "2.1",
                  "id": "p21"}
             ]}
        ]
        return response

    def print(self, data: dict):
        print(data)
        return {}


instance = Service()
