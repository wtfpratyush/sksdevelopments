/* SKS Developments — shared script for every page.
   Each block checks that its section exists, so the same file runs on the
   home page and on the inner pages (about, process, projects, …). */
(() => {
  const $ = (s, c = document) => (c ? c.querySelector(s) : null);
  const $$ = (s, c = document) => (c ? [...c.querySelectorAll(s)] : []);
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- first-visit loader (home page only) ---------- */
  const loader = $('.loader');
  if (document.documentElement.classList.contains('is-loading')) {
    if (!loader) {
      document.documentElement.classList.remove('is-loading');
    } else {
      const count = $('.loader__count', loader);
      const status = $('.loader__status', loader);
      const steps = ['Laying foundations', 'Raising structure', 'Fitting out', 'Handing over keys'];
      const DURATION = 2600;
      const start = performance.now();
      let pageReady = document.readyState === 'complete';
      window.addEventListener('load', () => { pageReady = true; });
      const finish = () => {
        loader.classList.add('is-done');
        // let the hero start its intro while the curtain lifts
        setTimeout(() => document.documentElement.classList.remove('is-loading'), 650);
        try { localStorage.setItem('sks-visited', '1'); } catch (e) { /* storage off: loader shows again next time */ }
      };
      const tick = (now) => {
        const t = Math.min((now - start) / DURATION, 1);
        // ease-out, but hold at 96% until the page (hero photo) has loaded, max 5s
        let p = 1 - Math.pow(1 - t, 3);
        if (!pageReady && now - start < 5000) p = Math.min(p, 0.96);
        loader.style.setProperty('--p', p.toFixed(3));
        count.textContent = String(Math.round(p * 100)).padStart(3, '0');
        status.textContent = steps[Math.min(steps.length - 1, Math.floor(p * steps.length))];
        if (p < 1) requestAnimationFrame(tick); else setTimeout(finish, 250);
      };
      requestAnimationFrame(tick);
    }
  }

  /* ---------- header on scroll + phone tab bar ---------- */
  const header = $('.header');
  const tabbar = $('.tabbar');
  let lastY = window.scrollY;
  let headTick = false;
  const onScroll = () => {
    headTick = false;
    const y = window.scrollY;
    header?.classList.toggle('is-scrolled', y > 40);
    // tab bar: hidden at the very top and once the footer comes into view
    const footer = $('.footer');
    const nearFooter = footer && footer.getBoundingClientRect().top < window.innerHeight - 40;
    tabbar?.classList.toggle('is-away', y < 60 || nearFooter);
    // hide while scrolling down past the top, show again on any scroll up
    if (header) {
      if (y > lastY + 4 && y > 500 && !document.body.classList.contains('menu-open')) header.classList.add('is-hidden');
      else if (y < lastY - 4 || y <= 500) header.classList.remove('is-hidden');
      const max = document.documentElement.scrollHeight - window.innerHeight;
      header.style.setProperty('--progress', max > 0 ? (y / max).toFixed(4) : 0);
    }
    lastY = y;
  };
  onScroll();
  window.addEventListener('scroll', () => {
    if (!headTick) { headTick = true; requestAnimationFrame(onScroll); }
  }, { passive: true });

  // slide the tab bar's glow pill under the active tab
  function moveGlow() {
    const glow = $('.tabbar__glow');
    const cur = $('.tabbar a.is-current');
    if (!glow) return;
    glow.style.opacity = cur ? '1' : '0';
    if (!cur) return;
    glow.style.setProperty('--x', cur.offsetLeft + 'px');
    glow.style.setProperty('--w', cur.offsetWidth + 'px');
  }
  moveGlow();
  window.addEventListener('resize', moveGlow);

  /* ---------- hero: building in front of the big word (home) ----------
     The outline is traced on images/hero-building.webp (1672 × 941 px), mapped
     onto the screen the same way `object-fit: cover` places the photo, then
     used as the clip-path of the front copy. */
  const front = $('.hero__front');
  const frontImg = $('img', front);
  if (front && frontImg) {
    const BUILDING = [
      [667, 411], [1336, 282], [1476, 388], [1476, 398], [1438, 402],
      [1438, 941], [660, 941], [660, 488], [755, 475], [755, 452], [667, 423],
    ];
    const fitFront = () => {
      const iw = frontImg.naturalWidth || 1672;
      const ih = frontImg.naturalHeight || 941;
      const W = front.clientWidth;
      const H = front.clientHeight;
      const [px, py] = getComputedStyle(frontImg).objectPosition
        .split(' ').map((v) => parseFloat(v) / 100);
      const scale = Math.max(W / iw, H / ih);
      const dx = (W - iw * scale) * px;
      const dy = (H - ih * scale) * py;
      front.style.clipPath = `polygon(${BUILDING
        .map(([x, y]) => `${(x * scale + dx).toFixed(1)}px ${(y * scale + dy).toFixed(1)}px`)
        .join(', ')})`;
    };
    if (frontImg.complete) fitFront(); else frontImg.addEventListener('load', fitFront);
    frontImg.addEventListener('error', () => { front.hidden = true; });
    new ResizeObserver(fitFront).observe(front);
  }

  /* ---------- hero parallax (home hero and page heroes) ---------- */
  const heroCard = $('.hero__card') || $('.page-hero__card');
  if (heroCard && !reduced) {
    let ticking = false;
    const parallax = () => {
      ticking = false;
      const y = Math.min(Math.max(window.scrollY, 0), heroCard.offsetHeight);
      heroCard.style.setProperty('--py', y.toFixed(1));
    };
    window.addEventListener('scroll', () => {
      if (!ticking) { ticking = true; requestAnimationFrame(parallax); }
    }, { passive: true });
    parallax();
  }

  /* ---------- mobile menu ---------- */
  const burger = $('.burger');
  const menu = $('#mobile-menu');
  if (burger && menu) {
    const setMenu = (open) => {
      document.body.classList.toggle('menu-open', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      menu.setAttribute('aria-hidden', String(!open));
    };
    burger.addEventListener('click', () => setMenu(!document.body.classList.contains('menu-open')));
    $$('a', menu).forEach((a) => a.addEventListener('click', () => setMenu(false)));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });
    window.matchMedia('(min-width: 960px)').addEventListener('change', (e) => e.matches && setMenu(false));
  }

  /* ---------- reveal on scroll ---------- */
  const revealIO = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add('is-in'); revealIO.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.1 });
  $$('.reveal').forEach((el) => revealIO.observe(el));

  /* ---------- counters ---------- */
  const animateCount = (el) => {
    const to = parseFloat(el.dataset.to);
    const dec = parseInt(el.dataset.decimals || '0', 10);
    if (reduced) { el.textContent = to.toFixed(dec); return; }
    const dur = 1800;
    const start = performance.now();
    const tick = (now) => {
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      el.textContent = (to * eased).toFixed(dec);
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const countIO = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) { animateCount(en.target); countIO.unobserve(en.target); }
    });
  }, { threshold: 0.6 });
  $$('.count').forEach((el) => countIO.observe(el));

  /* ---------- process: "How We Build" stages ---------- */
  const steps = $$('.step');
  const processGrid = $('#process .process');
  if (steps.length && processGrid) {
    const discs = $$('.disc');
    const stageNum = $('.stage__num');
    let current = 0;
    let timer = null;
    let touched = false;
    const setStep = (i) => {
      current = i;
      steps.forEach((s) => {
        const on = Number(s.dataset.step) === i;
        s.classList.toggle('is-active', on);
        $('.step__btn', s)?.setAttribute('aria-pressed', String(on));
      });
      discs.forEach((d) => d.classList.toggle('is-active', Number(d.dataset.disc) === i));
      if (stageNum) stageNum.textContent = String(i + 1).padStart(2, '0');
    };
    const stopAuto = () => { clearInterval(timer); timer = null; };
    const startAuto = () => {
      if (reduced || touched || timer) return;
      timer = setInterval(() => setStep((current + 1) % steps.length), 3200);
    };
    const choose = (s) => { touched = true; stopAuto(); setStep(Number(s.dataset.step)); };
    const canHover = window.matchMedia('(hover: hover)').matches;
    steps.forEach((s) => {
      s.addEventListener('click', () => choose(s));
      if (canHover) s.addEventListener('mouseenter', () => choose(s));
    });
    // cycle through the stages by itself while the section is on screen, until someone picks one
    new IntersectionObserver(([en]) => (en.isIntersecting ? startAuto() : stopAuto()), { threshold: 0.35 })
      .observe(processGrid);
  }

  /* ---------- portfolio slider (home) ---------- */
  const slider = $('.slider');
  if (slider) {
    const cards = $$('.card', slider);
    const dotsWrap = $('.dots');
    const [prevBtn, nextBtn] = $$('.slider-nav .round-btn');
    const cardStep = () => (cards[1] ? cards[1].offsetLeft - cards[0].offsetLeft : slider.clientWidth);
    const currentIndex = () => Math.round(slider.scrollLeft / cardStep());
    const goTo = (i) => {
      const idx = Math.max(0, Math.min(cards.length - 1, i));
      slider.scrollTo({ left: idx * cardStep(), behavior: reduced ? 'auto' : 'smooth' });
    };
    const dots = cards.map((card, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-label', `Show project ${i + 1}: ${$('h3', card).firstChild.textContent.trim()}`);
      b.addEventListener('click', () => goTo(i));
      dotsWrap?.appendChild(b);
      return b;
    });
    const update = () => {
      const i = currentIndex();
      const max = slider.scrollWidth - slider.clientWidth - 2;
      dots.forEach((d, k) => d.setAttribute('aria-selected', String(k === Math.min(i, cards.length - 1))));
      if (prevBtn) prevBtn.disabled = slider.scrollLeft <= 2;
      if (nextBtn) nextBtn.disabled = slider.scrollLeft >= max;
    };
    prevBtn?.addEventListener('click', () => goTo(currentIndex() - 1));
    nextBtn?.addEventListener('click', () => goTo(currentIndex() + 1));
    slider.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
    slider.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo(currentIndex() + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(currentIndex() - 1); }
    });
    window.addEventListener('resize', update);
    update();
  }

  /* ---------- projects page: filter chips ---------- */
  const chips = $$('.chip[data-filter]');
  if (chips.length) {
    const items = $$('.projects-grid .card');
    chips.forEach((chip) => chip.addEventListener('click', () => {
      const f = chip.dataset.filter;
      chips.forEach((c) => c.setAttribute('aria-pressed', String(c === chip)));
      items.forEach((it) => { it.hidden = f !== 'all' && it.dataset.type !== f; });
    }));
  }

  /* ---------- services: "What's included" toggles ---------- */
  $$('.svc__toggle').forEach((btn) => {
    btn.addEventListener('click', () => {
      const card = btn.closest('.svc');
      const open = !card.classList.contains('is-open');
      card.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
  });

  /* ---------- enquiry form (frontend only) ---------- */
  const form = $('.form');
  if (form) {
    const note = $('.form__note', form);
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let ok = true;
      $$('[required]', form).forEach((input) => {
        const valid = input.checkValidity();
        input.closest('.field').classList.toggle('is-invalid', !valid);
        if (!valid) ok = false;
      });
      note.classList.remove('is-ok', 'is-err');
      if (!ok) {
        note.textContent = 'Please complete the highlighted fields.';
        note.classList.add('is-err');
        $('.is-invalid input, .is-invalid select', form)?.focus();
        return;
      }
      const name = form.elements.name.value.trim().split(' ')[0];
      note.textContent = `Thank you, ${name}. We'll be in touch within one business day.`;
      note.classList.add('is-ok');
      form.reset();
    });
    $$('input, select', form).forEach((el) =>
      el.addEventListener('input', () => el.closest('.field').classList.remove('is-invalid'))
    );
  }

  /* ---------- newsletter ---------- */
  const nl = $('.newsletter');
  if (nl) {
    const nlNote = $('.newsletter__note');
    nl.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = $('input', nl);
      if (nlNote) {
        nlNote.textContent = input.checkValidity()
          ? "You're on the list. Expect project news once a month."
          : 'Please enter a valid email address.';
      }
      if (input.checkValidity()) nl.reset();
    });
  }

  /* ---------- footer: fit "SKS DEVELOPMENTS" to the full width ---------- */
  const fw = $('.footer__word');
  const fwText = $('span', fw);
  if (fw && fwText) {
    const fitWord = () => {
      fw.style.fontSize = '100px';
      const ratio = fw.clientWidth / fwText.getBoundingClientRect().width;
      fw.style.fontSize = (100 * ratio * 0.995).toFixed(2) + 'px';
    };
    fitWord();
    if (document.fonts) document.fonts.ready.then(fitWord);
    new ResizeObserver(fitWord).observe(fw);
  }

  /* ---------- links like services.html#design: land on the section ---------- */
  if (location.hash.length > 1) {
    const jump = () => {
      let t = null;
      try { t = document.querySelector(decodeURIComponent(location.hash)); } catch (e) { /* not a valid id */ }
      if (t) t.scrollIntoView({ behavior: 'instant', block: 'start' });
    };
    jump();
    window.addEventListener('load', jump, { once: true });
  }

  /* ---------- year ---------- */
  const year = $('#year');
  if (year) year.textContent = new Date().getFullYear();
})();
