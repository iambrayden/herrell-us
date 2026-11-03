var year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();

// Footer status bar: show which Cloudflare data center served this page and the
// round-trip time. /cdn-cgi/trace only exists behind Cloudflare, so local
// previews leave the status hidden.
(function () {
  var el = document.getElementById("edge");
  if (!el || !window.fetch) return;
  var start = performance.now();
  fetch("/cdn-cgi/trace", { cache: "no-store" })
    .then(function (r) { return r.ok ? r.text() : Promise.reject(); })
    .then(function (text) {
      var rtt = Math.round(performance.now() - start);
      var info = {};
      text.trim().split("\n").forEach(function (line) {
        var i = line.indexOf("=");
        if (i > 0) info[line.slice(0, i)] = line.slice(i + 1);
      });
      if (!info.colo) return;
      var parts = ["edge " + info.colo, "rtt " + rtt + " ms"];
      if (info.http) parts.push(info.http);
      if (info.tls && info.tls !== "off") parts.push(info.tls.replace("TLSv", "tls "));
      el.textContent = parts.join(" · ");
      el.hidden = false;
    })
    .catch(function () {});
})();
