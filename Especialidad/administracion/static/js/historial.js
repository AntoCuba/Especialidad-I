document.addEventListener('DOMContentLoaded', function() {
    const timelineContainer = document.getElementById('timeline-container');

    function getIconClass(action) {
        if (action.startsWith('Agregó')) {
            return 'add';
        } else if (action.startsWith('Editó')) {
            return 'edit';
        } else if (action.startsWith('Eliminó')) {
            return 'delete';
        } else if (action === 'Login' || action === 'Inició sesión') {
            return 'login';
        } else if (action === 'Logout' || action === 'Cerró sesión') {
            return 'logout';
        } else if (action.startsWith('Actualizó')) {
            return 'update';
        } else if (action.startsWith('Autorizó')) {
            return 'authorize';
        } else {
            return 'info';
        }
    }

    function fetchActivityLogs() {
        fetch(apiActivityLogsUrl)
            .then(response => response.json())
            .then(data => {
                timelineContainer.innerHTML = '';
                data.logs.forEach((item, index) => {
                    console.log('Activity action:', item.action, 'Mapped iconClass:', getIconClass(item.action));
                    const iconClass = getIconClass(item.action);
                    const timelineItem = document.createElement('div');
                    timelineItem.classList.add('timeline-item');
                    
                    const iconDiv = document.createElement('div');
                    iconDiv.className = 'timeline-icon ' + iconClass;
                    if(['edit', 'delete', 'add', 'login', 'logout'].includes(iconClass)) {
                        const img = document.createElement('img');
                        let imgSrc = '';
                        let imgAlt = '';
                        switch(iconClass) {
                            case 'edit':
                                imgSrc = iconImages.edit;
                                imgAlt = 'Editar';
                                break;
                            case 'delete':
                                imgSrc = iconImages.delete;
                                imgAlt = 'Eliminar';
                                break;
                            case 'add':
                                imgSrc = iconImages.add;
                                imgAlt = 'Agregar';
                                break;
                            case 'login':
                                imgSrc = iconImages.login;
                                imgAlt = 'Inició sesión';
                                break;
                            case 'logout':
                                imgSrc = iconImages.logout;
                                imgAlt = 'Cerró sesión';
                                break;
                        }
                        img.src = imgSrc;
                        img.alt = imgAlt;
                        img.style.width = '24px';
                        img.style.height = '24px';
                        iconDiv.appendChild(img);
                    } else if(['update', 'authorize'].includes(iconClass)) {
                        const icon = document.createElement('i');
                        let iconClassName = '';
                        switch(iconClass) {
                            case 'update':
                                iconClassName = 'fas fa-sync-alt';
                                break;
                            case 'authorize':
                                iconClassName = 'fas fa-check-circle';
                                break;
                        }
                        icon.className = iconClassName;
                        iconDiv.appendChild(icon);
                    } else {
                        const icon = document.createElement('i');
                        icon.className = iconClass;
                        iconDiv.appendChild(icon);
                    }

                    const contentDiv = document.createElement('div');
                    contentDiv.className = 'timeline-content';

                    const dateDiv = document.createElement('div');
                    dateDiv.className = 'timeline-date';
                    dateDiv.textContent = item.timestamp;

                    const userDiv = document.createElement('div');
                    userDiv.className = 'timeline-user';
                    userDiv.textContent = item.user;

                    const actionDiv = document.createElement('div');
                    actionDiv.className = 'timeline-action';
                    actionDiv.textContent = item.action + (item.description ? ': ' + item.description : '');

                    contentDiv.appendChild(dateDiv);
                    contentDiv.appendChild(userDiv);
                    contentDiv.appendChild(actionDiv);

                    timelineItem.appendChild(iconDiv);
                    timelineItem.appendChild(contentDiv);

                    timelineContainer.appendChild(timelineItem);
                });
            })
            .catch(error => {
                console.error('Error fetching activity logs:', error);
            });
    }

    // Refresh del Historial cada 1 minuto
    fetchActivityLogs();
    setInterval(() => fetchActivityLogs(), 60000);
});
