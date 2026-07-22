/**
 * Dataset upload widget — XHR upload + revert + status badge.
 *
 * Lives in base.html's navbar.  Handles:
 *   - CSV file selection and XHR upload to /behavioural-analysis/upload-dataset
 *   - Revert to original dataset via /behavioural-analysis/revert-dataset
 *   - "Custom dataset active" badge with localStorage persistence
 *   - Server-side status check on page load (GET /behavioural-analysis/dataset-status)
 *   - Click-outside-to-close navbar dropdowns (with smooth animation)
 */

(function () {
  'use strict';

  var input = document.getElementById('datasetUploadInput');
  var nameEl = document.getElementById('datasetUploadFilename');
  var btn = document.getElementById('datasetUploadBtn');
  var status = document.getElementById('datasetUploadStatus');
  var validationPanel = document.getElementById('datasetUploadValidation');
  if (!input || !btn || !status || !nameEl) { return; }

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function hideValidation() {
    if (validationPanel) {
      validationPanel.hidden = true;
      validationPanel.innerHTML = '';
    }
  }

  function showValidation(html) {
    if (validationPanel) {
      validationPanel.innerHTML = html;
      validationPanel.hidden = false;
    }
  }

  var uploadEndpoint = '/behavioural-analysis/upload-dataset';
  var revertEndpoint = '/behavioural-analysis/revert-dataset';
  var statusEndpoint = '/behavioural-analysis/dataset-status';

  /* ---- toggle pill morphing --------------------------------------------
   * The navbar pill normally reads "⇪ Upload Dataset" (purple gradient).
   * When the live dataset is custom (uploaded), it morphs to "↩ Revert to
   * Original" with a red/orange gradient + gentle pulse so it's visually
   * obvious that an uploaded dataset is currently active. The caret (▾)
   * inside the pill *always* opens the panel — clicking the rest of the
   * pill in revert-mode fires the revert directly.
   * --------------------------------------------------------------------- */

  var widgetToggle = document.querySelector('#uploadWidget > .nav-upload-toggle');
  var widgetIcon = widgetToggle ? widgetToggle.querySelector('.nav-upload-toggle__icon') : null;
  var widgetLabel = widgetToggle ? widgetToggle.querySelector('.nav-upload-toggle__label') : null;
  var widgetCaret = widgetToggle ? widgetToggle.querySelector('.nav-upload-toggle__caret') : null;
  var widgetDetails = document.getElementById('uploadWidget');

  function setToggleMode(mode) {
    if (!widgetToggle) { return; }
    if (mode === 'revert') {
      if (widgetIcon)  { widgetIcon.textContent = '\u21A9'; }
      if (widgetLabel) { widgetLabel.textContent = 'Revert to Original'; }
      widgetToggle.dataset.mode = 'revert';
      widgetToggle.classList.add('nav-upload-toggle--revert');
      widgetToggle.setAttribute('title', 'Click to restore the original dataset');
    } else {
      if (widgetIcon)  { widgetIcon.textContent = '\u21EA'; }
      if (widgetLabel) { widgetLabel.textContent = 'Upload Dataset'; }
      widgetToggle.dataset.mode = '';
      widgetToggle.classList.remove('nav-upload-toggle--revert');
      widgetToggle.setAttribute('title', 'Upload a new CardsDataset-style CSV');
    }
  }

  /* Prevent the inline refresh-detection script in <head> from clobbering
     a dataset that the upload widget just installed. The cookie lives ~15
     seconds and is consumed/cleared on the next page paint. */
  function setSkipRevertCookie() {
    try { document.cookie = 'app_skip_revert=1; path=/; max-age=15; SameSite=Lax'; } catch (_) {}
  }

  // Pre-paint morph based on localStorage hint (avoids a flash of the
  // upload-style pill if the dataset is actually custom).
  try {
    if (localStorage.getItem('datasetCustom') === 'true') { setToggleMode('revert'); }
  } catch (_) {}

  /* ---- badge (Custom dataset active) ---- */

  var badge = document.getElementById('datasetActiveBadge');

  function showBadge() {
    if (badge) {
      badge.hidden = false;
      badge.textContent = '\u26A0 Custom dataset active';
    }
    setToggleMode('revert');
    try { localStorage.setItem('datasetCustom', 'true'); } catch (_) {}
  }

  function hideBadge() {
    if (badge) { badge.hidden = true; }
    setToggleMode('upload');
    try { localStorage.removeItem('datasetCustom'); } catch (_) {}
  }

  /** Check server-side whether files match .orig.bak hashes on page load. */
  function refreshBadgeFromServer() {
    if (!badge) { return; }
    try {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', statusEndpoint, true);
      xhr.timeout = 8000;
      xhr.onload = function () {
        if (xhr.status !== 200) { return; }
        var payload;
        try { payload = JSON.parse(xhr.responseText || '{}'); } catch (_) { return; }
        if (payload.is_custom) {
          showBadge();
        } else {
          hideBadge();
        }
      };
      xhr.onerror = function () {
        try {
          if (localStorage.getItem('datasetCustom') === 'true') { showBadge(); }
        } catch (_) {}
      };
      xhr.send();
    } catch (_) {}
  }

  refreshBadgeFromServer();

  /* ---- status helper ---- */

  function setStatus(kind, message) {
    status.dataset.kind = kind;
    status.textContent = message || '';
  }

  /* ---- toggle pill click routing ------------------------------------------------
   * Clicking the pill body in revert mode fires an in-place revert (with a
   * confirm dialog). Clicking the caret inside the pill — or clicking the pill
   * body in upload mode — falls through to <details>'s default behavior and
   * just opens the panel, so users can still upload a NEW file when the pill
   * is in revert mode.
   * -------------------------------------------------------------------------- */

  if (widgetToggle) {
    widgetToggle.addEventListener('click', function (ev) {
      // Carret click: let the panel open naturally.
      if (ev.target && ev.target.closest && ev.target.closest('.nav-upload-toggle__caret')) {
        return;
      }
      // Pill body in revert mode: confirm + revert + reload.
      if (widgetToggle.dataset.mode === 'revert') {
        ev.preventDefault();
        if (!confirm('Restore the original dataset?\n\nThis replaces CardsDataset.csv, card_analysis_data.json, and the blank-patterns Excel with the versions that shipped with the repository.')) {
          return;
        }
        try {
          var xhr = new XMLHttpRequest();
          xhr.open('POST', revertEndpoint, false); // sync so the page can re-render against reverted data
          xhr.send();
          var ok = (xhr.status >= 200 && xhr.status < 300);
          var payload = {};
          try { payload = JSON.parse(xhr.responseText || '{}'); } catch (_) {}
          if (ok) {
            hideBadge();
            _prepareReload('reverted');
            setSkipRevertCookie();
            window.location.reload();
          } else {
            setStatus('error', 'Revert failed: ' + (payload.error || ('HTTP ' + xhr.status)));
          }
        } catch (e) {
          setStatus('error', 'Network error during revert. Try again.');
        }
      }
    });
  }

  /* ---- file picker ---- */

  input.addEventListener('change', function () {
    var file = input.files && input.files[0];
    if (file) {
      nameEl.textContent = file.name + ' (' + Math.round(file.size / 1024) + ' KB)';
      nameEl.title = file.name;
      nameEl.classList.add('has-file');
    } else {
      nameEl.textContent = 'No file chosen';
      nameEl.title = '';
      nameEl.classList.remove('has-file');
    }
    // Belt-and-suspenders: if the OS file picker ever collapses the details
    // panel, reopen it so the user can still click "Upload & Reprocess".
    var widget = document.getElementById('uploadWidget');
    if (widget) { widget.setAttribute('open', ''); }
    setStatus('idle', '');
    hideValidation();
  });

  /* ---- upload ---- */

  btn.addEventListener('click', function () {
    hideValidation();
    var file = input.files && input.files[0];
    if (!file) {
      setStatus('error', 'Pick a .csv or .xlsx file first.');
      return;
    }
    if (!/\.(csv|xlsx)$/i.test(file.name)) {
      setStatus('error', 'Only .csv or .xlsx files are accepted.');
      return;
    }

    btn.classList.add('is-loading');
    btn.disabled = true;
    setStatus('pending', 'Uploading and re-processing ' + file.name + '\u2026');

    var form = new FormData();
    form.append('dataset', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', uploadEndpoint, true);
    xhr.timeout = 120000;
    xhr.onload = function () {
      btn.classList.remove('is-loading');
      btn.disabled = false;
      var payload = {};
      try { payload = JSON.parse(xhr.responseText || '{}'); } catch (_) { payload = {}; }

      if (xhr.status >= 200 && xhr.status < 300 && payload.ok) {
        var stats = payload.statistics || {};
        showBadge();
        var msg = 'Processed '
          + (stats.total_trials || 0) + ' trials \u2014 '
          + (stats.success_count || 0) + ' successes ('
          + (stats.success_rate || 0) + '% SR). '
          + (stats.trials_with_blank_cards || 0) + ' used blank cards. Reloading\u2026';
        setStatus('ok', msg);
        _prepareReload('uploaded');
        setSkipRevertCookie();
        setTimeout(function () { window.location.reload(); }, 1400);
      } else if (payload.missing_columns && payload.required_columns) {
        setStatus('error', 'Upload failed: ' + (payload.error || 'Missing required columns'));
        var missingList = payload.missing_columns.map(function (col) {
          return '<li><code>' + escapeHtml(col) + '</code></li>';
        }).join('');
        var requiredTags = payload.required_columns.map(function (col) {
          return '<code>' + escapeHtml(col) + '</code>';
        }).join(', ');
        showValidation(
          '<div class="nav-upload-validation__header">Missing required columns</div>' +
          '<p>The following columns are missing from your file:</p>' +
          '<ul class="nav-upload-validation__list">' + missingList + '</ul>' +
          '<p>Required columns are: ' + requiredTags + '</p>' +
          '<p class="nav-upload-validation__next">Next step: add the missing columns to your file and upload again. ' +
          'Every row must include a value for each required column.</p>'
        );
      } else {
        hideValidation();
        setStatus('error', 'Upload failed: ' + (payload.error || ('HTTP ' + xhr.status)));
      }
    };
    xhr.onerror = function () {
      btn.classList.remove('is-loading');
      btn.disabled = false;
      setStatus('error', 'Network error talking to ' + uploadEndpoint + '. Try again.');
    };
    xhr.ontimeout = function () {
      btn.classList.remove('is-loading');
      btn.disabled = false;
      setStatus('error', 'Upload timed out. Try again with a smaller CSV.');
    };
    xhr.send(form);
  });

  /* ---- click-outside-to-close navbar dropdowns (smooth) ----
   *
   * Only auto-close nav-dropdown style widgets (Insights, Research). The
   * upload widget is excluded on purpose so users can pick a file via the
   * OS dialog and still see "Upload & Reprocess" when they return.
   */

  document.addEventListener('click', function (event) {
    var navbar = document.querySelector('.navbar');
    if (!navbar) { return; }
    var openWidgets = navbar.querySelectorAll('details.nav-dropdown[open]');
    for (var i = 0; i < openWidgets.length; i++) {
      var widget = openWidgets[i];
      if (!widget.contains(event.target)) {
        widget.classList.add('nav-dropdown--closing');
        setTimeout(function(w) {
          w.removeAttribute('open');
          w.classList.remove('nav-dropdown--closing');
        }, 150, widget);
      }
    }
  });

  /* ---- revert ---- */

  var revertBtn = document.getElementById('datasetRevertBtn');
  if (revertBtn) {
    revertBtn.addEventListener('click', function () {
      if (!confirm('Restore the original dataset?\n\nThis replaces CardsDataset.csv, card_analysis_data.json, and the blank-patterns Excel with the versions that shipped with the repository.')) {
        return;
      }
      revertBtn.classList.add('is-loading');
      revertBtn.disabled = true;
      setStatus('pending', 'Restoring original dataset\u2026');

      var xhr = new XMLHttpRequest();
      xhr.open('POST', revertEndpoint, true);
      xhr.timeout = 30000;
      xhr.onload = function () {
        revertBtn.classList.remove('is-loading');
        revertBtn.disabled = false;
        var payload = {};
        try { payload = JSON.parse(xhr.responseText || '{}'); } catch (_) { payload = {}; }
        if (xhr.status >= 200 && xhr.status < 300 && payload.ok) {
          hideBadge();
          setStatus('ok', (payload.message || 'Restored.') + ' Reloading\u2026');
          _prepareReload('reverted');
          setSkipRevertCookie();
          setTimeout(function () { window.location.reload(); }, 1400);
        } else {
          setStatus('error', 'Revert failed: ' + (payload.error || ('HTTP ' + xhr.status)));
        }
      };
      xhr.onerror = function () {
        revertBtn.classList.remove('is-loading');
        revertBtn.disabled = false;
        setStatus('error', 'Network error. Try again.');
      };
      xhr.ontimeout = function () {
        revertBtn.classList.remove('is-loading');
        revertBtn.disabled = false;
        setStatus('error', 'Revert timed out. Try again.');
      };
      xhr.send();
    });
  }

  /* ---- toast + scroll restoration across reload ----
   *
   * When upload or revert completes, the page reloads after a short delay
   * so the new data paints. Use sessionStorage to:
   *   1. Remember the scroll position so the user lands back where they were.
   *   2. Tag the reload with the kind so a one-shot toast informs them
   *      that the dataset has been uploaded or restored.
   */

  function _prepareReload(kind) {
    try {
      sessionStorage.setItem('appReloadKind', kind);
      sessionStorage.setItem('appReloadScrollY', String(window.scrollY));
    } catch (_) {}
  }

  function showToast(text, kind) {
    var container = document.getElementById('app-toast-container');
    if (!container) { return; }
    var toast = document.createElement('div');
    toast.className = 'app-toast app-toast--visible app-toast--' + (kind || 'info');
    toast.textContent = text;
    container.appendChild(toast);
    setTimeout(function () {
      toast.classList.remove('app-toast--visible');
      setTimeout(function () { toast.remove(); }, 350);
    }, 3500);
  }

  // Restore scroll + show a one-shot toast if reload was triggered by an
  // upload or revert. Runs at script init on every page.
  try {
    var savedY = sessionStorage.getItem('appReloadScrollY');
    var savedKind = sessionStorage.getItem('appReloadKind');
    if (savedY !== null) {
      window.scrollTo(0, parseInt(savedY, 10));
      sessionStorage.removeItem('appReloadScrollY');
    }
    if (savedKind === 'uploaded') {
      showToast('Uploaded dataset is now active. Use Revert to restore the original.', 'info');
      sessionStorage.removeItem('appReloadKind');
    } else if (savedKind === 'reverted') {
      showToast('Restored to original dataset.', 'success');
      sessionStorage.removeItem('appReloadKind');
    }
  } catch (_) {}
})();
