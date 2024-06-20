from service import ParentService, create_button, create_input, create_table, create_list, create_link
import subprocess, re

class Service(ParentService):


    def public_print(self, data: dict) -> list[dict]:

        result = subprocess.run("cat all_lics.txt", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

        all_lics = []

        for line in result.stdout.split('\n'):
            if line:
                lic = re.search("\"\d+.lic\"", line)
                if lic[0]:
                    all_lics.append(lic[0].replace('"', ''))

        all_lics = dict().fromkeys(all_lics)

        result = subprocess.run("cat used_lics.txt", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        used_lics = {}

        for line in result.stdout.split('\n'):
            if line:
                current = line.split()
                pid = current[1]
                current_lic = current[len(current) - 1]
                current_lic = current_lic.split('/')
                current_lic = current_lic[len(current_lic) - 1]
                used_lics[pid] = current_lic.replace(")", "")

        result = subprocess.run("cat host_lics.txt", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

        host_lics = {}

        for line in result.stdout.split('\n'):
            if line:
                current = line.split()
                pid = current[1]
                index = current.index("-reghost")
                host_lics[pid] = current[index + 1]

        result = {}

        for key in host_lics:
            lic = used_lics.get(key)
            if pid:
                result[host_lics[key]] = lic
        
        keys = set(all_lics.keys())
        values = set(result.values())

        diff = keys.difference(values)

        free = list(diff)

        formatted = []

        for k in result:
            formatted.append(
                {
                    "server": k,
                    "lic": result[k] if result[k] else "Не используется"
                }
            )

        response = [

            create_table(
                id="lics",
                headers="Сервер, Лиценизия",
                data=formatted
            ),
            *create_list(
                id="free",
                array=free,
                caption="Свободные"
            )    
	    
        ]
        return response


instance = Service()
config = {
	"module1": {
		"synonyme": "Лицензирование",
		"methods": {
			"public_print": "Использованные лицензии"
			}
		}

	}
