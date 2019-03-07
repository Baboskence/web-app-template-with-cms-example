//************************ON LOAD*****************************
document.addEventListener('DOMContentLoaded', function () {
	function request(obj) {
		return new Promise((resolve, reject) => {
			let xhr = new XMLHttpRequest();
			xhr.open(obj.method || "GET", obj.url);
			if (obj.headers) {
				Object.keys(obj.headers).forEach(key => {
					xhr.setRequestHeader(key, obj.headers[key]);
				});
			}
			xhr.onload = () => {
				if (xhr.status >= 200 && xhr.status < 300) {
					resolve(xhr.response);
				} else {
					reject(xhr.statusText);
				}
			};
			xhr.onerror = () => reject(xhr.statusText);
			xhr.send(obj.body);
		});
	}
	//return with ready-to-use content units, including events
	function UnitDom(data) {
		this.detail = document.createElement('details');
		this.summary = document.createElement('summary');
		this.controls = document.createElement('div');
		this.output = document.createElement('div');
		this.saveButton = document.createElement('button');
		//set up unit
		this.summary.innerHTML = data.description;
		this.controls.id = 'controls-' + data.name;
		this.output.id = 'output-' + data.name;
		this.saveButton.innerHTML = "Save"
			//build dom-tree inside Details tag
			this.detail.appendChild(this.summary);
		this.detail.appendChild(this.controls);
		this.detail.appendChild(this.output);
		this.detail.appendChild(this.saveButton);
	}
	let main = document.body.getElementsByTagName('main')[0];
	Admin.contentUnitData.forEach(function (unitData) {
		//create dom representation of unit
		let unitDom = new UnitDom(unitData);
		//append to main
		main.appendChild(unitDom.detail);
		//set up text-editor
		let editor = new Admin.textEditor.Editor({
				ctrElement: unitDom.controls,
				outElement: unitDom.output
			});

		//saveButton:update contents, catch problem
		unitDom.saveButton.addEventListener('click',function () {
			request({
				url: '/update',
				method: 'post',
				headers: {
					"content-type": "application/json"
				},
				body: JSON.stringify({
					fName: unitData.fName,
					newContent: unitDom.output.innerHTML
				})
			}).catch(err => alert(err));
		});
	});

}, false);
