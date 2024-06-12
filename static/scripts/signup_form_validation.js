const username = document.getElementById('username')
const password = document.getElementById('password')
const confirm_password = document.getElementById('confirm_password')
const form = document.getElementById('signup')
const errorElement = document.getElementById('error')
const dayInput = document.getElementById('dob-day');
const monthInput = document.getElementById('dob-month');
const yearInput = document.getElementById('dob-year');
const gender = document.getElementById('gender');

const validateEmail = (email) => {
  return String(email)
    .toLowerCase()
    .match(
      /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};

function isValidDate(day, month, year)
{
    const date = new Date(year, month - 1, day);
    return (
        date.getFullYear() === year &&
        date.getMonth() === month - 1 &&
        date.getDate() === day
    );
}

function isOldEnough(day, month, year)
{
    const today = new Date();
    const birthDate = new Date(year, month - 1, day);
    const age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();

    if (
        monthDiff < 0 ||
        (monthDiff === 0 && today.getDate() < birthDate.getDate())
    ) {
        return age - 1 >= 13;
    }
    return age >= 13;
}

form.addEventListener('submit', (e)=>{
    let messages = []
    const day = parseInt(dayInput.value, 10);
    const month = parseInt(monthInput.value, 10);
    const year = parseInt(yearInput.value, 10);

    if (username.value === '' || username.value == null ){
        e.preventDefault()
        errorElement.innerText = ('Username is required')
    }

    else if (email.value === '' || email.value == null ){
        e.preventDefault()
        errorElement.innerText = ('Email is required')
    }

    else if (!isValidDate(day, month, year))
    {
        e.preventDefault();
        errorElement.textContent = 'Please enter a valid date of birth.';
    }

    else if (gender.value === '' || gender.value == null)
    {
        e.preventDefault();
        errorElement.textContent = 'Please select your gender.';
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

    else if (!isOldEnough(day, month, year))
    {
        e.preventDefault();
        errorElement.textContent = 'You must be at least 13 years old to sign up.';
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


