from os import listdir


class ParentService:

    def methods(self):
        return [f for f in dir(self) if not f.startswith("_") and f.startswith("public")]


def get_list_of_modules() -> list[str]:
    return [f[:len(f) - 3] for f in listdir("./modules/") if f.endswith(".py")]
