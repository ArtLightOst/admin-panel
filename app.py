from types import ModuleType
from flask import Flask, render_template, request
from service import get_list_of_modules
from config import Config

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


@app.add_template_filter
def synonym(text: str, module: str = None, method: str = None):
    if module and method:
        return Config[module]["methods"][method]
    elif module:
        return Config[module]["synonym"]
    else:
        return text
