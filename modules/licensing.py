# -*- coding: utf-8 -*-

import subprocess, re, sys, os, socket

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from service import ParentService, create_button, create_input, create_table, create_list, create_link, notify, MyThread, notify_telegram

config = {
	"licensing": {
		"synonyme": u"Лицензирование",
		"methods": {
			"public_licensing_status": u"Использованные лицензии"
			}
		},
        "Subject": u"Лицензирование",
        "recipients": ["", ""], # Указать получателей письма
        "body": u"Не осталось свободных лицензий",
	"telegram_token": "", # Указать токен от всеотца ботов
        "telegram_chats_id": [""], # Указать id чатов (получается только программно через http запрос
        "telegram_message": "",
	} 

class Service(ParentService):

    def public_licensing_status(self, data: dict) -> list[dict]:

        result = subprocess.run("/opt/1C/1CE/components/1c-enterprise-ring-0.19.5+12-x86_64/ring license list", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

        all_lics = []

        for line in result.stdout.split('\n'):
            if line:
                lic = re.search("\"\d+.lic\"", line)
                if lic[0]:
                    all_lics.append(lic[0].replace('"', ''))

        all_lics = dict().fromkeys(all_lics)

        result = subprocess.run("sudo lsof /var/1C/licenses/*", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
        used_lics = {}

        for line in result.stdout.split('\n'):
            if line:
                current = line.split()
                pid = current[1]
                current_lic = current[len(current) - 1]
                current_lic = current_lic.split('/')
                current_lic = current_lic[len(current_lic) - 1]
                used_lics[pid] = current_lic.replace(")", "")

        result = subprocess.run("ps axu | grep 'rmngr' | grep --invert-match 'grep rmngr'", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

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

        registration_numbers = {}

        for k in result:
            if result[k]:
                output = subprocess.run(f"grep \"Регистрационный номер: \" /var/1C/licenses/{result[k]}", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True).stdout
                registration_numbers[k] = output.split(":")[1].strip()

        for k in result:
            formatted.append(
                {
                    "server": k,
                    "lic": result[k] if result[k] else "Не используется",
		    "reg_number": registration_numbers[k] if registration_numbers.get(k, False) else "Не используется"
                }
            )

        formatted_free = []

        for lic in free:
            output = subprocess.run(f"grep \"Регистрационный номер: \" /var/1C/licenses/{lic}", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True).stdout
            number = output.split(":")[1].strip()
            formatted_free.append(f"{lic} ({number})")
	
        response = [

            create_table(
                id="lics",
                headers="Сервер, Лицензия, Регистрационный номер",
                data=formatted
            ),
            *create_list(
                id="free",
                array=formatted_free,
                caption="Свободные"
            )    
	    
        ]
        return response

    def public_long_operations(self, data: dict) -> MyThread:
        
        proc = MyThread(name="Тестовый скрипт", command=["bash", "mybashscript.sh"])

        proc.start()

        return proc

    def cron_licensing(self) -> int:

        try:

            result = subprocess.run("/opt/1C/1CE/components/1c-enterprise-ring-0.19.5+12-x86_64/ring license list", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

            all_lics = []

            for line in result.stdout.split('\n'):
                if line:
                    lic = re.search("\"\d+.lic\"", line)
                    if lic[0]:
                        all_lics.append(lic[0].replace('"', ''))

            all_lics = dict().fromkeys(all_lics)

            result = subprocess.run("sudo lsof /var/1C/licenses/*", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)
            used_lics = {}

            for line in result.stdout.split('\n'):
                if line:
                    current = line.split()
                    pid = current[1]
                    current_lic = current[len(current) - 1]
                    current_lic = current_lic.split('/')
                    current_lic = current_lic[len(current_lic) - 1]
                    used_lics[pid] = current_lic.replace(")", "")

            result = subprocess.run("ps axu | grep 'rmngr' | grep --invert-match 'grep rmngr'", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

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

            if not len(free) and len(result) > len(all_lics):
               notify(config["Subject"], config["recipients"], config["body"] + ", имя сервера: " + socket.gethostname())

            return 0

        except Exception as ex:

            return ex

def cron_check_prod(self) -> int:

    try:

        result = subprocess.run("ps axu | grep -i '{имя базы}' | grep --invert-match 'grep -i {имя базы}'", shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

        rmngr_is_up = False
        rphost_is_up = False

        for line in result.stdout.split('\n'):
            if line:
                rmngr = line.find("rmngr")
                if rmngr != -1:
                    rmngr_is_up = True
                rphost = line.find("rphost")
                if rphost != -1:
                    rphost_is_up = True

                if rmngr_is_up and rphost_is_up:
                    return 0

                for chat in config["telegram_chats_id"]:    
                    notify_telegram(config["telegram_token"], chat, config["telegram_message"])

        return 0
                       
    except Exception as ex:

        return ex


instance = Service()     

if __name__ == "__main__":
    for arg in sys.orig_argv:
        if arg == "check_prod_lic":
            sys.exit(instance.cron_check_prod())
        if arg == "check_all_lic":
            sys.exit(instance.cron_licensing())
