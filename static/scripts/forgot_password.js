function showEmailPopup() {
      document.getElementById('popup-overlay').style.display = 'flex';
      document.getElementById('email-popup').style.display = 'block';
      document.getElementById('code-popup').style.display = 'none';
    }

    async function submitEmail(event) {
      event.preventDefault();
      const email = document.getElementById('email-input').value;
      if (email) {
        try {
          const response = await fetch('/submit-email', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email: email }),
          });
          const result = await response.json();
          if (response.ok) {
            document.getElementById('email-popup').style.display = 'none';
            document.getElementById('code-popup').style.display = 'block';
          } else {
            alert(result.message || 'Failed to submit email.');
          }
        }
        catch (error) {
          console.error('Error submitting email:', error);
          alert('An error occurred. Please try again.');
        }
      }
      else {
        alert('Please enter your email.');
      }
    }

    async function submitCode(event) {
      event.preventDefault();
      const code = document.getElementById('code-input').value;
      if (code) {
        try {
          const response = await fetch('/submit-code', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code }),
          });
          const result = await response.json();
          if (response.ok) {
            alert('Code submitted successfully.');
            closePopup();
          }
          else {
            alert(result.message || 'Failed to submit code.');
          }
        } catch (error) {
          console.error('Error submitting code:', error);
          alert('An error occurred. Please try again.');
        }
      } else {
        alert('Please enter the code.');
      }
    }

    function closePopup() {
        document.getElementById('popup-overlay').style.display = 'none';
        document.getElementById('email-input').value = '';
        document.getElementById('code-input').value = '';
    }

function stopPropagation(event) {
    event.stopPropagation();
}
