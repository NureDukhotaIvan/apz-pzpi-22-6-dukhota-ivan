document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        alert('Не авторизовано');
        return;
    }

    const locationMap = {
        1: 'Math class',
        2: 'Second Entrance',
        3: 'Security room',
        4: 'Shelter',
        5: 'PE class',
        6: 'Canteen',
        7: 'Main Hall',
        8: 'Main Entrance',
        9: 'Concert Hall'
    };

    const groupedSensors = {};
    const section = document.querySelector('.sensor-section');

    async function loadSensors() {
        try {
            const response = await fetch('http://localhost:8000/api/iot/sensors/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) throw new Error('Помилка отримання сенсорів');

            const sensors = await response.json();
            section.innerHTML = '';
            Object.keys(groupedSensors).forEach(k => delete groupedSensors[k]);

            sensors.forEach(sensor => {
                if (!groupedSensors[sensor.location]) {
                    groupedSensors[sensor.location] = [];
                }
                groupedSensors[sensor.location].push(sensor);
            });

            renderSensors();
        } catch (err) {
            console.error('Помилка завантаження сенсорів:', err);
            alert('Не вдалося завантажити сенсори');
        }
    }

    function renderSensors() {
        section.innerHTML = '';
        Object.entries(groupedSensors).forEach(([location, sensorsAtLocation]) => {
            const groupDiv = document.createElement('div');
            groupDiv.classList.add('sensor-group');

            const locationRow = document.createElement('div');
            locationRow.classList.add('sensor-location-row');
            locationRow.innerHTML = `<strong>Локація:</strong> ${location}`;
            groupDiv.appendChild(locationRow);

            sensorsAtLocation.forEach(sensor => {
                const sensorRow = document.createElement('div');
                sensorRow.classList.add('sensor-row');
                sensorRow.innerHTML = `
                    <span>Тип: ${sensor.type}</span>
                    <span>Статус: ${sensor.status}</span>
                    <button class="delete-sensor-btn" data-id="${sensor.id}">❌</button>
                `;
                groupDiv.appendChild(sensorRow);
            });

            section.appendChild(groupDiv);
        });
    }

    document.getElementById('addSensorBtn').addEventListener('click', async () => {
        const locationId = parseInt(document.getElementById('pickSensorLocation').value);
        const statusIndex = parseInt(document.getElementById('pickSensorStatus').value);
        const typeIndex = parseInt(document.getElementById('pickSensorType').value);

        const statusMap = {
            1: 'disabled',
            2: 'active'
        };

        const typeMap = {
            1: 'fire',
            2: 'gas',
            3: 'smoke',
            4: 'temperature',
            5: 'intrusion'
        };

        const location = locationMap[locationId];
        const type = typeMap[typeIndex];
        const status = statusMap[statusIndex];

        if (!location || !type || !status) {
            alert('Будь ласка, оберіть значення в кожному полі');
            return;
        }
        const existing = groupedSensors[location] || [];
        if (existing.find(s => s.type === type)) {
            alert(`У локації "${location}" вже існує сенсор типу "${type}"`);
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/api/iot/sensors/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    location,
                    type,
                    status,
                    danger_percentage: 0
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Ошибка при создании сенсора:', errorData);
                throw new Error('Не вдалося створити сенсор');
            }

            const newSensor = await response.json();

            if (!groupedSensors[location]) {
                groupedSensors[location] = [];
            }
            groupedSensors[location].push(newSensor);
            renderSensors();
        } catch (err) {
            console.error('Помилка при створенні сенсора:', err);
            alert('Не вдалося додати сенсор');
        }
    });

    await loadSensors();

      section.addEventListener('click', async (e) => {
        if (e.target.classList.contains('delete-sensor-btn')) {
            const sensorId = e.target.dataset.id;
            const confirmed = confirm('Ви впевнені, що хочете видалити цей сенсор?');
            if (!confirmed) return;

            try {
                const response = await fetch(`http://localhost:8000/api/iot/sensors/${sensorId}/`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (!response.ok) throw new Error('Помилка видалення');

                for (const location in groupedSensors) {
                    const index = groupedSensors[location].findIndex(s => s.id == sensorId);
                    if (index !== -1) {
                        groupedSensors[location].splice(index, 1);
                        if (groupedSensors[location].length === 0) {
                            delete groupedSensors[location];
                        }
                        break;
                    }
                }

                renderSensors();
            } catch (err) {
                console.error('Помилка при видаленні сенсора:', err);
                alert('Не вдалося видалити сенсор');
            }
        }
    });
});


document.getElementById('cameraPage')?.addEventListener('click', () => {
    window.location.href = '../CamerasPage/cio.html';
});

document.getElementById('sensorPage')?.addEventListener('click', () => {
    window.location.href = '../IoTPage/iot.html';
});

document.getElementById('userPage')?.addEventListener('click', () => {
    window.location.href = '../UserPage/user.html';
});

document.getElementById('statPage')?.addEventListener('click', () => {
    window.location.href = '../StatPage/stat.html';
});
