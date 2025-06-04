document.getElementById('acceptBtn').addEventListener('click', async function () {
    const email = document.getElementById('emailInput').value;
    const password = document.getElementById('passwordInput').value;

    try {
        const response = await fetch('http://localhost:8000/api/token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            alert('Успішний вхід!');
            window.location.href = '../CamerasPage/cio.html';
        } else {
            alert('Помилка: ' + (data.detail || 'Невірні дані'));
        }
    } catch (error) {
        console.error('Помилка:', error);
        alert('Сталася помилка з’єднання.');
    }
});