const CACHE_NAME = 'health-pwa-v1';
const urlsToCache = [
  '/',
  '/static/style.css', // Add your static CSS or JS files here
  '/static/generated-icon.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
