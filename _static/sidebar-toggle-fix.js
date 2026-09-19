/*
 * Make the "Toggle primary sidebar" button work again.
 *
 * Two separate faults in the shipped theme, both confirmed against the live site:
 *
 * 1. sphinx-book-theme.js binds its handler with document.querySelector(".primary-toggle"),
 *    which takes the FIRST match. This build renders two elements with that class: the
 *    pydata navbar icon, which is hidden above 992px, and the button a desktop reader
 *    actually sees. The handler therefore lands on the invisible one, and clicking the
 *    visible button does nothing at all.
 *
 * 2. Even when the theme's class does get applied, its own rule
 *    @media (min-width: 992px) { .bd-sidebar-primary.pst-sidebar-hidden { visibility: hidden } }
 *    does not take effect in the built site: the element matches the selector, the media
 *    query matches, and the computed visibility stays "visible".
 *
 * So this binds to every toggle and hides the sidebar with a class of our own, defined in
 * sidebar-toggle-fix.css, rather than depending on the theme's rule.
 *
 * Written to be harmless if either fault is fixed upstream. The theme registers its own
 * capture-phase listener first and calls stopImmediatePropagation, so on any element it has
 * already claimed, its handler runs and ours never fires.
 */
(function () {
  "use strict";

  var HIDDEN = "sbt-primary-sidebar-hidden";
  var KEY = "sbt-primary-sidebar-collapsed";
  var DESKTOP = "(min-width: 992px)";

  function isDesktop() {
    return window.matchMedia(DESKTOP).matches;
  }

  function apply(collapsed) {
    document.documentElement.classList.toggle(HIDDEN, collapsed);
    document.querySelectorAll(".primary-toggle").forEach(function (btn) {
      btn.setAttribute("aria-expanded", collapsed ? "false" : "true");
    });
  }

  function ready(fn) {
    if (document.readyState !== "loading") {
      fn();
    } else {
      document.addEventListener("DOMContentLoaded", fn);
    }
  }

  ready(function () {
    var toggles = document.querySelectorAll(".primary-toggle");
    if (!toggles.length || !document.querySelector(".bd-sidebar-primary")) {
      return;
    }

    // Restore the reader's last choice, but only on desktop. Below 992px the sidebar is an
    // off-canvas panel that the theme opens and closes itself, and a stored collapse would
    // leave a phone reader with no navigation and no way to get it back.
    var stored = false;
    try {
      stored = window.localStorage.getItem(KEY) === "1";
    } catch (e) {
      stored = false;
    }
    if (stored && isDesktop()) {
      apply(true);
    }

    toggles.forEach(function (btn) {
      btn.addEventListener(
        "click",
        function (ev) {
          if (!isDesktop()) {
            // Below 992px the theme opens the sidebar as an off-canvas <dialog>. Both
            // sphinx-book-theme and pydata-sphinx-theme wire that up with
            // querySelector(".primary-toggle"), taking the FIRST match. Measured on the
            // live site at a 384px viewport: the first match is the .pst-navbar-icon
            // button, and it is display:none at EVERY width, mobile included. The button
            // a phone reader actually taps is the second one, which no theme handler is
            // attached to. So on mobile the tap reached nothing at all.
            //
            // Forward it to the element the theme did bind, rather than reimplementing
            // the dialog logic here. That reuses the theme's own content move, showModal,
            // and focus restore, so this keeps working if the theme changes them.
            var bound = document.querySelector(".primary-toggle");
            if (!bound || btn === bound) {
              return; // already the bound element; the theme's handler will run
            }
            ev.preventDefault();
            ev.stopImmediatePropagation();
            bound.click();
            return;
          }
          ev.preventDefault();
          ev.stopImmediatePropagation();
          var collapsed = !document.documentElement.classList.contains(HIDDEN);
          apply(collapsed);
          try {
            window.localStorage.setItem(KEY, collapsed ? "1" : "0");
          } catch (e) {
            /* private browsing, or storage disabled: the toggle still works for this page */
          }
        },
        true
      );
    });

    // Crossing the breakpoint with the sidebar collapsed would hide the off-canvas panel
    // too, so the collapse is dropped on the way down and restored on the way back up.
    var mq = window.matchMedia(DESKTOP);
    var onChange = function () {
      if (!mq.matches) {
        document.documentElement.classList.remove(HIDDEN);
      } else {
        try {
          apply(window.localStorage.getItem(KEY) === "1");
        } catch (e) {
          /* ignore */
        }
      }
    };
    if (mq.addEventListener) {
      mq.addEventListener("change", onChange);
    } else if (mq.addListener) {
      mq.addListener(onChange);
    }
  });
})();
