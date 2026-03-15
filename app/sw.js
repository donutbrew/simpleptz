// Simple PTZ — Service Worker
// Caches the app shell for offline use and fast reloads.
// Bump CACHE_VERSION to force a cache refresh after updates.

const CACHE_VERSION = 'simpleptz-v1';

const PRECACHE = [
  './',
  './index.html',
];

// Install: cache all app shell files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then(cache => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

// Activate: delete old caches from previous versions
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_VERSION)
          .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

// Fetch: serve from cache first, fall back to network
// For navigation requests, always try network first so updates are picked up,
// but fall back to cache if offline.
self.addEventListener('fetch', event => {
  const { request } = event;

  // Only handle same-origin requests — let camera CGI calls pass through untouched
  if (!request.url.startsWith(self.location.origin)) return;

  if (request.mode === 'navigate') {
    // Network-first for page navigations
    event.respondWith(
      fetch(request)
        .then(response => {
          // Cache the fresh copy
          const clone = response.clone();
          caches.open(CACHE_VERSION).then(cache => cache.put(request, clone));
          return response;
        })
        .catch(() => caches.match(request).then(r => r || caches.match('./')))
    );
  } else {
    // Cache-first for all other assets (fonts, scripts, etc.)
    event.respondWith(
      caches.match(request).then(cached => {
        if (cached) return cached;
        return fetch(request).then(response => {
          const clone = response.clone();
          caches.open(CACHE_VERSION).then(cache => cache.put(request, clone));
          return response;
        });
      })
    );
  }
});