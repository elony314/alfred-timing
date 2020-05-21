function run(argv) {
	let query = argv[0]
	let task = JSON.parse(query)
	let helper = Application("TimingHelper")
	if (!helper.scriptingSupportAvailable()) { throw "Scripting support requires a Timing Expert license. Please contact support via https://timingapp.com/contact to upgrade."; }
	let app = Application.currentApplication()
	app.includeStandardAdditions = true

	if (task.proj_id){ //if exist a parent project
		//get the project instance by id
		function searchProjectByID(id, projects=helper.rootProjects()) {
			return projects.map((project) => {
				if (project.id() === id) {
					return project
				} else {
					return searchProjectByID(project.projects(), id)
				}
			})
		}

		helper.startTask({ "withTitle": task.task_name, "project": searchProjectByID(task.proj_id) })
	} else { //either it is a existing task with no parent, or it is a new task
		helper.startTask({"withTitle": task.task_name})
	}

}