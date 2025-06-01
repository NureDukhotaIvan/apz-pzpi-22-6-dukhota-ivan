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

const token = localStorage.getItem('access_token');
const output = document.querySelector('.data-output');

function fetchAndDisplay(url) {
    fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(res => {
        if (!res.ok) throw new Error(`HTTP error ${res.status}`);
        return res.json();
    })
    .then(data => {
        output.textContent = formatData(data);
    })
    .catch(error => {
        output.textContent = `Ошибка: ${error.message}`;
    });
}

document.getElementById('SEI').addEventListener('click', () => {
    fetchAndDisplay('http://localhost:8000/api/blogic/sei/');
});

document.getElementById('incidentStat').addEventListener('click', () => {
    fetchAndDisplay('http://localhost:8000/api/blogic/incident-stats/');
});

document.getElementById('DBBackup').addEventListener('click', () => {
    fetch('http://localhost:8000/api/blogic/backup/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    })
    .then(res => {
        if (!res.ok) throw new Error(`HTTP error ${res.status}`);
        return res.json();
    })
    .then(data => {
        output.textContent = formatData(data);
    })
    .catch(error => {
        output.textContent = `Ошибка: ${error.message}`;
    });
});

function formatData(data, indent = 0) {
    const pad = ' '.repeat(indent);
    let result = '';

    if (Array.isArray(data)) {
        data.forEach((item, index) => {
            result += `${pad}- ${formatData(item, indent + 2)}\n`;
        });
    } else if (typeof data === 'object' && data !== null) {
        for (const key in data) {
            const value = data[key];
            if (typeof value === 'object') {
                result += `${pad}${key}:\n${formatData(value, indent + 2)}`;
            } else {
                result += `${pad}${key}: ${value}\n`;
            }
        }
    } else {
        result += `${pad}${data}\n`;
    }

    return result;
}

document.getElementById("report").addEventListener("click", async () => {
  try {
    const response = await fetch("http://localhost:8000/api/blogic/report/", {
      method: "GET",
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error("Помилка при завантаженні звіту");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "incident_report.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();

    window.URL.revokeObjectURL(url);
  } catch (error) {
    alert("Не вдалося завантажити звіт: " + error.message);
  }
});