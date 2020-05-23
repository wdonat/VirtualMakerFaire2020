
function postToServer(command, data, callback)
{
	let endPoint = "http://localhost:8000/api/v1/commandHandler";
//	let endPoint = "api/commandHandler.php";
	let sessionString = "testSessionString";
/*	
	if(command == "getScheduleInfo")
	{
		endPoint = "api/server_response.json";
	}
	else if(command == "updateScheduleInfo")
	{
		endPoint = "api/update_schedule.json";
	}
	else if(command == "getCurrentScheduleStatus")
	{
		endPoint = "api/current_state.json";
	}
	else if(command == "getGroups")
	{
		endPoint = "api/library_groups.json";
	}
	else if(command == "getSchedules")
	{
		endPoint = "api/library_schedules.json";
	}
	else if(command == "getSchedulesForImport")
	{
		endPoint = "api/import_schedules.json";
	}
*/
	let payloadObject = {
		sessionString: sessionString,
		command: command,
		data: data
	};

	const reqParams = {
		method: 'POST',
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(payloadObject)
	};

	const url_string = window.location.href;
	const url = new URL(url_string);
	let debug = url.searchParams.get("debug");

	if(debug == 1)
	{
		console.log("REQUEST:\n"+reqParams.body);
		alert("REQUEST:\n"+reqParams.body);
	}

	fetch(endPoint, reqParams)
		.then(response => response.json())
		.then(response => callback(response))
		//.catch(error => console.log(response));
		.catch(error => console.log('Request failed', error));

	return true;
}
