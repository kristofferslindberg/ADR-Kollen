// Cachar appen, OCR-filerna och tabellen så att den fungerar utan täckning efter första start.
const C = "adr-kollen-v1";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon.svg", "vendor/pdf.min.js", "vendor/pdf.worker.min.js",
  "vendor/tess/tesseract.min.js", "vendor/tess/worker.min.js", "vendor/tess/tesseract-core-simd-lstm.wasm.js",
  "vendor/tess/tesseract-core-lstm.wasm.js", "vendor/tess/swe.traineddata.gz", "vendor/tess/eng.traineddata.gz"];
self.addEventListener("install", (e) => e.waitUntil(caches.open(C).then((c) => c.addAll(FILES)).then(() => self.skipWaiting())));
self.addEventListener("activate", (e) => e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== C).map((k) => caches.delete(k))))));
self.addEventListener("fetch", (e) => e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request))));
