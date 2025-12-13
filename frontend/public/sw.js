self.addEventListener('push', function (event) {
    const data = event.data.json();
    const title = data.title || 'RedAlert';
    const options = {
        body: data.body,
        icon: '/icon.png', // Fallback if no icon
        badge: '/badge.png'
    };

    event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function (event) {
    event.notification.close();
    event.waitUntil(
        clients.openWindow('http://localhost:3000/alerts')
    );
});
