from types import ModuleType
from flask import Flask, render_template
from os import listdir

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(template_name_or_list="index.html", modules=get_list_of_modules())


@app.route('/<string:MODULE>')
def init_module(MODULE):
    module_object: ModuleType = __import__(f"modules.{MODULE}", globals(), locals(), ["instance"])
    return render_template(template_name_or_list="module.html", module_name=MODULE,
                           module=module_object.instance._methods(), modules=get_list_of_modules())


@app.route('/<string:MODULE>/<string:FUNCTION>')
def command(MODULE, FUNCTION):
    module_object: ModuleType = __import__(f"modules.{MODULE}", globals(), locals(), ["instance"])
    exec("module_object.instance." + FUNCTION + "()")
    return ""


def get_list_of_modules() -> list[str]:
    return [f[:len(f) - 3] for f in listdir("./modules/") if f.endswith(".py")]
