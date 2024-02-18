async function ExecPythonCommand(module, command) {

	let body
	let root = document.querySelector(".methods-content")

	if (command.startsWith("public")) {

		body = JSON.stringify({})

	} else {

		let container = {}
		getDataRecursive(root, container)
		body = JSON.stringify(container)

	}

	let response = await fetch("/" + module + "/" + command, {
		method: "POST",
		headers: {"Content-Type": "application/json", "Accept": "application/json"},
		mode: "same-origin",
		body: body
	})

	let data = await response.json();

	if (command.startsWith("public")) {
		root.innerHTML = ""
		renderContent(data)
	} else {
		console.log(data)
	}
}

function getDataRecursive(current, container) {

	if (container instanceof Array) {
		container.push(convertElement(current))
	} else {
		container[current.className] = convertElement(current)
	}

	if (current.hasChildNodes()) {

		for (let i = 0; i < current.childElementCount; i++) {
			getDataRecursive(current.children[i], container[current.className]["childs"])
		}

	}

}


function convertElement(element) { // TODO: придумать механизм без кучи ветвлений

	let obj = {}

	if (element.tagName === "INPUT") {

		obj["type"] = element.type.toString()
		obj["name"] = element.name.toString()
		obj["value"] = element.value.toString()

	}

	if (element.hasChildNodes()) {
		obj["childs"] = []
	}

	return obj
}

function renderContent(data) { // TODO: обобщить алгоритм отрисовки
	let root = document.querySelector(".methods-content")
	let child = document.createElement(data.tag)
	child.setAttribute("type", data.type)
	child.setAttribute("class", data.class)
	root.appendChild(child)
}
