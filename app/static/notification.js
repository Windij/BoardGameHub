// Функция для проигрывания звука и показа уведомления
function showNotification(message) {
    // Проигрываем звук
    const audio = new Audio('/static/sounds/notification.mp3');
    audio.play();

    // Создаем и показываем уведомление
    const notification = document.createElement('div');
    notification.className = 'site-notification';
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-bell"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove(); updateNotificationsPosition()" class="close-btn">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;

    // Находим контейнер для уведомлений или создаем новый
    let container = document.getElementById('notifications-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'notifications-container';
        container.style.position = 'fixed';
        container.style.top = '80px';
        container.style.left = '50%';
        container.style.transform = 'translateX(-50%)';
        container.style.zIndex = '1000';
        container.style.width = '90%';
        container.style.maxWidth = '600px';
        document.body.appendChild(container);
    }

    // Добавляем уведомление в контейнер
    container.appendChild(notification);

    // Удаляем уведомление через 10 секунд
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
            updateNotificationsPosition();
        }
    }, 10000);
}

// Функция для обновления позиций уведомлений
function updateNotificationsPosition() {
    const notifications = document.querySelectorAll('.site-notification');
    let topOffset = 80; // Начальное смещение от верха

    notifications.forEach((notification, index) => {
        notification.style.top = `${topOffset}px`;
        topOffset += notification.offsetHeight + 10; // 10px отступ между уведомлениями
    });
}

// Функция для проверки предстоящих встреч
function checkUpcomingGames() {
    fetch('/check_upcoming_games')
        .then(response => response.json())
        .then(data => {
            if (data.upcoming_games && data.upcoming_games.length > 0) {
                data.upcoming_games.forEach(game => {
                    showNotification(`Завтра в ${game.time} состоится встреча "${game.game_title}"!`);
                });
            }
        })
        .catch(error => console.error('Ошибка при проверке встреч:', error));
}

// Проверяем встречи каждый час (3600000 мс)
setInterval(checkUpcomingGames, 3600000);

// Проверяем сразу при загрузке страницы
document.addEventListener('DOMContentLoaded', checkUpcomingGames); 