document.addEventListener('DOMContentLoaded', function() {
    // Simulación de base de datos en localStorage
    if(!localStorage.getItem('citas')) {
        localStorage.setItem('citas', JSON.stringify([]));
    }

    // Cargar citas existentes
    loadAppointments();

    // Manejar envío del formulario
    document.getElementById('appointment-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Obtener datos del formulario
        const appointment = {
            nombres: document.getElementById('nombres').value,
            apellidos: document.getElementById('apellidos').value,
            email: document.getElementById('email').value,
            telefono: document.getElementById('telefono').value,
            tratamiento: document.getElementById('tratamiento').value,
            sede: document.getElementById('sede').value,
            fecha: document.getElementById('fecha').value,
            hora: document.getElementById('hora').value,
            tipoPaciente: document.getElementById('tipo-paciente').value,
            edad: document.getElementById('edad').value,
            timestamp: new Date().getTime()
        };

        // Guardar en la "base de datos" (localStorage)
        const citas = JSON.parse(localStorage.getItem('citas'));
        citas.push(appointment);
        localStorage.setItem('citas', JSON.stringify(citas));

        // Mostrar mensaje y recargar lista
        alert('Cita agendada exitosamente');
        this.reset();
        loadAppointments();
    });

    // Manejar cierre de sesión
    document.getElementById('logout-btn').addEventListener('click', function() {
        // Aquí normalmente se limpiaría la sesión del usuario
        // Redirigir a login
        window.location.href = "login.html";
    });

    // Función para cargar citas
    function loadAppointments() {
        const citas = JSON.parse(localStorage.getItem('citas'));
        const listContainer = document.getElementById('appointments-list');
        listContainer.innerHTML = '';

        if(citas.length === 0) {
            listContainer.innerHTML = '<p>No hay citas programadas</p>';
            return;
        }

        citas.forEach(cita => {
            const citaElement = document.createElement('div');
            citaElement.className = 'appointment-item';
            citaElement.innerHTML = `
                <p><strong>Fecha:</strong> ${formatDate(cita.fecha)}</p>
                <p><strong>Hora:</strong> ${cita.hora}</p>
                <p><strong>Tratamiento:</strong> ${getTreatmentName(cita.tratamiento)}</p>
                <p><strong>Sede:</strong> ${getSedeName(cita.sede)}</p>
                <button class="btn-delete" data-id="${cita.timestamp}">Eliminar</button>
            `;
            listContainer.appendChild(citaElement);
        });

        // Agregar eventos a botones de eliminar
        document.querySelectorAll('.btn-delete').forEach(btn => {
            btn.addEventListener('click', function() {
                const timestamp = parseInt(this.getAttribute('data-id'));
                deleteAppointment(timestamp);
            });
        });
    }

    // Función para eliminar cita
    function deleteAppointment(timestamp) {
        let citas = JSON.parse(localStorage.getItem('citas'));
        citas = citas.filter(cita => cita.timestamp !== timestamp);
        localStorage.setItem('citas', JSON.stringify(citas));
        loadAppointments();
    }

    // Funciones auxiliares
    function formatDate(dateString) {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString('es-ES', options);
    }

    function getTreatmentName(code) {
        const treatments = {
            'blanqueamiento': 'Blanqueamiento Dental',
            'ortodoncia': 'Ortodoncia',
            'limpieza': 'Limpieza Dental',
            'extraccion': 'Extracción'
        };
        return treatments[code] || code;
    }

    function getSedeName(code) {
        const sedes = {
            'bello': 'Bello',
            'poblado': 'Poblado',
            'laureles': 'Laureles'
        };
        return sedes[code] || code;
    }
});