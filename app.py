from types import ModuleType
from flask import Flask, render_template, request
from os import listdir

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(template_name_or_list="index.html", modules=get_list_of_modules())


@app.route('/<string:module>')
def init_module(module: str):
    module_object: ModuleType = __import__(f"modules.{module}", globals(), locals(), ["instance"])
    return render_template(template_name_or_list="module.html", module_name=module,
                           methods=module_object.instance.methods(), modules=get_list_of_modules())


@app.route('/<string:module>/<string:function>', methods=['POST'])
def command(module: str, function: str):
    module_object: ModuleType = __import__(f"modules.{module}", globals(), locals(), ["instance"])
    exec(compile(source="response = module_object.instance." + function + "(request.get_json())",
                 filename="",
                 mode="exec"),
         globals(),
         locals())
    return locals()['response']


def get_list_of_modules() -> list[str]:
    return [f[:len(f) - 3] for f in listdir("./modules/") if f.endswith(".py")]
