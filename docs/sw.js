// Cachar appen så att den fungerar utan täckning. Sidan hämtas från nätet först (så att nya
// versioner kommer fram), övriga filer från cachen. Byt C vid ändrade vendor-filer.
const C = "adr-kollen-v2";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon.svg", "vendor/pdf.min.js", "vendor/pdf.worker.min.js",
  "vendor/tess/tesseract.min.js", "vendor/tess/worker.min.js", "vendor/tess/tesseract-core-simd-lstm.wasm.js",
  "vendor/tess/tesseract-core-lstm.wasm.js", "vendor/tess/swe.traineddata.gz", "vendor/tess/eng.traineddata.gz"];
self.addEventListener("install", (e) => e.waitUntil(caches.open(C).then((c) => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener("activate", (e) => e.waitUntil(caches.keys()
  .then((ks) => Promise.all(ks.filter((k) => k !== C).map((k) => caches.delete(k)))).then(() => self.clients.claim())));
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  if (e.request.mode === "navigate") {
    e.respondWith(fetch(e.request).then((r) => {
      const copy = r.clone(); caches.open(C).then((c) => c.put("index.html", copy)); return r;
    }).catch(() => caches.match("index.html")));
    return;
  }
  e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request)));
});
