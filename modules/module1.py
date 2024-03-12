from service import ParentService, create_button, create_input, create_table, create_list, create_link


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
                headers="Заголовок1, Заголовок2, Заголовок3, Заголовок4",
                data=[
                    {
                        "11": 1, "22": 2, "33": 3, "input": create_input(id="1", type="checkbox")
                    },
                    {
                        "11": 1, "22": 2, "33": 3, "input": create_input(id="2", type="checkbox")
                    },
                    {
                        "11": 1, "22": 2, "33": 3, "input": create_input(id="3", type="checkbox")
                    }
                ]
            ),

            create_list(
                id="list",
                array=[
                    create_link(
                        id="ping",
                        link="",
                        text="Ping"
                    ),
                    create_link(
                        id="youtube",
                        link="https://www.youtube.com/",
                        text="Youtube"
                    ),
                    create_link(
                        id="github",
                        link="https://github.com/ArtLightOst",
                        text="Мой гитхаб"
                    )
                ]
            )

        ]
        return response

    def print(self, data: dict):
        print(data)
        return {}


instance = Service()
