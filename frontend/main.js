let projectsUrl = 'http://localhost:8000/api/projects/'

let getProjects = () => {
    fetch(projectsUrl)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            buildProjects(data)
        })
}


let buildProjects = (projects) => {
    let projectsWrapper = document.getElementById("projects-wrapper")
    projectsWrapper.innerHTML = ``
    // console.log('project-wrapper: ', projectsWrapper)

    for (let i = 0; projects.length > i; i++) {
        let project = projects[i]
        
        let projectCard = `
                <div class="project--card">
                    <img src="http://localhost:8000${project.featured_image}/"/>
                    <div>
                        <div class="card--header">
                            <h3>${project.title}</h3>
                            <strong class="vote--option" data-vote="up" data-project="${project.id}">&#43;</strong>
                            <strong class="vote--option" data-vote="down" data-project="${project.id}">&#8722;</strong>
                            
                        </div>
                        <i>${project.vote_ratio}% Positive feedback</i>
                        <p>${project.description.substring(0, 150)}</p>
                    </div>
                </div>
        `

        projectsWrapper.innerHTML += projectCard
    }

    addVoteEvents()

}


let addVoteEvents = () => {
    let token = localStorage.getItem('token')
    let voteButtons = document.getElementsByClassName("vote--option")
    for (let i = 0; i < voteButtons.length; i++) {
        voteButtons[i].addEventListener('click', (e)=> {
            let voteValue = e.target.dataset.vote
            let voteProject = e.target.dataset.project
            
            fetch(
                `http://localhost:8000/api/projects/${voteProject}/vote`, 
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization" : `Bearer ${token}`
                    },
                    body: JSON.stringify({"value": voteValue})
                }
            )
            .then(response => 
                response.json()
            )
            .then(data => {
                console.log(data)
                // 刷新页面
                getProjects()
            })

        })
    }


}


projects = getProjects()