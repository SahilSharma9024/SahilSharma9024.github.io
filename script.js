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

const WELCOME_MS = 2200;   // how long the intro screen stays up

(function () {
    'use strict';

    const root = document.documentElement;

    /* The card lining animates a registered custom property, which needs
       @property support. Where it is missing the ring simply stays still
       rather than breaking, so this is an enhancement flag, not a gate. */
    if (typeof CSS !== 'undefined' && typeof CSS.registerProperty === 'function') {
        root.classList.add('snake-modern');
    }
    const $ = (sel, ctx) => (ctx || document).querySelector(sel);
    const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

    /* Decks register their measure function here. Nothing inside #mainContent
       can be measured while the intro screen is up - it is `hidden`, so every
       offsetHeight is 0 - so the deck has to be re-measured once the page is
       revealed. */
    const deckFits = [];

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

    /* ---------- Smooth scrolling ----------
       Lenis, with the same settings as the company site. Skipped for anyone
       who asked for reduced motion, and on touch devices, where the native
       scroll is already smooth and hijacking it only adds lag. */
    function initSmoothScroll() {
        if (typeof Lenis !== 'function') return null;
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return null;
        if (window.matchMedia('(pointer: coarse)').matches) return null;

        const lenis = new Lenis({
            lerp: 0.055,
            smoothWheel: true,
            wheelMultiplier: 0.8,
            touchMultiplier: 1.5,
            syncTouch: false,
            infinite: false,
        });

        function raf(time) {
            lenis.raf(time);
            requestAnimationFrame(raf);
        }
        requestAnimationFrame(raf);

        /* The page no longer drives scroll itself, so the sticky bar has to be
           told from Lenis rather than from a scroll listener. */
        const bar = $('#topbar');
        if (bar) {
            lenis.on('scroll', ({ scroll }) => {
                bar.classList.toggle('scrolled', scroll > 20);
            });
        }

        /* Anchors have to be routed through Lenis too: a native jump moves the
           real scroll position out from under the animation it is running. */
        document.addEventListener('click', (e) => {
            const a = e.target.closest('a[href^="#"], a[href^="/#"]');
            if (!a) return;
            const hash = a.getAttribute('href').replace(/^\//, '');
            if (hash === '#' || hash.length < 2) return;
            const target = document.querySelector(hash);
            if (!target) return;
            e.preventDefault();
            const bar = document.getElementById('topbar');
            lenis.scrollTo(target, { offset: -((bar ? bar.offsetHeight : 64) + 14) });
            history.replaceState(null, '', hash);
        });

        return lenis;
    }

    const lenis = initSmoothScroll();
    /* Nothing is driving scroll, so hand smoothing back to the browser. */
    if (lenis) root.classList.add('has-lenis');
    else root.classList.add('no-lenis');

    /* ---------- Welcome screen ---------- */
    const welcome = $('#welcomeScreen');
    const main = $('#mainContent');
    const typeEl = $('#welcomeType');
    const subEl = $('#welcomeSub');

    function startMain() {
        if (!main) return;
        main.hidden = false;
        initReveals();
        // Next frame: the deck cannot be measured until this is laid out.
        requestAnimationFrame(() => {
            deckFits.forEach((f) => f());
            jumpToHash();
        });
    }

    /* Arriving at /#connect from a project page: the browser tried to scroll
       there while #mainContent was still hidden, so it had nowhere to go and
       gave up. Do it ourselves once the page is actually on screen. */
    function jumpToHash() {
        const hash = window.location.hash;
        if (!hash || hash.length < 2) return;
        const target = document.querySelector(hash);
        if (!target) return;

        const bar = $('#topbar');
        const offset = -((bar ? bar.offsetHeight : 60) + 14);
        if (lenis) lenis.scrollTo(target, { offset, immediate: true });
        else target.scrollIntoView({ block: 'start' });
    }

    /* The intro plays once per visit, not on every page. Without this, coming
       back to the home page from a project - which is what "Get in touch"
       does - replays the whole thing and drops you at the top instead of at
       the section you asked for. */
    let introSeen = false;
    try {
        introSeen = sessionStorage.getItem('introSeen') === '1';
    } catch (e) {
        /* private mode - just play it */
    }

    // Landing on a specific section is a deliberate destination, so no intro.
    const wantsSection = window.location.hash.length > 1;

    if (welcome && main && !introSeen && !wantsSection) {
        try {
            sessionStorage.setItem('introSeen', '1');
        } catch (e) {
            /* ignore */
        }

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
        if (welcome) welcome.style.display = 'none';
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

    /* ---------- Contact form ---------- */
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

    if (cfReason) {
        cfReason.addEventListener('change', applyTemplate);
        /* Fill in the default choice's subject and message now. This used to
           happen when the dialog opened; with the form on the page there is no
           open event, so the fields sat empty until the dropdown was changed
           and changed back. */
        applyTemplate();
    }

    /* The form sits in the Connect section rather than in a dialog, so an
       email link scrolls to it and puts the cursor in the first field. The
       href stays a real Gmail URL, so middle-click and no-JS still work. */
    function goToForm(reason) {
        const card = $('#message');
        if (!card) return false;
        if (reason && TEMPLATES[reason]) cfReason.value = reason;
        applyTemplate();

        const bar = $('#topbar');
        const offset = -((bar ? bar.offsetHeight : 60) + 16);
        if (lenis) lenis.scrollTo(card, { offset });
        else card.scrollIntoView({ behavior: 'smooth', block: 'start' });

        setTimeout(() => cfName && cfName.focus({ preventScroll: true }), 420);
        return true;
    }

    ['link-email', 'soc-gmail', 'emailText'].forEach((id) => {
        const el = document.getElementById(id);
        if (!el) return;
        el.addEventListener('click', (e) => {
            // Only intercept when the form is on this page; project pages
            // should follow the link to the mail client as before.
            if (goToForm()) e.preventDefault();
        });
    });

    // "or email directly" escape hatch under the send button.
    const direct = $('#cf-direct');
    if (direct) {
        direct.href = gmailCTA;
        direct.target = '_blank';
        direct.rel = 'noopener';
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

    /* ---------- Sticky top bar ----------
       Only wired when Lenis is not driving; otherwise it would fight the
       lenis.on('scroll') handler above. */
    const topbar = $('#topbar');
    if (topbar) {
        const onScroll = () => topbar.classList.toggle('scrolled', window.scrollY > 20);
        if (!lenis) window.addEventListener('scroll', onScroll, { passive: true });
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

        initLiveCards();
    }

    /* ---------- Card lining: only animate what is on screen ----------
       Unlike the reveal above this does not unobserve, because a card
       scrolled back out of view should stop animating again. */
    function initLiveCards() {
        const cards = $$('.card');
        if (!('IntersectionObserver' in window)) {
            cards.forEach((el) => el.classList.add('is-live'));
            return;
        }
        const io = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    entry.target.classList.toggle('is-live', entry.isIntersecting);
                });
            },
            { rootMargin: '150px 0px' }
        );
        cards.forEach((el) => io.observe(el));
    }

    /* ---------- Project deck ----------
       A fan of cards with one in front, advancing on a fixed clock. The cards
       are placed by a ring index rather than by measuring anything, so only
       transform and opacity change and the browser can keep it on the
       compositor. */
    (function initDecks() {
        const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        const LAST_RING = 3;

        $$('[data-deck]').forEach((deck) => {
            const stack = $('[data-deck-stack]', deck) || deck;
            const items = $$('[data-deck-item]', deck);
            const prev = $('[data-deck-prev]', deck);
            const next = $('[data-deck-next]', deck);
            const count = items.length;
            if (!count) return;

            let active = 0;
            let timer = 0;

            const layout = () => {
                items.forEach((el, i) => {
                    // Signed distance around the ring: -n/2 .. +n/2, so the fan
                    // wraps and the loop has no seam.
                    let d = i - active;
                    if (d > count / 2) d -= count;
                    if (d < -count / 2) d += count;

                    const ring = String(Math.min(Math.abs(d), LAST_RING));
                    const side = String(Math.sign(d));

                    /* One parking slot holds the card out of the fan, so a card
                       that just left on one side is next due in from the other.
                       Send it across with transitions off: it is fully
                       transparent at this point, so the jump cannot be seen,
                       and it then travels in from the correct side instead of
                       popping into place mid-fan. */
                    if (el.dataset.ring === String(LAST_RING) && el.dataset.side !== side) {
                        el.style.transition = 'none';
                        el.style.setProperty('--side', side);
                        void el.offsetWidth;
                        el.style.transition = '';
                    }

                    el.dataset.ring = ring;
                    el.dataset.side = side;
                    el.style.setProperty('--side', side);

                    if (ring === String(LAST_RING)) el.setAttribute('aria-hidden', 'true');
                    else el.removeAttribute('aria-hidden');
                });
            };

            const go = (i) => {
                active = ((i % count) + count) % count;
                layout();
            };

            /* ---- height ----
               The cards are absolutely positioned, so the deck cannot get its
               height from them; it has to be told. A figure written in CSS is
               always wrong for somebody: the subtitles and the tag rows wrap
               differently per card and again at each width, so a height that
               fits the tallest leaves a gap under the rest, and one that fits
               the rest clips the tallest.

               So measure. Let every card size to its own content, take the
               largest, and give the deck that. Cards then all share the
               tallest card's height and none of them is cut off. */
            const fit = () => {
                items.forEach((el) => {
                    el.style.height = 'auto';
                });

                let tallest = 0;
                items.forEach((el) => {
                    tallest = Math.max(tallest, el.offsetHeight);
                });

                items.forEach((el) => {
                    el.style.height = '';
                });

                /* On the stack, not the wrapper. `.deck` declares --deck-h in
                   its own rule, so a value inherited from the parent would be
                   shadowed by it; an inline style on the same element wins. */
                // 0 means the deck is not rendered yet - behind the intro screen,
                // or on a hidden tab. Leave the CSS fallback in place and wait to
                // be called again rather than writing a useless height.
                if (tallest) stack.style.setProperty('--deck-h', tallest + 'px');
            };

            /* Re-measure when the width changes, and once more after the web
               fonts land - text measured in the fallback face is the wrong
               height. */
            let resizeTimer = 0;
            window.addEventListener('resize', () => {
                window.clearTimeout(resizeTimer);
                resizeTimer = window.setTimeout(fit, 150);
            });

            if (document.fonts && document.fonts.ready) {
                document.fonts.ready.then(fit);
            }

            deckFits.push(fit);

            const pause = () => {
                window.clearInterval(timer);
                timer = 0;
            };

            const play = () => {
                if (reduced || timer || !deck.hasAttribute('data-deck-auto')) return;
                timer = window.setInterval(() => go(active + 1), 3000);
            };

            // Tabbing to a card behind brings it forward; hovering does not,
            // because a pointer grazing a card on its way past should not flip
            // the deck.
            items.forEach((el, i) => {
                el.addEventListener('focusin', () => {
                    pause();
                    if (i !== active) go(i);
                });
            });

            let onScreen = true;

            const resume = () => {
                if (onScreen && !document.hidden) play();
                else pause();
            };

            if ('IntersectionObserver' in window) {
                new IntersectionObserver(
                    (entries) => {
                        onScreen = entries[0].isIntersecting;
                        resume();
                    },
                    { threshold: 0.3 }
                ).observe(deck);
            }

            deck.addEventListener('focusout', resume);
            document.addEventListener('visibilitychange', resume);

            /* An arrow restarts the clock rather than stopping it, so the deck
               never ends up parked because someone clicked once. */
            const nudge = (to) => {
                pause();
                go(to);
                resume();
            };

            if (prev) prev.addEventListener('click', () => nudge(active - 1));
            if (next) next.addEventListener('click', () => nudge(active + 1));

            /* Swipe. Bound to the stack rather than the wrapper so a drag that
               starts on an arrow is not read as a gesture, and cancel is
               handled because a touch the browser reclaims never sends
               pointerup. */
            let downX = null;

            stack.addEventListener('pointerdown', (e) => {
                downX = e.clientX;
                pause();
            }, { passive: true });

            stack.addEventListener('pointerup', (e) => {
                if (downX === null) return;
                const dx = e.clientX - downX;
                downX = null;
                if (Math.abs(dx) > 40) nudge(active + (dx < 0 ? 1 : -1));
                else resume();
            }, { passive: true });

            stack.addEventListener('pointercancel', () => {
                downX = null;
                resume();
            }, { passive: true });

            layout();
            fit();
            resume();
        });
    })();

    /* ---------- Private repo pills ---------- */
    /* Hover and focus are handled in CSS; this is the tap path, where there is
       no hover to rely on. Clicking again, or anywhere else, puts it back. */
    $$('.plink.is-private').forEach((pill) => {
        pill.addEventListener('click', (e) => {
            e.preventDefault();
            const on = pill.classList.toggle('show-private');
            if (!on) return;
            const clear = (ev) => {
                if (pill.contains(ev.target)) return;
                pill.classList.remove('show-private');
                document.removeEventListener('click', clear, true);
            };
            document.addEventListener('click', clear, true);
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
        const HOT = 'a, button, .chip, .project-card, input, textarea, select, [role="button"]';
        document.addEventListener('mouseover', (e) => {
            if (e.target.closest && e.target.closest(HOT)) dot.classList.add('hot');
        });
        document.addEventListener('mouseout', (e) => {
            if (e.target.closest && e.target.closest(HOT)) dot.classList.remove('hot');
        });

        /* Idles once the glow has caught up with the pointer. It used to write
           two transforms on every single frame for the whole life of the page,
           which is main-thread work landing in the middle of every scroll -
           for a decoration that was not moving. */
        let running = false;

        function frame() {
            gx += (tx - gx) * GLOW_EASE;
            gy += (ty - gy) * GLOW_EASE;
            dx += (tx - dx) * DOT_EASE;
            dy += (ty - dy) * DOT_EASE;

            glow.style.transform = 'translate3d(' + gx + 'px,' + gy + 'px,0)';
            dot.style.transform = 'translate3d(' + dx + 'px,' + dy + 'px,0)';

            // Sub-pixel: nothing more to show, so stop until the pointer moves.
            if (Math.abs(tx - gx) < 0.1 && Math.abs(ty - gy) < 0.1 &&
                Math.abs(tx - dx) < 0.1 && Math.abs(ty - dy) < 0.1) {
                running = false;
                return;
            }
            requestAnimationFrame(frame);
        }

        function kick() {
            if (running) return;
            running = true;
            requestAnimationFrame(frame);
        }

        window.addEventListener('mousemove', kick, { passive: true });
        window.addEventListener('touchmove', kick, { passive: true });
        window.addEventListener('touchstart', kick, { passive: true });
        kick();
    })();

    /* ---------- Footer year ---------- */
    const year = $('#year');
    if (year) year.textContent = new Date().getFullYear();
})();
