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
