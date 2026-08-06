/* ==========================================================================
   Sahil Sharma — Portfolio
   ========================================================================== */

// Leave blank to hide the component
const links = {
    linkedin: 'https://www.linkedin.com/in/sahil-sharma-155697349',
    github: 'https://github.com/SahilSharma9024',
    twitter: 'https://x.com/SahilSharma9024',
    email: 'sahilsharmaas2006@gmail.com',
    whatsapp: 'https://wa.me/919024442872',
};

/* --------------------------------------------------------------------------
   MAIL — Web3Forms
   -------------------------------------------------------------------------- */
const MAIL = {
    ACCESS_KEY: 'e11ee396-4e20-4cb5-82d0-2c6124c6c891',                                  // <-- paste Web3Forms key here
    ENDPOINT: 'https://api.web3forms.com/submit',
};

const WELCOME_MS = 3600;   // how long the intro screen stays up

(function () {
    'use strict';

    const root = document.documentElement;
    const $ = (sel, ctx) => (ctx || document).querySelector(sel);
    const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

    /* ---------- Theme ---------- */
    const themeToggle = $('#themeToggle');

    function setTheme(theme) {
        root.setAttribute('data-theme', theme);
        try {
            localStorage.setItem('theme', theme);
        } catch (e) {
            /* private mode — theme just won't persist */
        }
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            setTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
        });
    }

    // Follow the OS only while the visitor hasn't chosen for themselves.
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    mq.addEventListener('change', (e) => {
        let saved = null;
        try {
            saved = localStorage.getItem('theme');
        } catch (err) { /* ignore */ }
        if (!saved) root.setAttribute('data-theme', e.matches ? 'dark' : 'light');
    });

    /* ---------- Toast ---------- */
    const toastEl = $('#toast');
    let toastTimer;

    function toast(message) {
        if (!toastEl) return;
        toastEl.textContent = message;
        toastEl.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => toastEl.classList.remove('show'), 2200);
    }

    /* ---------- Welcome screen ---------- */
    const welcome = $('#welcomeScreen');
    const main = $('#mainContent');
    const typeEl = $('#welcomeType');
    const subEl = $('#welcomeSub');

    function startMain() {
        if (!main) return;
        main.hidden = false;
        initReveals();
    }

    if (welcome && main) {
        welcome.style.setProperty('--welcome-ms', WELCOME_MS + 'ms');

        const text = "Hi, I'm Sahil Sharma.";
        const speed = 70;
        let i = 0;

        (function type() {
            if (i <= text.length) {
                typeEl.textContent = text.slice(0, i);
                i += 1;
                setTimeout(type, speed);
            } else if (subEl) {
                subEl.classList.add('show');
            }
        })();

        // Let visitors skip the intro.
        const skip = () => finish();
        let finished = false;

        function finish() {
            if (finished) return;
            finished = true;
            welcome.classList.add('fade-out');
            setTimeout(() => {
                welcome.style.display = 'none';
                startMain();
            }, 600);
        }

        welcome.addEventListener('click', skip);
        document.addEventListener('keydown', function onKey(e) {
            if (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ') {
                document.removeEventListener('keydown', onKey);
                skip();
            }
        });

        setTimeout(finish, WELCOME_MS);
    } else {
        startMain();
    }

    /* ---------- Name typewriter (loops) ---------- */
    const nameEl = $('#typewriterName');
    if (nameEl) {
        const fullName = nameEl.dataset.fullname || nameEl.textContent.trim();
        const speed = 120;
        const pause = 5000;

        (function cycle() {
            let i = 0;
            (function type() {
                if (i <= fullName.length) {
                    nameEl.textContent = fullName.slice(0, i);
                    i += 1;
                    setTimeout(type, speed);
                } else {
                    setTimeout(cycle, pause);
                }
            })();
        })();
    }

    /* ---------- Wire up links ---------- */
    function gmailComposeUrl(email, subject, body) {
        return (
            'https://mail.google.com/mail/?view=cm&fs=1&to=' + encodeURIComponent(email) +
            (subject ? '&su=' + encodeURIComponent(subject) : '') +
            (body ? '&body=' + encodeURIComponent(body) : '')
        );
    }

    const gmailCTA = gmailComposeUrl(
        links.email,
        'Hello Sahil',
        'Hi Sahil,\n\nI would love to connect with you regarding your work.'
    );

    // id -> url. An empty url hides the element instead of leaving it dead.
    const linkMap = {
        'link-linkedin': links.linkedin,
        'link-github': links.github,
        'link-twitter': links.twitter,
        'link-whatsapp': links.whatsapp,
        'link-email': gmailCTA,
        'soc-linkedin': links.linkedin,
        'soc-github': links.github,
        'soc-twitter': links.twitter,
        'soc-whatsapp': links.whatsapp,
        'soc-gmail': gmailCTA,
    };

    Object.entries(linkMap).forEach(([id, url]) => {
        const el = document.getElementById(id);
        if (!el) return;
        if (!url) {
            el.style.display = 'none';
            return;
        }
        el.href = url;
    });

    const emailText = $('#emailText');
    if (emailText) {
        emailText.href = gmailCTA;
        emailText.target = '_blank';
        emailText.rel = 'noopener';
        emailText.textContent = links.email;
    }

    /* ---------- Contact modal ---------- */
    const modal = $('#contactModal');
    const contactForm = $('#contactForm');
    const cfNote = $('#cf-note');
    const cfName = $('#cf-name');
    const cfEmail = $('#cf-email');
    const cfReason = $('#cf-reason');
    const cfSubject = $('#cf-subject');
    const cfMessage = $('#cf-message');

    // Pre-filled copy per reason. The visitor can send as-is or edit first.
    const TEMPLATES = {
        internship: {
            subject: 'Internship opportunity for you',
            body: 'Hi Sahil,\nI came across your portfolio and I think you could be a good fit for an opportunity on our team.\n\nA little about the role:- \nWould you be open to a short chat this week?\nBest regards,',
        },
        collab: {
            subject: "Let's build something together",
            body: 'Hi Sahil,\nI saw your work and would love to collaborate on something.\n\nWhat I have in mind:\n- \nLet me know if that sounds interesting.\nBest regards,',
        },
        project: {
            subject: 'Question about one of your projects',
            body: 'Hi Sahil,\nI was looking through your projects and had a question about \n\nSpecifically:\n- \nBest regards,',
        },
        freelance: {
            subject: 'Freelance work — are you available?',
            body: 'Hi Sahil,\nI have a piece of work I think you would be well suited to.\n\nScope and timeline:\n- \nAre you taking on projects at the moment?\nBest regards,',
        },
        hello: {
            subject: 'Hello Sahil!',
            body: 'Hi Sahil,\nI came across your portfolio and wanted to reach out and say hello.\n\nBest regards,',
        },
    };

    // Only overwrite the fields the visitor has not personalised.
    let subjectTouched = false;
    let messageTouched = false;

    if (cfSubject) cfSubject.addEventListener('input', () => { subjectTouched = true; });
    if (cfMessage) cfMessage.addEventListener('input', () => { messageTouched = true; });

    function applyTemplate() {
        const t = TEMPLATES[cfReason.value] || TEMPLATES.hello;
        if (!subjectTouched) cfSubject.value = t.subject;
        if (!messageTouched) cfMessage.value = t.body;
    }

    if (cfReason) cfReason.addEventListener('change', applyTemplate);

    let lastFocused = null;

    function openModal(reason) {
        if (!modal) return;
        lastFocused = document.activeElement;
        if (reason && TEMPLATES[reason]) cfReason.value = reason;
        applyTemplate();
        modal.classList.add('open');
        document.body.style.overflow = 'hidden';
        setTimeout(() => cfName && cfName.focus(), 60);
    }

    function closeModal() {
        if (!modal) return;
        modal.classList.remove('open');
        document.body.style.overflow = '';
        if (lastFocused) lastFocused.focus();
    }

    if (modal) {
        $$('[data-close-modal]', modal).forEach((el) =>
            el.addEventListener('click', closeModal)
        );
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
        });

        // Every email entry point opens the form instead of a mail draft.
        // The href stays as the Gmail URL so middle-click and no-JS still work.
        ['link-email', 'soc-gmail', 'emailText'].forEach((id) => {
            const el = document.getElementById(id);
            if (!el) return;
            el.addEventListener('click', (e) => {
                e.preventDefault();
                openModal();
            });
        });

        // "or email directly" escape hatch inside the modal.
        const direct = $('#cf-direct');
        if (direct) {
            direct.href = gmailCTA;
            direct.target = '_blank';
            direct.rel = 'noopener';
        }
    }

    function setNote(message, ok) {
        if (!cfNote) return;
        cfNote.textContent = message;
        cfNote.className = 'form-note show ' + (ok ? 'ok' : 'bad');
    }

    function setSending(busy) {
        const btn = contactForm.querySelector('button[type="submit"]');
        const label = btn.querySelector('[data-label]');
        btn.disabled = busy;
        if (!label) return;
        if (busy) {
            label.dataset.original = label.textContent;
            label.textContent = 'Sending…';
        } else if (label.dataset.original) {
            label.textContent = label.dataset.original;
        }
    }

    function gmailFallback(subject, body, from) {
        const composed = body + '\n\n— ' + from.name + ' (' + from.email + ')';
        window.open(
            gmailComposeUrl(links.email, subject, composed),
            '_blank',
            'noopener'
        );
    }

    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            if (!contactForm.checkValidity()) {
                contactForm.reportValidity();
                return;
            }

            const from = { name: cfName.value.trim(), email: cfEmail.value.trim() };
            const subject = cfSubject.value.trim();
            const body = cfMessage.value.trim();

            // No key configured yet → keep the draft-a-mail flow.
            if (!MAIL.ACCESS_KEY) {
                gmailFallback(subject, body, from);
                setNote('Your message is ready in a new tab — press send there and it reaches me.', true);
                return;
            }

            setSending(true);
            try {
                const res = await fetch(MAIL.ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
                    body: JSON.stringify({
                        access_key: MAIL.ACCESS_KEY,
                        subject: subject,
                        from_name: 'Portfolio — ' + from.name,
                        replyto: from.email,
                        name: from.name,
                        email: from.email,
                        reason: cfReason.options[cfReason.selectedIndex].text,
                        message: body,
                    }),
                });
                const data = await res.json();
                if (!res.ok || !data.success) throw new Error('rejected');

                setNote('Sent — thanks for reaching out. I will get back to you soon.', true);
                contactForm.reset();
                subjectTouched = messageTouched = false;
                applyTemplate();
                setTimeout(closeModal, 2200);
            } catch (err) {
                // Never lose a message: fall back to the mail draft.
                gmailFallback(subject, body, from);
                setNote('Could not send automatically, so I have opened a pre-filled email instead — please press send there.', false);
            } finally {
                setSending(false);
            }
        });
    }

    /* ---------- Copy email ---------- */
    const copyBtn = $('#copyEmailBtn');
    if (copyBtn) {
        copyBtn.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(links.email);
                toast('Email copied — ' + links.email);
            } catch (e) {
                // Clipboard API needs a secure context; fall back to selection.
                const ta = document.createElement('textarea');
                ta.value = links.email;
                ta.style.position = 'fixed';
                ta.style.opacity = '0';
                document.body.appendChild(ta);
                ta.select();
                try {
                    document.execCommand('copy');
                    toast('Email copied — ' + links.email);
                } catch (err) {
                    toast('Copy failed — ' + links.email);
                }
                document.body.removeChild(ta);
            }
        });
    }

    /* ---------- Sticky top bar ---------- */
    const topbar = $('#topbar');
    if (topbar) {
        const onScroll = () => topbar.classList.toggle('scrolled', window.scrollY > 20);
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    /* ---------- Mobile menu (navbar burger) ---------- */
    const burger = $('#navBurger');
    const mobileMenu = $('#mobileMenu');
    const navScrim = $('#navScrim');

    function setMobileMenu(open) {
        if (!burger || !mobileMenu) return;
        mobileMenu.classList.toggle('open', open);
        burger.classList.toggle('open', open);
        if (navScrim) navScrim.classList.toggle('open', open);
        // Freezes the page behind the drawer instead of letting it scroll
        // under the blur.
        root.classList.toggle('nav-open', open);
        burger.setAttribute('aria-expanded', String(open));
        burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }

    if (burger && mobileMenu) {
        burger.addEventListener('click', (e) => {
            e.stopPropagation();
            setMobileMenu(!mobileMenu.classList.contains('open'));
        });

        // Close after picking a destination.
        $$('a', mobileMenu).forEach((a) => a.addEventListener('click', () => setMobileMenu(false)));

        document.addEventListener('click', (e) => {
            if (mobileMenu.contains(e.target) || burger.contains(e.target)) return;
            setMobileMenu(false);
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') setMobileMenu(false);
        });

        // Leaving mobile width with the menu open would strand it open.
        window.addEventListener('resize', () => {
            if (window.innerWidth > 900) setMobileMenu(false);
        });
    }

    /* ---------- Reveal on scroll ---------- */
    function initReveals() {
        const items = $$('.reveal');
        if (!('IntersectionObserver' in window)) {
            items.forEach((el) => el.classList.add('in'));
            return;
        }
        const io = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) return;
                    entry.target.classList.add('in');
                    io.unobserve(entry.target);
                });
            },
            { rootMargin: '0px 0px -10% 0px', threshold: 0.06 }
        );
        items.forEach((el) => io.observe(el));
    }

    /* ---------- Project panels ---------- */
    $$('.project').forEach((project) => {
        const head = $('.project-head', project);
        const body = $('.project-body', project);
        if (!head || !body) return;

        function open() {
            // Independent panels: any number of projects can stay expanded.
            project.classList.add('open');
            head.setAttribute('aria-expanded', 'true');
            body.style.maxHeight = body.scrollHeight + 'px';
        }

        function collapse(el) {
            const b = $('.project-body', el);
            const h = $('.project-head', el);
            el.classList.remove('open');
            if (h) h.setAttribute('aria-expanded', 'false');
            if (b) b.style.maxHeight = '0px';
        }

        head.addEventListener('click', () => {
            if (project.classList.contains('open')) collapse(project);
            else open();
        });

        // Keep the height correct when the viewport reflows the content.
        window.addEventListener('resize', () => {
            if (project.classList.contains('open')) {
                body.style.maxHeight = body.scrollHeight + 'px';
            }
        });
    });

    /* ---------- Quick jump panel ---------- */
    const panelToggle = $('#panelToggle');
    const sidePanel = $('#sidePanel');

    function setPanel(open) {
        if (!panelToggle || !sidePanel) return;
        sidePanel.classList.toggle('open', open);
        panelToggle.classList.toggle('open', open);
        panelToggle.setAttribute('aria-expanded', String(open));
        sidePanel.setAttribute('aria-hidden', String(!open));
    }

    if (panelToggle) {
        panelToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            setPanel(!sidePanel.classList.contains('open'));
        });
    }

    document.addEventListener('click', (e) => {
        if (!sidePanel || !panelToggle) return;
        if (sidePanel.contains(e.target) || panelToggle.contains(e.target)) return;
        setPanel(false);
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') setPanel(false);
    });

    $$('[data-scroll-target]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const target = document.getElementById(btn.dataset.scrollTarget);
            if (!target) return;
            setPanel(false);
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            target.classList.remove('focus-pulse');
            void target.offsetWidth;          // force reflow so the animation restarts
            target.classList.add('focus-pulse');
            setTimeout(() => target.classList.remove('focus-pulse'), 1000);
        });
    });

    /* ---------- Soft cursor follower ---------- */
    (function cursorFollower() {
        // Runs on touch too: there it tracks taps and drags rather than hover.
        const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (still) return;

        const glow = document.createElement('div');
        glow.className = 'cursor-glow';
        const dot = document.createElement('div');
        dot.className = 'cursor-dot';
        document.body.append(glow, dot);

        // Target (true pointer) vs rendered positions.
        let tx = window.innerWidth / 2;
        let ty = window.innerHeight / 2;
        let gx = tx, gy = ty;   // glow — heavy, trails well behind
        let dx = tx, dy = ty;   // dot  — light, stays close
        let awake = false;

        // Lerp factors: lower = lazier. Runs every frame, so motion is
        // continuous rather than jumping between mousemove events.
        const GLOW_EASE = 0.055;
        const DOT_EASE = 0.2;

        function show() {
            if (awake) return;
            awake = true;
            glow.classList.add('visible');
            dot.classList.add('visible');
        }

        function hide() {
            awake = false;
            glow.classList.remove('visible');
            dot.classList.remove('visible');
        }

        window.addEventListener('mousemove', (e) => {
            tx = e.clientX;
            ty = e.clientY;
            show();
        }, { passive: true });

        // Fade out gently when the pointer leaves, back in when it returns.
        document.addEventListener('mouseleave', hide);
        document.addEventListener('mouseenter', show);

        /* Touch: the glow appears under the finger and trails it while dragging,
           then fades out a beat after release so it does not sit there stranded. */
        let touchFade;

        function fromTouch(e) {
            const t = e.touches && e.touches[0];
            if (!t) return;
            clearTimeout(touchFade);
            tx = t.clientX;
            ty = t.clientY;
            show();
        }

        window.addEventListener('touchstart', (e) => {
            // Land the glow on the finger rather than sliding in from wherever
            // it was left, which would look like a stray object flying across.
            const t = e.touches && e.touches[0];
            if (!t) return;
            if (!awake) {
                gx = dx = t.clientX;
                gy = dy = t.clientY;
            }
            fromTouch(e);
        }, { passive: true });

        window.addEventListener('touchmove', fromTouch, { passive: true });

        window.addEventListener('touchend', () => {
            clearTimeout(touchFade);
            touchFade = setTimeout(hide, 1200);
        }, { passive: true });

        // Swell the dot over anything clickable.
        const HOT = 'a, button, .chip, .project-head, input, textarea, select, [role="button"]';
        document.addEventListener('mouseover', (e) => {
            if (e.target.closest && e.target.closest(HOT)) dot.classList.add('hot');
        });
        document.addEventListener('mouseout', (e) => {
            if (e.target.closest && e.target.closest(HOT)) dot.classList.remove('hot');
        });

        (function frame() {
            gx += (tx - gx) * GLOW_EASE;
            gy += (ty - gy) * GLOW_EASE;
            dx += (tx - dx) * DOT_EASE;
            dy += (ty - dy) * DOT_EASE;

            glow.style.transform = 'translate3d(' + gx + 'px,' + gy + 'px,0)';
            dot.style.transform = 'translate3d(' + dx + 'px,' + dy + 'px,0)';

            requestAnimationFrame(frame);
        })();
    })();

    /* ---------- Footer year ---------- */
    const year = $('#year');
    if (year) year.textContent = new Date().getFullYear();
})();
