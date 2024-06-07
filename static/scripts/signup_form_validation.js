const username = document.getElementById('username')
const password = document.getElementById('password')
const confirm_password = document.getElementById('confirm_password')
const form = document.getElementById('signup')
const errorElement = document.getElementById('error')

const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};

form.addEventListener('submit', (e)=>{
    let messages = []
    if (username.value === '' || username.value == null ){
        e.preventDefault()
        errorElement.innerText = ('Username is required')
    }

    else if (email.value === '' || email.value == null ){
        e.preventDefault()
        errorElement.innerText = ('Email is required')
    }

    else if (password.value === '' || password.value == null )
    {
        e.preventDefault()
        errorElement.innerText = ('Password is required')
    }

    else if (confirm_password.value === '' || confirm_password.value == null )
    {
        e.preventDefault()
        errorElement.innerText = ('Please confirm password')
    }

    else if (username.value.length <= 3 || username.value.length >= 15)
    {
        e.preventDefault()
        errorElement.innerText = ('Username must be 3 - 15 characters')
    }

    else if(!validateEmail(email.value)){
        e.preventDefault()
        errorElement.innerText = ('Invalid email')
    }

    else if (password.value.length < 10 )
    {
        e.preventDefault()
        errorElement.innerText = ('Password must be 10 characters or longer')
    }

    else if (password.value !== confirm_password.value)
    {
        e.preventDefault()
        errorElement.innerText = ('Passwords do not match')
    }
})