from service import ParentService, create_button, create_input, create_table, create_list, create_link
import subprocess

class Service(ParentService):

    def public_print(self, data: dict) -> list[dict]:
        result = subprocess.run("ls", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        text = result.stdout.split()
        
        response = [

            create_list(
                id="list",
                array=text
            ),
            create_button(
		id = "button",
		caption = "Кнопка",
		module = "module1",
		method = "print_some"
	    )

        ]
        return response

    def print_some(self, data: dict) -> list[dict]:
        result = subprocess.run("systemctl start nginx", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        
        return {"feedback": str(result)}

instance = Service()
config = {
	"module1": {
		"synonyme": "Модуль 1",
		"methods": {
			"public_print": "Список файлов"
			}
		}

	}
