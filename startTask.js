function run(argv) {
	let query = argv[0]
	let task = JSON.parse(query)
	let helper = Application("TimingHelper")
	if (!helper.scriptingSupportAvailable()) { throw "Scripting support requires a Timing Expert license. Please contact support via https://timingapp.com/contact to upgrade."; }
	let app = Application.currentApplication()
	app.includeStandardAdditions = true

	if (task.proj_id){ //if exist a parent project
		//get the project instance by id
		function searchProjById(id, projects=helper.rootProjects()){
			return projects.map(p=>{
				if(p.id() === id){
					return p
				} if (p.projects()!==undefined && p.projects().length!=0){
					return searchProjById(id, p.projects())
				} else {
					return null
				}
			}).reduce((acc, cur)=>{
				return acc!==null ? acc : cur
			})
		}

		helper.startTask({ "withTitle": task.task_name, "project": searchProjById(task.proj_id)})
	} else { //either it is a existing task with no parent, or it is a new task
		helper.startTask({"withTitle": task.task_name})
	}

}