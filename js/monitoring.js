/* Three Tiny Brushes: monitoring config. Setup steps: /workspace/threetinybrushes/MONITORING.md
 * Both IDs empty = monitoring OFF: this file returns immediately and makes no network requests.
 * The DSN and the Clarity ID are public values (they end up in every visitor's browser), so it's fine to commit them. */
var SENTRY_DSN = '';   // Sentry > Settings > Projects > (project) > Client Keys (DSN), e.g. 'https://abc123@o123456.ingest.us.sentry.io/1234567'
var CLARITY_ID = '';   // Microsoft Clarity > Settings > Setup > project ID, e.g. 'abcd1234ef'
var RELEASE = 'unreleased';  // stamped with the git short sha by tools/deploy_github.sh when SENTRY_DSN is set

(function () {
  'use strict';
  if (!SENTRY_DSN && !CLARITY_ID) return;

  // Pinned Sentry browser bundle (errors only: no tracing, no replay) with Subresource Integrity.
  var SENTRY_SRC = 'https://browser.sentry-cdn.com/10.75.3/bundle.min.js';
  var SENTRY_SRI = 'sha384-jS9CKUOSAB+VN9i8uqR3dDKFThyW/VFLVW7VU8FJIEA6hwAy3aY71i329xbTIxaN';

  // Run third-party code only after the page has loaded and the browser is idle, so it never slows first paint.
  function idle(fn) { if ('requestIdleCallback' in window) requestIdleCallback(fn, { timeout: 4000 }); else setTimeout(fn, 1500); }
  function later(fn) { if (document.readyState === 'complete') idle(fn); else window.addEventListener('load', function () { idle(fn); }); }

  if (SENTRY_DSN) {
    // Keep errors that happen before the SDK arrives, then report them once it's ready.
    var early = [];
    var onError = function (e) { early.push(e.error || new Error(e.message)); };
    var onRejection = function (e) { early.push(e.reason); };
    window.addEventListener('error', onError);
    window.addEventListener('unhandledrejection', onRejection);
    later(function () {
      var s = document.createElement('script');
      s.src = SENTRY_SRC; s.integrity = SENTRY_SRI; s.crossOrigin = 'anonymous'; s.async = true;
      s.onload = function () {
        window.removeEventListener('error', onError);
        window.removeEventListener('unhandledrejection', onRejection);
        if (!window.Sentry) return;
        window.Sentry.init({
          dsn: SENTRY_DSN,
          environment: 'production',
          release: RELEASE,
          sampleRate: 1.0,          // keep every error event (low traffic site)
          // tracing off: no tracesSampleRate and this bundle has no tracing, so no performance quota is used.
          sendDefaultPii: false,
          // Dedupe is a default integration (drops repeated identical errors), so it's already on.
          allowUrls: [/https?:\/\/threetinybrushes\.github\.io/i, /https?:\/\/(www\.)?threetinybrushes\.com/i],
          denyUrls: [
            /extensions\//i, /^chrome(-extension)?:\/\//i, /^moz-extension:\/\//i, /^safari(-web)?-extension:\/\//i,
            /^webkit-masked-url:/i, /clarity\.ms/i, /fonts\.(googleapis|gstatic)\.com/i, /square(up)?\.(site|com)/i
          ],
          ignoreErrors: [
            /^Script error\.?$/,                         // cross-origin script with no details
            'ResizeObserver loop limit exceeded',
            'ResizeObserver loop completed with undelivered notifications',
            'Non-Error promise rejection captured',
            'top.GLOBALS', 'originalCreateNotification', 'canvas.contentDocument', 'MyApp_RemoveAllHighlights',
            'atomicFindClose', 'fb_xd_fixed', 'conduitPage', '__gCrWeb', 'instantSearchSDKJSBridgeClearHighlight',
            'webkitExitFullScreen', "Can't find variable: ZiteReader", 'jigsaw is not defined', 'ComboSearch is not defined'
          ]
        });
        for (var i = 0; i < early.length; i++) window.Sentry.captureException(early[i]);
        early = [];
      };
      document.head.appendChild(s);
    });
  }

  if (CLARITY_ID) {
    later(function () {
      // Official Microsoft Clarity snippet. Input masking is controlled in Clarity > Settings > Masking (keep Balanced or Strict).
      (function (c, l, a, r, i, t, y) {
        c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
        t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
        y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
      })(window, document, 'clarity', 'script', CLARITY_ID);
    });
  }
})();
