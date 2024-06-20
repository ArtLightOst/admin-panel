import traceback
from types import ModuleType
from flask import Flask, render_template, request
from service import get_list_of_modules
from config import get_info_logger, get_error_logger
from random import randint

app = Flask(__name__)
info_logger = get_info_logger()
error_logger = get_error_logger()


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
    try:
        module_object: ModuleType = __import__(f"modules.{module}", globals(), locals(), ["instance"])
        exec(compile(source="response = module_object.instance." + function + "(request.get_json())",
                     filename="",
                     mode="exec"),
             globals(),
             locals())
        return locals()['response']
    except Exception as e:
        error_logger.error(f"{e} -> {traceback.format_exc()}")
        return {"error": "Произошла ошибка при POST запросе, смотрите логи"}


@app.route('/<string:module>/BackgroundProcesses', methods=['GET'])
def BackgroundProcesses(module: str):
        return [{
        "id": "test",
        "title": "Выполняется длительная операция",
        "value": randint(0, 100),
        "max": 100
    }]    
    


@app.add_template_filter
def synonym(text: str, module: str = None, method: str = None):
    if module and method:
        exec(compile(source = f"from modules.{module} import config", filename = "", mode = "exec"), globals(), locals())
        return locals()['config'][module]["methods"][method]
    elif module:
        exec(compile(source = f"from modules.{module} import config", filename = "", mode = "exec"), globals(), locals())
        return locals()['config'][module]["synonyme"]
    else:
        return text


@app.errorhandler(Exception)
def error_handler(e):
    error_logger.error(f"{e} -> {traceback.format_exc()}")
    return render_template(template_name_or_list="error.html")


@app.after_request
def log(response):
    if not (request.path == "/favicon.ico" or request.path.startswith("/static")):
        info_logger.info(
            f"{request.method} | {request.endpoint} | {response.status} | {request.host}\n{request.user_agent}"
        )
    return response
