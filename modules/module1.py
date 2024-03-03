from service import ParentService, create_button, create_input, create_table


class Service(ParentService):

    def public_print(self, data: dict) -> list[dict]:
        response = [

            *create_input(
                id="input1",
                caption="Создано функцией"
            ),

            create_button(
                id="button1",
                caption="Создано функцией",
                module='module1',
                method='print'),

            create_table(
                id="table1",
                headers="Заголовок1, Заголовок2, Заголовок3",
                data=[
                    {
                        "1": 1, "2": 2, "3": 3
                    },
                    {
                        "1": 1, "2": 2, "3": 3
                    },
                    {
                        "1": 1, "2": 2, "3": 3
                    }
                ]
            )

        ]
        return response

    def print(self, data: dict):
        print(data)
        return {}


instance = Service()
