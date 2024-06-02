const email = document.getElementById('email')
const password = document.getElementById('password')
const form = document.getElementById('login')
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

    if (email.value === '' || email.value == null ){
        e.preventDefault()
        errorElement.innerText = ('Email is required')
    }

    else if (password.value === '' || password.value == null )
    {
        e.preventDefault()
        errorElement.innerText = ('Password is required')
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

})
