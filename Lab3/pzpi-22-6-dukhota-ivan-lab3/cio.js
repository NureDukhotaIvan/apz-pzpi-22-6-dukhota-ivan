const resources = {
  en: {
    translation: {
      admin_panel: 'Admin Panel "SchoolDef"',
      cameras: 'Cameras',
      sensors: 'Sensors',
      users: 'Users',
      stats: 'Statistics',
      settings: 'Settings',
      camera_control: 'Camera Control',
      add_camera: 'Add new camera',
      choose_location: 'Choose location:',
      choose_status: 'Choose status:',
      status_disabled: 'Disabled',
      status_active: 'Active',
      add_btn: 'Add',

      loc_math: 'Math class',
      loc_entrance2: 'Second Entrance',
      loc_secroom: 'Security room',
      loc_shelter: 'Shelter',
      loc_pe: 'PE class',
      loc_canteen: 'Canteen',
      loc_hall: 'Main Hall',
      loc_entrance: 'Main Entrance',
      loc_concert: 'Concert Hall'
    }
  },
  uk: {
    translation: {
      admin_panel: 'Адміністративна панель "SchoolDef"',
      cameras: 'Камери',
      sensors: 'Сенсори',
      users: 'Користувачі',
      stats: 'Статистика',
      settings: 'Налаштування',
      camera_control: 'Контролювання камер',
      add_camera: 'Додайте нову камеру',
      choose_location: 'Оберіть локацію:',
      choose_status: 'Оберіть статус:',
      status_disabled: 'Вимкнено',
      status_active: 'Активно',
      add_btn: 'Додати',

      loc_math: 'Клас математики',
      loc_entrance2: 'Другий вхід',
      loc_secroom: 'Охоронна кімната',
      loc_shelter: 'Укриття',
      loc_pe: 'Клас фізкультури',
      loc_canteen: 'Їдальня',
      loc_hall: 'Головна зала',
      loc_entrance: 'Головний вхід',
      loc_concert: 'Концертна зала'
    }
  }
};

i18next.init({
  lng: 'en',
  debug: false,
  resources
}, function(err, t) {
  updateContent();
});

function updateContent() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    el.textContent = i18next.t(key);
  });
}

document.getElementById('settingsBtn').addEventListener('click', () => {
  const menu = document.getElementById('languageMenu');
  menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
});

document.querySelectorAll('.langBtn').forEach(btn => {
  btn.addEventListener('click', () => {
    const lang = btn.getAttribute('data-lang');
    i18next.changeLanguage(lang, () => {
      updateContent();
      document.getElementById('languageMenu').style.display = 'none';
    });
  });
});


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

    try {
        const response = await fetch('http://localhost:8000/api/iot/cameras/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error('Ошибка получения данных');

        const cameras = await response.json();
        const section = document.querySelector('.camera-section');
        section.innerHTML = '';

        cameras.forEach(camera => {
            const div = document.createElement('div');
            div.classList.add('camera-item');
            div.innerHTML = `
                <div class="camera-item-top">
                    <p>${camera.location}</p>
                    <button class="delete-btn" data-camera-id="${camera.id}">❌</button>
                </div>
                <div class="camera-item-bottom"></div>
            `;
            section.appendChild(div);
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const cameraId = e.target.getAttribute('data-camera-id');
                const confirmation = confirm('Ви точно хочете видалити камеру? Ця дія буде незворотня.');

                if (confirmation) {
                    try {
                        const deleteResponse = await fetch(`http://localhost:8000/api/iot/cameras/${cameraId}/`, {
                            method: 'DELETE',
                            headers: {
                                'Authorization': `Bearer ${token}`
                            }
                        });

                        if (deleteResponse.ok) {
                            alert('Камера видалена');
                            location.reload();
                        } else {
                            const errorData = await deleteResponse.json();
                            alert('Ошибка: ' + (errorData.detail || 'Не удалось удалить камеру'));
                        }
                    } catch (err) {
                        console.error('Delete error:', err);
                        alert('Ошибка при удалении камеры');
                    }
                }
            });
        });

    } catch (err) {
        console.error('Fetch error:', err);
        alert('Не вдалося завантажити камери');
    }

    document.querySelector('.manage-section-row5 button').addEventListener('click', async () => {
        const locationVal = parseInt(document.getElementById('pickCameraLocation').value);
        const statusVal = parseInt(document.getElementById('pickCameraStatus').value);

        const locationStr = locationMap[locationVal];
        const statusStr = statusVal === 2 ? 'active' : 'disabled';

        if (!locationStr || !statusStr) {
            alert('Оберіть локацію та статус!');
            return;
        }

        try {
            const checkResponse = await fetch('http://localhost:8000/api/iot/cameras/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!checkResponse.ok) throw new Error('Помилка при перевірці камер');

            const existingCameras = await checkResponse.json();
            const locationAlreadyUsed = existingCameras.some(cam => cam.location === locationStr);

            if (locationAlreadyUsed) {
                alert(`Камера для локації "${locationStr}" вже існує`);
                return;
            }
            const response = await fetch('http://localhost:8000/api/iot/cameras/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ location: locationStr, status: statusStr })
            });

            if (response.ok) {
                alert('Камеру додано!');
                location.reload();
            } else {
                const errorData = await response.json();
                alert('Помилка: ' + (errorData.detail || 'Не вдалося додати камеру'));
            }

        } catch (err) {
            console.error('POST error:', err);
            alert('Помилка при додаванні камери');
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
