//setInterval(background, 1000)

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

	root.innerHTML = ""
	root.appendChild(getLoadingElement())
	
	let response = await fetch("/" + module + "/" + command, {
		method: "POST",
		headers: { "Content-Type": "application/json", "Accept": "application/json" },
		mode: "same-origin",
		body: body
	})

	let data = await response.json();

	if (command.startsWith("public")) {
		if (data?.error) {
			alert(data.error)
			return
		}
		root.innerHTML = ""
		renderContent(root, data)
	} else {
		let feedback = document.querySelector("#feedback")
		feedback.textContent = data.feedback
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

	obj["id"] = element?.id
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

async function background() {

	if (document.querySelector("#methods-wrapper")) {

		let response = await fetch(window.location.href.split("/").pop() + "/BackgroundProcesses")

		let data = await response.json()

		if (data) {

			for (let element of data) {

				id = element.id

				progress = document.querySelector("#" + id)

				if (progress) {

					progress.setAttribute("value", element.value)
					label = document.querySelector("#label" + id)
					label.textContent = element.title + "(" + element.value * 100 / element.max + "%)"

				}
				else {

					parent = document.querySelector("#feedback")

					newContainer = document.createElement("div")
					newContainer.setAttribute("id", "container" + id)

					newProgress = document.createElement("progress")
					newProgress.setAttribute("id", id)
					newProgress.setAttribute("value", element.value)
					newProgress.setAttribute("max", element.max)

					newLabel = document.createElement("label")
					newLabel.setAttribute("for", id)
					newLabel.setAttribute("id", "label" + id)
					newLabel.textContent = element.title + "(" + element.value * 100 / element.max + "%)"

					newContainer.appendChild(newLabel)
					newContainer.appendChild(newProgress)

					parent.appendChild(newContainer)

				}

			}

		}

	}

}

function getLoadingElement() {
	
	img = document.createElement("img")
	img.setAttribute("src", "/static/img/loading.gif")

	return img

}
