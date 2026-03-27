(function () {
  const STORAGE_KEY = 'theme';
  const THEMES = ['system', 'dark', 'light'];

  function getStoredTheme() {
    try {
      const value = localStorage.getItem(STORAGE_KEY);
      return THEMES.includes(value) ? value : 'system';
    } catch {
      return 'system';
    }
  }

  function setStoredTheme(theme) {
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch {
      // ignore
    }
  }

  function applyTheme(theme) {
    const root = document.documentElement;
    if (theme === 'light' || theme === 'dark') {
      root.setAttribute('data-theme', theme);
    } else {
      root.removeAttribute('data-theme');
    }
  }

  function labelFor(theme) {
    if (theme === 'dark') return 'Theme: Dark';
    if (theme === 'light') return 'Theme: Light';
    return 'Theme: System';
  }

  function nextTheme(current) {
    const idx = THEMES.indexOf(current);
    return THEMES[(idx + 1) % THEMES.length];
  }

  function syncButtons(theme) {
    document.querySelectorAll('[data-theme-toggle]')
      .forEach((button) => {
        button.textContent = labelFor(theme);
        button.setAttribute('aria-label', labelFor(theme));
      });

    document.querySelectorAll('[data-set-theme]')
      .forEach((button) => {
        const targetTheme = button.getAttribute('data-set-theme');
        button.setAttribute('data-active', String(targetTheme === theme));
      });
  }

  function bindDropdown(theme) {
    document.querySelectorAll('[data-set-theme]')
      .forEach((button) => {
        button.addEventListener('click', () => {
          const next = button.getAttribute('data-set-theme') || 'system';
          if (!THEMES.includes(next)) return;
          setStoredTheme(next);
          applyTheme(next);
          syncButtons(next);

          const details = button.closest('details');
          if (details) details.open = false;
        });
      });

    // Ensure UI reflects theme on load
    syncButtons(theme);
  }

  function init() {
    const theme = getStoredTheme();
    applyTheme(theme);
    syncButtons(theme);

    bindDropdown(theme);

    document.querySelectorAll('[data-theme-toggle]')
      .forEach((button) => {
        button.addEventListener('click', () => {
          const current = getStoredTheme();
          const next = nextTheme(current);
          setStoredTheme(next);
          applyTheme(next);
          syncButtons(next);
        });
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
