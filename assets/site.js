/* Progressive enhancement only: all copy, pricing, links and FAQ work without JavaScript. */
(() => {
  "use strict";

  const root = document.documentElement;
  const storageKey = "autocontract-language";
  const locale = root.lang === "en" ? "en" : "ro";
  let preferred;
  try { preferred = localStorage.getItem(storageKey); } catch { /* Storage may be disabled. */ }
  const url = new URL(window.location.href);
  const explicit = url.searchParams.get("lang");
  if (!explicit && locale === "ro" && preferred === "en" && /^\/(?:index\.html)?$/.test(url.pathname)) {
    window.location.replace(`/en/${url.hash}`);
    return;
  }
  try { localStorage.setItem(storageKey, locale); } catch { /* Normal navigation still works. */ }
  if (explicit === "ro" || explicit === "en") {
    url.searchParams.delete("lang");
    window.history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);
  }
  document.querySelectorAll("[data-language]").forEach(link => {
    link.addEventListener("click", () => {
      try { localStorage.setItem(storageKey, link.dataset.language); } catch { /* Optional preference. */ }
    });
  });

  root.classList.add("js");
  const menuButton = document.querySelector(".menu-toggle");
  const navigation = document.querySelector(".main-nav");
  if (menuButton && navigation) {
    menuButton.hidden = false;
    const close = () => {
      menuButton.setAttribute("aria-expanded", "false");
      navigation.classList.remove("is-open");
    };
    menuButton.addEventListener("click", () => {
      const open = menuButton.getAttribute("aria-expanded") !== "true";
      menuButton.setAttribute("aria-expanded", String(open));
      navigation.classList.toggle("is-open", open);
    });
    navigation.querySelectorAll("a").forEach(link => link.addEventListener("click", close));
    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
        close();
        menuButton.focus();
      }
    });
    document.addEventListener("click", event => {
      if (!navigation.contains(event.target) && !menuButton.contains(event.target)) close();
    });
    const desktop = window.matchMedia("(min-width: 641px)");
    desktop.addEventListener?.("change", close);
  }

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (!reducedMotion.matches && "IntersectionObserver" in window) {
    root.classList.add("has-reveal");
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.06 });
    document.querySelectorAll("[data-reveal]").forEach(element => observer.observe(element));
    reducedMotion.addEventListener?.("change", event => {
      if (event.matches) {
        observer.disconnect();
        root.classList.remove("has-reveal");
      }
    });
  }
})();
