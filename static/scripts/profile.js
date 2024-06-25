document.addEventListener('DOMContentLoaded', function() {
    const starsign_data = document.getElementById('starsign-data');
    let starsign = starsign_data.innerText;
    let imageUrl;

    switch(starsign.toLowerCase()) {
        case 'aries':
            imageUrl = '/static/images/starsigns/ARIES.png';
            break;
        case 'taurus':
            imageUrl = '/static/images/starsigns/TAURUS.png';
            break;
        case 'gemini':
            imageUrl = '/static/images/starsigns/GEMINI.png';
            break;
        case 'aquarius':
            imageUrl = '/static/images/starsigns/AQUARIUS.png';
            break;
        case 'pisces':
            imageUrl = '/static/images/starsigns/PISCES.png';
            break;
        case 'sagittarius':
            imageUrl = '/static/images/starsigns/SAGITTARIUS.png';
            break;
        case 'cancer':
            imageUrl = '/static/images/starsigns/CANCER.png';
            break;
        case 'libra':
            imageUrl = '/static/images/starsigns/LIBRA.png';
            break;
        case 'scorpio':
            imageUrl = '/static/images/starsigns/SCORPIO.png';
            break;
        case 'virgo':
            imageUrl = '/static/images/starsigns/VIRGO.png';
            break;
        case 'leo':
            imageUrl = '/static/images/starsigns/LEO.png';
            break;
        case 'capricorn':
            imageUrl = '/static/images/starsigns/CAPRICORN.png';
            break;
        default:
            imageUrl = 'https://via.placeholder.com/250';
    }

    document.getElementById('starsignImage').src = imageUrl;
});

document.getElementById('file-input').addEventListener('change', async function() {
    const formData = new FormData();
    const error = document.getElementById('error');
    formData.append('file', this.files[0]);

    try
    {
        const response = await fetch('/upload',
            {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                location.reload();
            }
            else if (response.status === 401)
            {
                window.location.href = '/login';
            }
            else {
                const result = await response.json();

                error.innerText = result.message || 'Failed to login.';
            }
    }

    catch (error)
    {
        console.error('Error submitting entry:', error);
        error.innerText = 'An error occurred, please try again.';
    }
});