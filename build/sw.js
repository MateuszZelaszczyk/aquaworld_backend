const CACHE_NAME = "app1";

this.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll([
        "/static/media/TalkFish.765db5dc58917125672c.png",
        "/static/media/bg.0382e8fafd643f7d1630.jpg",
        "/static/media/Fish.5d978f1d0e7fe5779fa4.jpg",
        "/logo192.png",
        "/static/js/bundle.js",
        "/profile",
        "/profile/mainpage",
        "/profile/myaqua",
        "/index.html",
        "/",
      ]);
    })
  );
});

this.addEventListener("fetch", (event) => {
  if (!navigator.onLine) {
    event.respondWith(
      caches.match(event.request).then((response) => {
        if (response) {
          return response;
        }
      })
    );
  }
});
