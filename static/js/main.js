async function ExecPythonCommand(module, command) {
	let body = JSON.stringify({"1": 1, "2": 2})
	let response = await fetch("/" + module + "/" + command.replace("public", "shadow"), {
		method: "POST",
		headers: {"Content-Type": "application/json", "Accept": "application/json"},
		mode: "same-origin",
		body: body
	})
	let data = await response.json();
	// Тут парситься json из python и перерисовывается блок methods-content в соответствие со спецификацией (определю позже)
	console.log(data)
}