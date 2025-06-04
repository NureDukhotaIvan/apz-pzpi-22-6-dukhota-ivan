document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        alert('Не авторизовано');
        return;
    }

    const loadData = async () => {
        try {
            const studentsTbody = document.getElementById('studentsTbody');
            const parentsTbody = document.getElementById('parentsTbody');
            const teachersTbody = document.getElementById('teachersTbody');

            studentsTbody.innerHTML = '';
            parentsTbody.innerHTML = '';
            teachersTbody.innerHTML = '';

            const responseStudents = await fetch('http://localhost:8000/api/user/students/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const students = await responseStudents.json();
            console.log("Students:", students);

            students.forEach(student => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${student.email}</td>
                    <td>${student.first_name}</td>
                    <td>${student.last_name}</td>
                    <td>${student.date_of_birth}</td>
                    <td>${student.student_class}</td>
                    <td>${student.access_card_number}</td>
                    <td><button class="delete-btn" data-id="${student.id}" data-role="student">Видалити</button></td>
                `;
                studentsTbody.appendChild(row);
            });

            const responseParents = await fetch('http://localhost:8000/api/user/parents/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const parents = await responseParents.json();
            console.log("Parents:", parents);

            parents.forEach(parent => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${parent.email}</td>
                    <td>${parent.first_name}</td>
                    <td>${parent.last_name}</td>
                    <td>${parent.student ? parent.student.first_name + ' ' + parent.student.last_name : 'Немає студенту'}</td>
                    <td><button class="delete-btn" data-id="${parent.id}" data-role="parent">Видалити</button></td>
                `;
                parentsTbody.appendChild(row);
            });

            const responseTeachers = await fetch('http://localhost:8000/api/user/teachers/', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const teachers = await responseTeachers.json();
            console.log("Teachers:", teachers);

            teachers.forEach(teacher => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${teacher.email}</td>
                    <td>${teacher.first_name}</td>
                    <td>${teacher.last_name}</td>
                    <td>${teacher.position}</td>
                    <td>${teacher.access_card_number}</td>
                    <td><button class="delete-btn" data-id="${teacher.id}" data-role="teacher">Видалити</button></td>
                `;
                teachersTbody.appendChild(row);
            });

            document.querySelectorAll('.delete-btn').forEach(button => {
                button.addEventListener('click', async (e) => {
                    const id = e.target.getAttribute('data-id');
                    const role = e.target.getAttribute('data-role');

                    const confirmDelete = confirm('Ви точно хочете видалити цього користувача?');
                    if (confirmDelete) {
                        try {
                            let deleteUrl = '';

                            if (role === 'teacher') {
                                deleteUrl = `http://localhost:8000/api/user/teachers/${id}/`;
                            } else if (role === 'student') {
                                deleteUrl = `http://localhost:8000/api/user/students/${id}/`;
                            } else if (role === 'parent') {
                                deleteUrl = `http://localhost:8000/api/user/parents/${id}/`;
                            }

                            const response = await fetch(deleteUrl, {
                                method: 'DELETE',
                                headers: {
                                    'Authorization': `Bearer ${token}`
                                }
                            });

                            if (response.ok) {
                                alert('Запис видалено');
                                loadData();
                            } else {
                                alert('Помилка при видалені');
                            }
                        } catch (err) {
                            console.error('Error:', err);
                            alert('Не вдалося знайти запис');
                        }
                    }
                });
            });

        } catch (err) {
            console.error('Error:', err);
            alert('Не вдалося завантажити дані');
        }
    };

    loadData();

    const modal = document.getElementById("userModal");
    const openModalBtn = document.getElementById("addUser");
    const closeModalBtn = document.querySelector(".close-button");
    const roleSelect = document.getElementById("role");
    const userForm = document.getElementById("userForm");

    const roleFields = {
        student: document.getElementById("studentFields"),
        parent: document.getElementById("parentFields"),
        teacher: document.getElementById("teacherFields")
    };

    openModalBtn.addEventListener("click", () => {
        modal.style.display = "block";
    });

    closeModalBtn.addEventListener("click", () => {
        modal.style.display = "none";
        userForm.reset();
        Object.values(roleFields).forEach(div => div.classList.add("hidden"));
    });

    roleSelect.addEventListener("change", () => {
        const selectedRole = roleSelect.value;
        Object.entries(roleFields).forEach(([role, div]) => {
            const shouldShow = role === selectedRole;
            div.classList.toggle("hidden", !shouldShow);
            Array.from(div.querySelectorAll("input")).forEach(input => {
                input.disabled = !shouldShow;
            });
        });
    });

    userForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('access_token');
        const role = roleSelect.value;

        const commonData = {
            email: document.getElementById("email").value,
            password: Math.random().toString(36).slice(-8),
            first_name: document.getElementById("first_name").value,
            last_name: document.getElementById("last_name").value,
        };

        let endpoint = "";
        let body = { ...commonData };

        if (role === "student") {
            endpoint = "create-student";
            body.date_of_birth = document.getElementById("dob").value;
            body.student_class = document.getElementById("student_class").value;
            body.access_card_number = Math.floor(100000000 + Math.random() * 900000000).toString();
        } else if (role === "parent") {
            endpoint = "create-parent";
            body.student_id = document.getElementById("student_id").value;
        } else if (role === "teacher") {
            endpoint = "create-teacher";
            body.position = document.getElementById("position").value;
            body.access_card_number = Math.floor(100000000 + Math.random() * 900000000).toString();
        }

        try {
            const response = await fetch(`http://localhost:8000/api/user/${endpoint}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(body)
            });

            if (response.ok) {
                alert("Користувача додано успішно");
                modal.style.display = "none";
                userForm.reset();
                Object.values(roleFields).forEach(div => div.classList.add("hidden"));
                loadData();
            } else {
                const errData = await response.json();
                alert("Помилка: " + JSON.stringify(errData));
            }
        } catch (err) {
            console.error("Error:", err);
            alert("Помилка при додаванні користувача");
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