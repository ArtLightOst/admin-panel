function ExecPythonCommand(module, command) {
	let request = new XMLHttpRequest()
	request.open("Get", "/" + module + "/" + command, true)
	request.send()
}