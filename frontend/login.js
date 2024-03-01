let form = document.getElementById('login-form')

form.addEventListener('submit', (e) => {
    e.preventDefault()
    // console.log('Form was submitted')
    let formData = {
        'username': form.username.value,
        'password': form.password.value
    }
    // console.log('FORM DATA: ', formData)

    fetch('http://localhost:8000/api/users/token/',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        }
    ).then(response => response.json())
    .then(data => {
        console.log(data)
        if (data.access == null) {
            alert('Username or password did not work')
        } else {
            localStorage.setItem('token', data.access)
            window.location = "file:///Users/hanbo/Projects/PythonProjects/DjangoProjects/frontend/project-list.html"
        }
        
    })
})