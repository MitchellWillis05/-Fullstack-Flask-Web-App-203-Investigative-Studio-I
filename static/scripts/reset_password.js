  // this will pop session data when page is left

        window.addEventListener('beforeunload', function() {
            fetch('/clear-session')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok ' + response.statusText);
                    }
                    // Redirect to home page after clearing session
                    window.location.href = '/';
                })
                .catch(error => {
                    console.error('There has been a problem with your fetch operation:', error);
                });
        });