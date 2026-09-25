#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site build for the portfolio.

Stitches the partials in src/partials and the project data in src/data into
finished HTML under dist/. Standard library only - no npm, no node_modules, no
framework. Run it with:

    python build.py

and serve dist/ with anything. GitHub Pages publishes the same folder via
.github/workflows/pages.yml.

Why a build at all: the nav, footer, theme bootstrap, contact modal and quick
jump panel are identical on every page. Without this they would be copy-pasted
into nine files and a nav change would mean editing all nine.
"""
import hashlib
import io
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'src'))

from data.projects import PROJECTS, ICON          # noqa: E402
import covers                                     # noqa: E402

SRC = os.path.join(HERE, 'src')
OUT = os.path.join(HERE, 'dist')
SITE = 'https://sahilsharma9024.github.io'
LF = chr(10)

BY_ID = {p['id']: p for p in PROJECTS}


def digest(name):
    """Short content hash, so a changed asset gets a URL the cache has not seen."""
    with io.open(os.path.join(HERE, name), 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:8]


ASSET_V = {}


# --------------------------------------------------------------------- io ---

def read(rel):
    with io.open(os.path.join(SRC, rel), encoding='utf-8') as f:
        return f.read().replace(chr(13) + LF, LF)


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, 'w', encoding='utf-8', newline=LF) as f:
        f.write(text)
    return len(text.encode('utf-8'))


# ---------------------------------------------------------------- chrome ---

PARTIALS = {name: read('partials/%s.html' % name) for name in (
    'welcome', 'topbar', 'footer', 'modal',
    'section-hero', 'section-about', 'section-experience',
    'section-skills', 'section-education', 'section-connect',
)}

# Everything except Projects is a section of the home page. `anchor` is the
# in-page form used on home itself; `href` is the form used from anywhere else.
NAV = [
    ('#about', '/#about', 'About'),
    ('#experience', '/#experience', 'Experience'),
    ('#skills', '/#skills', 'Skills'),
    ('#education', '/#education', 'Education'),
    ('/projects/', '/projects/', 'Projects'),
    ('#connect', '/#connect', 'Connect'),
]


def nav_links(here, indent='                    '):
    out = []
    for anchor, href, label in NAV:
        target = anchor if here == '/' else href
        active = ' class="is-here"' if href == '/projects/' and here == '/projects/' else ''
        out.append('<a href="%s"%s>%s</a>' % (target, active, label))
    return LF.join(indent + a for a in out)


def topbar(here):
    """Single-page anchors become page links; the rest of the bar is untouched."""
    t = PARTIALS['topbar']

    # Desktop nav
    t = re.sub(r'<nav class="topnav">.*?</nav>',
               '<nav class="topnav">' + LF + nav_links(here) + LF + '                </nav>',
               t, count=1, flags=re.S)

    # Mobile nav shares the same list
    t = re.sub(r'(<nav class="mobile-nav"[^>]*>).*?(</nav>)',
               lambda m: m.group(1) + LF + nav_links(here) + LF + '                ' + m.group(2),
               t, count=1, flags=re.S)

    t = t.replace('<a href="#top" class="mono-mark">', '<a href="/" class="mono-mark">')
    t = t.replace('href="resume.pdf"', 'href="/resume.pdf"')
    return t



HEAD = '''<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <meta name="description" content="{desc}" />
    <meta name="author" content="Sahil Sharma" />
    <link rel="canonical" href="{canon}" />
    <meta name="theme-color" content="#4f46e5" media="(prefers-color-scheme: light)" />
    <meta name="theme-color" content="#070911" media="(prefers-color-scheme: dark)" />

    <meta property="og:type" content="{ogtype}" />
    <meta property="og:site_name" content="Sahil Sharma" />
    <meta property="og:title" content="{ogtitle}" />
    <meta property="og:description" content="{desc}" />
    <meta property="og:url" content="{canon}" />
    <meta property="og:image" content="{SITE}/assets/og-cover.jpg" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:image:alt" content="Sahil Sharma — Software Engineer" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{ogtitle}" />
    <meta name="twitter:description" content="{desc}" />
    <meta name="twitter:image" content="{SITE}/assets/og-cover.jpg" />

    <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png" />
    <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />

    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
        href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap"
        rel="stylesheet" />
    <link rel="stylesheet" href="/styles.css?v={cssv}" />

    <!-- Set the theme before first paint so there is no flash of the wrong theme. -->
    <script>
        (function () {{
            try {{
                var saved = localStorage.getItem('theme');
                var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
                document.documentElement.setAttribute('data-theme', saved || (prefersDark ? 'dark' : 'light'));
            }} catch (e) {{
                document.documentElement.setAttribute('data-theme', 'light');
            }}
        }})();
    </script>

    <script type="application/ld+json">
{jsonld}
    </script>
</head>

<body>
'''

FOOT = '''
    </div><!-- /main -->

    {modal}

    <!-- Lenis: smooth scrolling. Loaded before script.js, which initialises it. -->
    <script src="https://cdn.jsdelivr.net/npm/lenis@1.3.26/dist/lenis.min.js"></script>
    <script src="/script.js?v={jsv}"></script>
</body>

</html>
'''

PERSON_LD = '''    {
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "Sahil Sharma",
      "url": "%s/",
      "image": "%s/assets/og-cover.jpg",
      "jobTitle": "Software Engineer",
      "description": "B.Tech CSE (AI & ML) student building AI automation pipelines, LLM integrations and backend systems.",
      "email": "mailto:sahilsharma9024@gmail.com",
      "alumniOf": {
        "@type": "CollegeOrUniversity",
        "name": "Guru Gobind Singh Indraprastha University",
        "address": { "@type": "PostalAddress", "addressLocality": "New Delhi", "addressCountry": "IN" }
      },
      "knowsAbout": ["Artificial Intelligence", "Machine Learning", "Python", "C#", "ASP.NET Core", "Backend Development", "Automation", "Large Language Models"],
      "sameAs": ["https://github.com/SahilSharma9024"]
    }''' % (SITE, SITE)


def project_ld(p):
    return '''    {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "%s",
      "applicationCategory": "%s",
      "description": "%s",
      "url": "%s/projects/%s/",
      "author": { "@type": "Person", "name": "Sahil Sharma", "url": "%s/" }
    }''' % (p['brand'], p['category'],
            re.sub(r'\s+', ' ', p['summary']).replace('"', "'"),
            SITE, p['id'], SITE)


def page(slug, title, desc, body, here, jsonld=PERSON_LD, ogtype='website',
         ogtitle=None, welcome=False):
    canon = SITE + '/' + (slug + '/' if slug else '')
    head = HEAD.format(title=title, desc=desc, canon=canon, SITE=SITE,
                       ogtype=ogtype, ogtitle=ogtitle or title, jsonld=jsonld,
                       cssv=ASSET_V['css'])
    html = head
    if welcome:
        html += LF + '    ' + PARTIALS['welcome'].strip() + LF
        html += LF + '    <div id="mainContent" class="main-content" hidden>' + LF
    else:
        # Only the landing page gates behind the intro; deep links open directly.
        html += LF + '    <div id="mainContent" class="main-content">' + LF
    html += LF + topbar(here) + LF
    html += body + LF
    html += PARTIALS['footer'] + LF
    html += FOOT.format(modal=PARTIALS['modal'].strip(), jsv=ASSET_V['js'])

    rel = (slug + '/index.html') if slug else 'index.html'
    n = write(rel, html)
    print('  %-38s %6.1f KB' % (rel, n / 1024.0))
    return canon


# -------------------------------------------------------------- fragments ---

def icon_svg(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round">%s</svg>' % ICON[name])


def badges(p):
    cat = ('<span class="pbadge pbadge-cat">%s</span>' % p['category'])
    if p['status'] == 'featured':
        st = ('<span class="pbadge pbadge-featured">'
              '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2L3 14h8l-1 8 10-12h-8z"/></svg>'
              'Flagship</span>')
    else:
        st = '<span class="pbadge pbadge-live">%s</span>' % p['status_label']
    return cat, st


def card(p, link=True):
    """The project card. Same anatomy as the company site: cover with badges,
    icon and title, summary, three tag pills, then a footer with the stack and
    a Details arrow."""
    cat, st = badges(p)
    tags = ''.join('<li class="pill">%s</li>' % t for t in p['tags'][:3])
    href = '/projects/%s/' % p['id']

    title = ('<a href="%s">%s</a>' % (href, p['brand'])) if link else p['brand']

    return '''                    <article class="card project-card">
                        <div class="pcover-wrap">
                            {cover}
                            <span class="pcover-sheen" aria-hidden="true"></span>
                            <div class="pcover-badges">{cat}{st}</div>
                        </div>

                        <div class="project-card-body">
                            <div class="project-card-head">
                                <span class="pad {pad}" aria-hidden="true">{icon}</span>
                                <span class="project-name">
                                    <span class="brand">{title}</span>
                                    <span class="subtitle">{subtitle}</span>
                                </span>
                            </div>

                            <p class="project-card-sum">{summary}</p>

                            <ul class="chips project-card-tags">{tags}</ul>

                            <div class="project-card-foot">
                                <span class="project-card-meta">
                                    <strong>{meta}</strong>
                                    <em>{meta_note}</em>
                                </span>
                                <span class="project-open">
                                    Details
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                         stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                                        <path d="M5 12h14M13 6l6 6-6 6" />
                                    </svg>
                                </span>
                            </div>
                        </div>
                        {hit}
                    </article>'''.format(
        cover=covers.cover(p['id']), cat=cat, st=st, pad=p['pad'],
        icon=ICON_MARKUP[p['id']], title=title, subtitle=p['subtitle'],
        summary=p['summary'], tags=tags, meta=p['meta'], meta_note=p['meta_note'],
        hit=('<a class="project-card-hit" href="%s" aria-label="%s — details" tabindex="-1"></a>' % (href, p['brand'])) if link else '')


def link_html(kind, label, href, note):
    if kind == 'private':
        # The label swaps to "Private" on hover, focus or tap. Both strings are
        # stacked in the same grid cell so the pill does not change width as
        # they cross-fade.
        return ('<button class="plink is-private" type="button" '
                'aria-label="%s \u2014 private repository">'
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
                'stroke-linecap="round" stroke-linejoin="round">'
                '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>'
                '<span class="plink-swap">'
                '<span class="plink-label">%s</span>'
                '<span class="plink-private" aria-hidden="true">%s</span>'
                '</span></button>' % (label, label, note or 'Private'))
    ico = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
           'stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>'
           if kind == 'demo' else
           '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 00-3.16 19.49c.5.09.68-.22.68-.48'
           'l-.01-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 '
           '1.53 1.03.89 1.53 2.34 1.09 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.56-1.11-4.56-4.94 0-1.09.39-1.98 '
           '1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02a9.5 9.5 0 015 0c1.91-1.29 2.75-1.02 2.75-1.02.55 '
           '1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.69-4.57 4.94.36.31.68.92.68 1.85l-.01 2.75c0 '
           '.27.18.58.69.48A10 10 0 0012 2z"/></svg>')
    return ('<a class="plink" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>'
            % (href, ico, label))


ICON_MARKUP = {}   # filled in main(), from the icons baked into the partials


# ------------------------------------------------------------------ pages ---

def home():
    deck_items = ''.join(
        '                        <div class="deck-item" data-deck-item>' + LF
        + card(p) + LF + '                        </div>' + LF
        for p in PROJECTS)

    body = (PARTIALS['section-hero'] + LF
            + PARTIALS['section-about'] + LF
            + PARTIALS['section-experience'] + LF
            + PARTIALS['section-skills'] + LF
            + PARTIALS['section-education'] + LF) + '''
        <!-- ---------- Projects (deck) ---------- -->
        <section class="section" id="projects">
            <div class="bloom" style="width:28rem;height:28rem;top:10%;left:-9rem;background:rgba(236,72,153,.13)">
            </div>
            <div class="wrap">
                <div class="section-head reveal">
                    <span class="eyebrow">Projects</span>
                    <h2 class="display">Things I&rsquo;ve built.</h2>
                    <p>Six builds, from a shipped internal platform to weekend automation.</p>
                </div>

                <div class="reveal deck-wrap" data-deck data-deck-auto>
                    <div class="deck" data-deck-stack>
''' + deck_items + '''                    </div>

                    <nav class="deck-nav" aria-label="Projects">
                        <button type="button" class="deck-arrow" data-deck-prev aria-label="Previous project">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                 stroke-linecap="round" stroke-linejoin="round">
                                <path d="M19 12H5M11 18l-6-6 6-6" />
                            </svg>
                        </button>
                        <button type="button" class="deck-arrow" data-deck-next aria-label="Next project">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                 stroke-linecap="round" stroke-linejoin="round">
                                <path d="M5 12h14M13 6l6 6-6 6" />
                            </svg>
                        </button>
                    </nav>
                </div>

                <p class="deck-more">
                    <a class="btn" href="/projects/">Open the full project list
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                             stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M5 12h14M13 6l6 6-6 6" />
                        </svg>
                    </a>
                </p>
            </div>
        </section>
''' + LF + PARTIALS['section-connect'] + LF
    return page('', 'Sahil Sharma — Software Engineer | AI Automation & Backend',
                'Sahil Sharma — B.Tech CSE (AI &amp; ML) at GGSIPU, New Delhi. I build AI '
                'automation pipelines, LLM integrations and backend systems.',
                body, '/', ogtype='profile',
                ogtitle='Sahil Sharma — Software Engineer', welcome=True)


def projects_index():
    grid = LF.join(card(p) for p in PROJECTS)
    body = '''
        <section class="section" id="projects">
            <div class="bloom" style="width:28rem;height:28rem;top:6%;left:-9rem;background:rgba(236,72,153,.13)">
            </div>
            <div class="wrap">
                <div class="section-head reveal">
                    <span class="eyebrow">Projects</span>
                    <h2 class="display">Things I&rsquo;ve built.</h2>
                    <p>Six builds, from a shipped internal platform to weekend automation.
                        Open any card for the full breakdown.</p>
                </div>

                <div class="project-grid">
''' + grid + '''
                </div>
            </div>
        </section>
'''
    return page('projects', 'Projects — Sahil Sharma',
                'Six projects by Sahil Sharma: a team operations platform, automatic meeting '
                'minutes, AI news automation, a serverless music assistant, a mood-based '
                'recommender and a result management system.',
                body, '/projects/')


def project_page(p):
    cat, st = badges(p)
    features = ''.join(
        '''
                        <li class="pfeat">
                            <span class="pad {pad}" aria-hidden="true">{icon}</span>
                            <span class="pfeat-text">
                                <strong>{title}</strong>
                                <em>{body}</em>
                            </span>
                        </li>'''.format(pad=p['pad'], icon=icon_svg(n), title=t, body=b)
        for n, t, b in p['features'])

    steps = ''.join(
        '''
                        <li><span class="pstep-n">{n}</span><span>{t}</span></li>'''.format(n=i + 1, t=t)
        for i, t in enumerate(p['workflow']))

    tech = ''.join('<span class="chip">%s</span>' % t for t in p['tech'])
    links = ''.join(link_html(*l) for l in p['links'])
    tags = ''.join('<li class="pill">%s</li>' % t for t in p['tags'])

    body = '''
        <article class="section project-page">
            <div class="bloom" style="width:26rem;height:26rem;top:-4rem;right:-8rem;background:rgba(124,58,237,.12)">
            </div>
            <div class="wrap">
                <nav class="crumbs" aria-label="Breadcrumb">
                    <a href="/">Home</a><span aria-hidden="true">/</span>
                    <a href="/projects/">Projects</a><span aria-hidden="true">/</span>
                    <span aria-current="page">{brand}</span>
                </nav>

                <header class="project-hero reveal">
                    <span class="pad {pad}" aria-hidden="true">{icon}</span>
                    <div class="project-hero-text">
                        <span class="eyebrow">{category}</span>
                        <h1 class="display">{brand}</h1>
                        <p class="project-hero-sub">{subtitle}</p>
                        <ul class="chips project-card-tags">{tags}</ul>
                    </div>
                </header>

                <div class="card media-shot reveal">
                    <div class="pcover-wrap">
                        {cover}
                        <span class="pcover-sheen" aria-hidden="true"></span>
                        <div class="pcover-badges">{cat}{st}</div>
                    </div>
                </div>

                <div class="card project-detail reveal">
                    <p class="psheet-lead">{lead}</p>

                    <section class="psheet-sec">
                        <h4>What it does</h4>
                        <ul class="pfeats">{features}
                        </ul>
                    </section>

                    <section class="psheet-sec">
                        <h4>How it runs</h4>
                        <ol class="psteps">{steps}
                        </ol>
                    </section>

                    <div class="psheet-split">
                        <section class="psheet-sec">
                            <h4>Built with</h4>
                            <div class="chips">{tech}</div>
                        </section>

                        <section class="psheet-sec">
                            <h4>My role</h4>
                            <p class="psheet-role">{role}</p>
                        </section>
                    </div>

                    <section class="psheet-sec">
                        <h4>Links</h4>
                        <div class="plinks">{links}</div>
                    </section>
                </div>

                <nav class="project-pager">
                    <a class="btn" href="/projects/">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                             stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M19 12H5M11 18l-6-6 6-6" />
                        </svg>
                        All projects
                    </a>
                    <a class="btn btn-primary" href="/#connect">Get in touch</a>
                </nav>
            </div>
        </article>
'''.format(brand=p['brand'], pad=p['pad'], icon=ICON_MARKUP[p['id']],
           category=p['category'], subtitle=p['subtitle'], tags=tags,
           cover=covers.cover(p['id'], fit='meet'), cat=cat, st=st, lead=p['lead'],
           features=features, steps=steps, tech=tech, role=p['role'], links=links)

    desc = re.sub(r'\s+', ' ', p['summary'])
    return page('projects/' + p['id'],
                '%s — %s | Sahil Sharma' % (p['brand'], p['subtitle']),
                desc, body, '/projects/', jsonld=project_ld(p), ogtype='article',
                ogtitle='%s — %s' % (p['brand'], p['subtitle']))


# ------------------------------------------------------------------- main ---

def sitemap(urls):
    body = LF.join(
        '    <url>' + LF
        + '        <loc>%s</loc>' % u + LF
        + '        <changefreq>monthly</changefreq>' + LF
        + '        <priority>%s</priority>' % ('1.0' if u.rstrip('/') == SITE else '0.7') + LF
        + '    </url>' for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>' + LF
            + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + LF
            + body + LF + '</urlset>' + LF)


def main():
    # The pastel pad and icon for each project already live in the partials that
    # shipped with the old page; keep using exactly those marks.
    import json
    with io.open(os.path.join(SRC, 'data', 'icons.json'), encoding='utf-8') as f:
        marks = json.load(f)
    for p in PROJECTS:
        ICON_MARKUP[p['id']] = marks[p['id']]['svg']

    # Empty the folder rather than removing it: on Windows an open terminal or
    # a running preview server holds a handle on the directory itself, and
    # rmtree then fails even though every file inside is free.
    os.makedirs(OUT, exist_ok=True)
    for name in os.listdir(OUT):
        path = os.path.join(OUT, name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    ASSET_V['css'] = digest('styles.css')
    ASSET_V['js'] = digest('script.js')

    print('pages  (styles.css?v=%s, script.js?v=%s)' % (ASSET_V['css'], ASSET_V['js']))
    urls = [home(), projects_index()]
    for p in PROJECTS:
        urls.append(project_page(p))

    print()
    print('static')
    for name in ('styles.css', 'script.js', 'resume.pdf', 'robots.txt', 'site.webmanifest'):
        shutil.copy2(os.path.join(HERE, name), os.path.join(OUT, name))
        print('  %s' % name)
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'))
    print('  assets/')

    write('sitemap.xml', sitemap(urls))
    print('  sitemap.xml (%d urls)' % len(urls))

    total = sum(os.path.getsize(os.path.join(r, n))
                for r, d, f in os.walk(OUT) for n in f)
    print()
    print('built %d pages — %.0f KB total' % (len(urls), total / 1024.0))


if __name__ == '__main__':
    main()
