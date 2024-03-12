async function ExecPythonCommand(module, command) {

	let body
	let root = document.querySelector("#methods-content")

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
		renderContent(root, data)
	} else {
		console.log(data) // TODO: решить вопрос с переключением классов для отображения успеха или неудачи
	}
}

function getDataRecursive(current, container) {

	if (container instanceof Array) {
		container.push(convertElement(current))
	} else {
		container[current.id] = convertElement(current)
	}

	if (current.childElementCount > 0) {

		for (let i = 0; i < current.childElementCount; i++) {

			let next

			if (container instanceof Array) {
				next = container.at(container.length - 1)["childs"]
			} else {
				next = container[current.id]["childs"]
			}

			getDataRecursive(current.children[i], next)
		}

	}

}


function convertElement(element) {

	let obj = {}

	obj["name"] = element?.name
	obj["value"] = element?.value
	obj["checked"] = element?.checked
	obj["text"] = element?.innerText

	if (element.childElementCount > 0) {
		obj["childs"] = []
	}

	return obj
}

function renderContent(root, data) {

	for (let element of data) {

		let keys = Object.keys(element)
		let child = document.createElement(element.tag)
		root.appendChild(child)
		keys.splice(keys.indexOf("tag"), 1)
		if (keys.includes("textContent")) {
			child.textContent = element.textContent
			keys.splice(keys.indexOf("textContent"), 1)
		}
		for (let key of keys) {
			if (key === "childs") {
				renderContent(child, element[key])
			} else {
				child.setAttribute(key, element[key])
			}
		}
	}
}
