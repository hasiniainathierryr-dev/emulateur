const CACHE_NAME = "htplayer-cache-v1";
const urlsToCache = ["/"]; // uniquement la page d'accueil

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    }).then(() => {
      console.log("✅ Service Worker installé !");
    }).catch(err => {
      console.error("Erreur pendant l'installation :", err);
    })
  );
});

self.addEventListener("activate", event => {
  console.log("✅ Service Worker activé !");
});

self.addEventListener("fetch", event => {
  event.respondWith(fetch(event.request));
});
