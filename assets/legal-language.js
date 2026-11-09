(() => {
  'use strict';
  const key = 'autocontract-language';
  const current = document.documentElement.lang === 'en' ? 'en' : 'ro';
  const explicit = new URLSearchParams(location.search).get('lang');
  let remembered;
  try { remembered = localStorage.getItem(key); } catch (_) { /* Storage may be unavailable. */ }
  const fixedLanguage = document.documentElement.hasAttribute('data-fixed-language');
  const preferred = fixedLanguage ? current : ['ro', 'en'].includes(explicit) ? explicit : (['ro', 'en'].includes(remembered) ? remembered : current);
  if (['ro', 'en'].includes(explicit)) {
    try { localStorage.setItem(key, explicit); } catch (_) { /* Navigation still works. */ }
  }
  if (preferred !== current) {
    const path = location.pathname.replace(/^\/en\//, '/');
    location.replace((preferred === 'en' ? '/en' : '') + path + location.hash);
    return;
  }
  document.querySelectorAll('[data-language]').forEach(link => {
    link.addEventListener('click', () => {
      try { localStorage.setItem(key, link.dataset.language); } catch (_) { /* Plain links are the fallback. */ }
    });
  });
})();
