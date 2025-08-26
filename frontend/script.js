const API_BASE = '/api';  // Usar ruta relativa

// Elementos del DOM
let currentUser = null;

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    loadGuides();
    
    // Event listeners
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    document.getElementById('uploadForm').addEventListener('submit', handleUpload);
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);
});

// Verificar estado de autenticación
async function checkAuthStatus() {
    try {
        const token = localStorage.getItem('authToken');
        if (!token) return;
        
        const response = await fetch(`${API_BASE}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const user = await response.json();
            currentUser = user;
            showAdminPanel(user.role);
        }
    } catch (error) {
        console.error('Error verificando autenticación:', error);
        localStorage.removeItem('authToken');
    }
}

// Manejar inicio de sesión
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('authToken', data.token);
            currentUser = data.user;
            showAdminPanel(data.user.role);
            document.getElementById('loginForm').reset();
            loadGuides(); // Recargar las guías después de login
        } else {
            const error = await response.json();
            alert(`Error: ${error.message}`);
        }
    } catch (error) {
        console.error('Error en login:', error);
        alert('Error de conexión con el servidor');
    }
}

// Mostrar panel de administración
function showAdminPanel(role) {
    document.getElementById('loginSection').style.display = 'none';
    document.getElementById('adminPanel').style.display = 'block';
    document.getElementById('userRole').textContent = `Usuario: ${role}`;
}

// Manejar cierre de sesión
function handleLogout() {
    localStorage.removeItem('authToken');
    currentUser = null;
    document.getElementById('adminPanel').style.display = 'none';
    document.getElementById('loginSection').style.display = 'block';
    document.getElementById('loginForm').reset();
    loadGuides(); // Recargar las guías después de logout
}

// Cargar guías desde el servidor
async function loadGuides() {
    try {
        const response = await fetch(`${API_BASE}/guides`);
        if (response.ok) {
            const guides = await response.json();
            displayGuides(guides);
        }
    } catch (error) {
        console.error('Error cargando guías:', error);
    }
}

// Mostrar guías en la interfaz
function displayGuides(guides) {
    const categoriesContainer = document.querySelector('.categories');
    categoriesContainer.innerHTML = '';
    
    const categories = {
        'HOB': 'Guías HOB',
        'AWS': 'Guías AWS',
        'WINDOWS': 'Guías WINDOWS',
        'LINUX': 'Guías LINUX',
        'CBB': 'Guías CBB'
    };
    
    for (const [categoryId, categoryName] of Object.entries(categories)) {
        const categoryGuides = guides.filter(g => g.category === categoryId);
        
        const categoryElement = document.createElement('div');
        categoryElement.className = 'category';
        categoryElement.innerHTML = `
            <h3>${categoryName}</h3>
            <ul class="guides-list" id="${categoryId.toLowerCase()}-guides">
                ${categoryGuides.map(guide => `
                    <li>
                        <a href="${API_BASE}/guides/${guide.id}/download" target="_blank">${guide.name}</a>
                        ${currentUser ? `<button class="delete-btn" onclick="deleteGuide('${guide.id}')">Eliminar</button>` : ''}
                    </li>
                `).join('')}
                ${categoryGuides.length === 0 ? '<li>No hay guías disponibles</li>' : ''}
            </ul>
        `;
        
        categoriesContainer.appendChild(categoryElement);
    }
}

// Manejar subida de archivos
async function handleUpload(e) {
    e.preventDefault();
    
    if (!currentUser) {
        alert('Debe iniciar sesión para subir archivos');
        return;
    }
    
    const name = document.getElementById('guideName').value;
    const category = document.getElementById('guideCategory').value;
    const fileInput = document.getElementById('guideFile');
    const file = fileInput.files[0];
    
    if (!name || !category || !file) {
        alert('Por favor complete todos los campos');
        return;
    }
    
    const formData = new FormData();
    formData.append('name', name);
    formData.append('category', category);
    formData.append('file', file);
    
    try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE}/guides`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        if (response.ok) {
            alert('Guía subida exitosamente');
            document.getElementById('uploadForm').reset();
            loadGuides();
        } else {
            const error = await response.json();
            alert(`Error: ${error.message}`);
        }
    } catch (error) {
        console.error('Error subiendo archivo:', error);
        alert('Error de conexión con el servidor');
    }
}

// Eliminar una guía
async function deleteGuide(guideId) {
    if (!confirm('¿Está seguro de que desea eliminar esta guía?')) {
        return;
    }
    
    try {
        const token = localStorage.getItem('authToken');
        const response = await fetch(`${API_BASE}/guides/${guideId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            alert('Guía eliminada exitosamente');
            loadGuides();
        } else {
            const error = await response.json();
            alert(`Error: ${error.message}`);
        }
    } catch (error) {
        console.error('Error eliminando guía:', error);
        alert('Error de conexión con el servidor');
    }
}

// Hacer funciones globales para los onclick
window.deleteGuide = deleteGuide;
