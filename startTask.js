function run(argv) {
	var query = argv[0]
	var task = JSON.parse(query)
	var helper = Application("TimingHelper")
	if (!helper.scriptingSupportAvailable()) { throw "Scripting support requires a Timing Expert license. Please contact support via https://timingapp.com/contact to upgrade."; }
	var app = Application.currentApplication()
	app.includeStandardAdditions = true

	var target_proj

	if (task.proj_id){ //if exist a parent project
		//get the project instance by id
		function searchProjectByID(projects, id) {
			return projects.map(function (project) {
				if (project.id() === id) {
					target_proj = project
				} else {
					return searchProjectByID(project.projects(), id)
				}
			})
		}

		searchProjectByID(helper.rootProjects(), task.proj_id)
		helper.startTask({ "withTitle": task.task_name, "project": target_proj })
	} else {
		helper.startTask({"withTitle": task.task_name})
	}

}