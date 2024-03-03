from os import listdir


class ParentService:

    def methods(self):
        return [f for f in dir(self) if not f.startswith("_") and f.startswith("public")]


def get_list_of_modules() -> list[str]:
    return [f[:len(f) - 3] for f in listdir("./modules/") if f.endswith(".py")]


def create_input(id: str, caption: str, type: str = "text") -> tuple[dict, dict]:
    tag_input = {
        "tag": "input",
        "id": id,
        "type": type
    }
    label_for_input = {
        "tag": "label",
        "for": id,
        "textContent": caption
    }

    return label_for_input, tag_input


def create_button(id: str, caption: str, module: str, method: str) -> dict:
    button = {
        "tag": "button",
        "id": id,
        "type": "submit",
        "textContent": caption,
        "onClick": f"ExecPythonCommand('{module}', '{method}')"
    }

    return button


def create_table(id: str, headers: str, data: list[dict]):
    table = {
        "tag": "table",
        "id": id,
        "childs": []
    }

    thead = {
        "tag": "thead",
        "id": "thead",
        "childs": []
    }

    thead_tr = {
        "tag": "tr",
        "id": "thead-tr",
        "childs": []
    }

    headers = headers.split(sep=",")

    for header in headers:
        thead_tr_th = {
            "tag": "th",
            "id": "thead-tr-th-" + str(headers.index(header)),
            "textContent": header
        }
        thead_tr["childs"].append(thead_tr_th)

    thead["childs"].append(thead_tr)
    table["childs"].append(thead)

    tbody = {
        "tag": "tbody",
        "id": "tbody",
        "childs": []
    }

    for element in data:
        tbody_tr = {
            "tag": "tr",
            "id": "tbody-tr-" + str(data.index(element)),
            "childs": []
        }

        for key in element.keys():
            tbody_tr_td = {
                "tag": "td",
                "id": "tbody-tr-td-" + str(data.index(element)),
                "textContent": element[key]
            }
            tbody_tr["childs"].append(tbody_tr_td)
        tbody["childs"].append(tbody_tr)

    table["childs"].append(tbody)

    return table
