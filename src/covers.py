# -*- coding: utf-8 -*-
"""
Cover art for the project cards.

Inline SVG, same approach as the company site: sharp at any size, a couple of
KB each, and every scene shows what the project actually does rather than a
wordmark on a gradient. Deliberately filter-free - an SVG filter is
re-evaluated on every paint and a page carrying several of them janks scroll.
"""
import io
import json

PALETTE = {
    'ai-news':     {'bg': ('#07223a', '#051626', '#040e18'), 'glow': '#0ea5e9'},
    'teampulse':   {'bg': ('#06251d', '#05170f', '#03100a'), 'glow': '#10b981'},
    'feelthebeat': {'bg': ('#241436', '#170c24', '#0f0818'), 'glow': '#a855f7'},
    'mood2music':  {'bg': ('#2a0f21', '#1a0813', '#12050d'), 'glow': '#ec4899'},
    'srms':        {'bg': ('#0d1330', '#0a0e22', '#080a18'), 'glow': '#6366f1'},
    'storysofar':  {'bg': ('#2a1c08', '#1a1105', '#120b03'), 'glow': '#f59e0b'},
}

LABEL = {
    'ai-news': 'AI news articles being summarised and posted to three social platforms',
    'teampulse': 'A team task board with a weekly report counted straight from it',
    'feelthebeat': 'Listening history turned into a weekly playlist and a WhatsApp summary',
    'mood2music': 'A mood and language selection producing a ranked song list',
    'srms': 'A marks table with totals, percentage and grade computed from it',
    'storysofar': 'A Google Meet call producing structured minutes with decisions and action items',
}

SANS = 'system-ui, sans-serif'
MONO = 'ui-monospace, monospace'
J = ''.join


def grid(op=0.04):
    v = J('<line x1="%d" y1="0" x2="%d" y2="500" />' % (i * 64, i * 64) for i in range(13))
    h = J('<line x1="0" y1="%d" x2="800" y2="%d" />' % (i * 64, i * 64) for i in range(8))
    return '<g stroke="#ffffff" stroke-opacity="%s" stroke-width="1">%s%s</g>' % (op, v, h)


def ai_news():
    papers = J(
        '<g transform="translate(%d %d) rotate(%d)">'
        '<rect width="196" height="74" rx="10" fill="url(#pc-paper-ai-news)" />'
        '<rect x="14" y="14" width="%d" height="8" rx="4" fill="#0f172a" opacity="0.7" />'
        '<rect x="14" y="30" width="150" height="6" rx="3" fill="#0f172a" opacity="0.26" />'
        '<rect x="14" y="43" width="128" height="6" rx="3" fill="#0f172a" opacity="0.2" />'
        '<rect x="14" y="56" width="52" height="6" rx="3" fill="#0ea5e9" opacity="0.55" />'
        '</g>' % (i * 14, i * 46, -4 + i * 3, 112 - i * 14)
        for i in range(3))

    dests = J(
        '<g transform="translate(566 %d)">'
        '<rect width="190" height="58" rx="14" fill="#06263f" fill-opacity="0.92" stroke="#ffffff" stroke-opacity="0.13" />'
        '<circle cx="33" cy="29" r="15" fill="%s" fill-opacity="0.2" stroke="%s" stroke-opacity="0.55" />'
        '<text x="33" y="34" text-anchor="middle" font-family="%s" font-size="13" font-weight="700" fill="%s">%s</text>'
        '<text x="60" y="27" font-family="%s" font-size="12.5" font-weight="600" fill="#e2e8f0">%s</text>'
        '<text x="60" y="43" font-family="%s" font-size="10" fill="#7dd3fc">auto-posted</text>'
        '</g>' % (138 + i * 88, c, c, SANS, c, g, SANS, n, MONO)
        for i, (n, g, c) in enumerate([('Twitter (X)', 'X', '#e2e8f0'),
                                       ('LinkedIn', 'in', '#38bdf8'),
                                       ('WhatsApp', 'W', '#34d399')]))

    return (grid() +
            '<g transform="translate(44 118)">' + papers + '</g>'
            '<g stroke="#38bdf8" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="5 7" fill="none">'
            '<path d="M262 246h56" /></g>'
            '<g transform="translate(320 176)">'
            '<rect width="164" height="148" rx="18" fill="#041a2c" fill-opacity="0.94" stroke="#38bdf8" stroke-opacity="0.34" />'
            '<g transform="translate(82 52)">'
            '<path d="M0 -26l6.5 17.5L24 -2l-17.5 6.5L0 22l-6.5-17.5L-24 -2l17.5-6.5z" fill="#38bdf8" fill-opacity="0.9" />'
            '</g>'
            '<text x="82" y="100" text-anchor="middle" font-family="%s" font-size="13" font-weight="700" fill="#e0f2fe">Gemini</text>'
            '<text x="82" y="120" text-anchor="middle" font-family="%s" font-size="10.5" fill="#7dd3fc">summarise</text>'
            '</g>'
            '<g stroke="#38bdf8" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="5 7" fill="none">'
            '<path d="M486 250h40" /><path d="M526 250v-88h34" /><path d="M526 250h34" /><path d="M526 250v88h34" />'
            '</g>' % (SANS, SANS) + dests)


def teampulse():
    cols = [('To do', ['#34d399', '#34d399', '#6ee7b7']),
            ('Doing', ['#fbbf24', '#34d399']),
            ('Done', ['#6ee7b7', '#6ee7b7', '#34d399', '#6ee7b7'])]
    board = ''
    for ci, (title, rows) in enumerate(cols):
        cards = J(
            '<g transform="translate(14 %d)">'
            '<rect width="148" height="34" rx="9" fill="#02241c" stroke="#ffffff" stroke-opacity="0.12" />'
            '<circle cx="16" cy="17" r="5" fill="%s" />'
            '<rect x="30" y="10" width="%d" height="6" rx="3" fill="#ffffff" fill-opacity="0.3" />'
            '<rect x="30" y="21" width="%d" height="5" rx="2.5" fill="#ffffff" fill-opacity="0.15" />'
            '</g>' % (38 + ri * 42, c, 92 - ri * 11, 62 - ri * 7)
            for ri, c in enumerate(rows))
        board += ('<g transform="translate(%d 0)">'
                  '<rect width="176" height="214" rx="14" fill="#04352a" fill-opacity="0.6" stroke="#ffffff" stroke-opacity="0.1" />'
                  '<text x="16" y="26" font-family="%s" font-size="11.5" font-weight="700" fill="#a7f3d0" letter-spacing="0.8">%s</text>'
                  '%s</g>' % (ci * 196, SANS, title.upper(), cards))

    bars = J('<rect x="%d" y="%d" width="20" height="%d" rx="5" fill="#34d399" fill-opacity="%.2f" />'
             % (22 + i * 34, 104 - h, h, 0.35 + 0.09 * i)
             for i, h in enumerate([26, 38, 30, 48, 42, 56, 34]))

    stats = J('<g transform="translate(0 %d)">'
              '<text x="0" y="0" font-family="%s" font-size="11" fill="#a7f3d0">%s</text>'
              '<text x="244" y="0" text-anchor="end" font-family="%s" font-size="12.5" font-weight="700" fill="#ecfdf5">%s</text>'
              '</g>' % (i * 26, SANS, k, MONO, v)
              for i, (k, v) in enumerate([('Tasks closed', '38'), ('Standups logged', '45')]))

    live = J('<g transform="translate(14 %d)">'
             '<circle cx="10" cy="10" r="9" fill="#34d399" fill-opacity="0.18" stroke="#34d399" stroke-opacity="0.5" />'
             '<rect x="26" y="6" width="%d" height="5" rx="2.5" fill="#ffffff" fill-opacity="0.26" />'
             '<rect x="26" y="15" width="%d" height="4" rx="2" fill="#ffffff" fill-opacity="0.14" />'
             '</g>' % (40 + i * 40, 48 - i * 6, 34 - i * 4) for i in range(4))

    return ('<g transform="translate(52 62)">' + board + '</g>'
            '<g transform="translate(52 318)">'
            '<rect width="568" height="130" rx="16" fill="#031e18" fill-opacity="0.94" stroke="#34d399" stroke-opacity="0.34" />'
            '<text x="22" y="32" font-family="%s" font-size="12.5" font-weight="700" fill="#d1fae5">Weekly report</text>'
            '<text x="22" y="50" font-family="%s" font-size="10.5" fill="#6ee7b7">counted from the board, not retyped</text>'
            '%s<g transform="translate(300 62)">%s</g></g>'
            '<g transform="translate(646 62)">'
            '<rect width="102" height="214" rx="14" fill="#04352a" fill-opacity="0.6" stroke="#ffffff" stroke-opacity="0.1" />'
            '<text x="14" y="26" font-family="%s" font-size="11.5" font-weight="700" fill="#a7f3d0">LIVE</text>'
            '%s</g>' % (SANS, SANS, bars, stats, SANS, live))


def feelthebeat():
    vals = [18, 34, 52, 30, 66, 44, 78, 40, 58, 26, 70, 48, 36, 62, 30, 54, 22, 44, 68, 32, 50, 38, 60, 28]
    bars = J('<rect x="%d" y="%d" width="9" height="%d" rx="4.5" fill="#c084fc" fill-opacity="%.2f" />'
             % (i * 17, 84 - h, h, 0.3 + 0.5 * (h / 78.0)) for i, h in enumerate(vals))

    tracks = J('<g transform="translate(20 %d)">'
               '<circle cx="9" cy="9" r="9" fill="#a855f7" fill-opacity="0.2" stroke="#c084fc" stroke-opacity="0.5" />'
               '<path d="M6.5 5l6 4-6 4z" fill="#e9d5ff" />'
               '<rect x="26" y="5" width="%d" height="6" rx="3" fill="#ffffff" fill-opacity="0.28" />'
               '<text x="290" y="13" text-anchor="end" font-family="%s" font-size="9.5" fill="#c4b5fd">%s</text>'
               '</g>' % (44 + i * 26, 188 - i * 24, MONO, d)
               for i, d in enumerate(['3:42', '4:07', '2:58']))

    return ('<g transform="translate(52 86)">'
            '<text x="0" y="0" font-family="%s" font-size="11.5" font-weight="700" fill="#e9d5ff" letter-spacing="0.8">ON REPEAT</text>'
            '<g transform="translate(0 20)">%s</g>'
            '<line x1="0" y1="112" x2="408" y2="112" stroke="#ffffff" stroke-opacity="0.14" />'
            '<text x="0" y="130" font-family="%s" font-size="10" fill="#a78bfa">rolling window &#183; play count &#8805; 3</text>'
            '</g>'
            '<g stroke="#c084fc" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="5 7" fill="none">'
            '<path d="M232 244v40h-60v44" /><path d="M232 284h236v34" /></g>'
            '<g transform="translate(52 318)">'
            '<rect width="330" height="132" rx="16" fill="#1a0f2b" fill-opacity="0.94" stroke="#a855f7" stroke-opacity="0.34" />'
            '<text x="20" y="30" font-family="%s" font-size="12.5" font-weight="700" fill="#f3e8ff">This week&#8217;s playlist</text>'
            '%s</g>'
            '<g transform="translate(424 318)">'
            '<rect width="324" height="132" rx="16" fill="#0d2b22" fill-opacity="0.94" stroke="#34d399" stroke-opacity="0.34" />'
            '<g transform="translate(20 20)">'
            '<circle cx="13" cy="13" r="13" fill="#25d366" fill-opacity="0.18" stroke="#34d399" stroke-opacity="0.55" />'
            '<text x="13" y="18" text-anchor="middle" font-family="%s" font-size="13" font-weight="700" fill="#6ee7b7">W</text>'
            '<text x="38" y="12" font-family="%s" font-size="12" font-weight="600" fill="#d1fae5">Your week in music</text>'
            '<text x="38" y="27" font-family="%s" font-size="9.5" fill="#6ee7b7">sent Sunday &#183; 9:00</text>'
            '</g>'
            '<g transform="translate(20 66)">'
            '<rect width="284" height="48" rx="12" fill="#04150f" stroke="#ffffff" stroke-opacity="0.1" />'
            '<rect x="14" y="13" width="242" height="6" rx="3" fill="#ffffff" fill-opacity="0.26" />'
            '<rect x="14" y="27" width="186" height="6" rx="3" fill="#ffffff" fill-opacity="0.16" />'
            '</g></g>'
            '<g transform="translate(600 74)">'
            '<rect width="148" height="52" rx="26" fill="#160d24" fill-opacity="0.92" stroke="#c084fc" stroke-opacity="0.4" />'
            '<circle cx="28" cy="26" r="9" fill="none" stroke="#c084fc" stroke-width="2" />'
            '<path d="M28 21v5l3.5 2" stroke="#c084fc" stroke-width="2" fill="none" stroke-linecap="round" />'
            '<text x="48" y="24" font-family="%s" font-size="11.5" font-weight="600" fill="#e9d5ff">GitHub Actions</text>'
            '<text x="48" y="38" font-family="%s" font-size="9.5" fill="#a78bfa">cron &#183; no server</text>'
            '</g>' % (SANS, bars, MONO, SANS, tracks, SANS, SANS, MONO, SANS, MONO))


def mood2music():
    langs = J('<g transform="translate(%d 0)">'
              '<rect width="68" height="30" rx="15" fill="%s" fill-opacity="%s" stroke="%s" stroke-opacity="%s" />'
              '<text x="34" y="20" text-anchor="middle" font-family="%s" font-size="11" font-weight="600" fill="%s">%s</text>'
              '</g>' % (i * 78,
                        '#ec4899' if i == 0 else '#ffffff', '0.24' if i == 0 else '0.07',
                        '#f9a8d4' if i == 0 else '#ffffff', '0.6' if i == 0 else '0.14',
                        SANS, '#fce7f3' if i == 0 else '#9ca3af', l)
              for i, l in enumerate(['Hindi', 'English', 'Punjabi']))

    moods = [('Happy', '#fbbf24', True), ('Calm', '#38bdf8', False), ('Energetic', '#f472b6', False)]
    mood_rows = J('<g transform="translate(0 %d)">'
                  '<rect width="224" height="36" rx="12" fill="%s" fill-opacity="%s" stroke="%s" stroke-opacity="%s" />'
                  '<circle cx="22" cy="18" r="7" fill="%s" fill-opacity="%s" />'
                  '<text x="42" y="23" font-family="%s" font-size="12.5" font-weight="600" fill="%s">%s</text>'
                  '%s</g>' % (i * 46, c, '0.2' if on else '0.07', c, '0.6' if on else '0.16',
                              c, '0.95' if on else '0.3', SANS,
                              '#fdf2f8' if on else '#9ca3af', n,
                              '<path d="M200 18l4 4.5 8-9" stroke="#fce7f3" stroke-width="2.4" fill="none" '
                              'stroke-linecap="round" stroke-linejoin="round" />' if on else '')
                  for i, (n, c, on) in enumerate(moods))

    results = J('<g transform="translate(24 %d)">'
                '<rect width="300" height="36" rx="11" fill="#190712" stroke="#ffffff" stroke-opacity="0.1" />'
                '<circle cx="22" cy="18" r="11" fill="#1db954" fill-opacity="0.2" stroke="#1db954" stroke-opacity="0.55" />'
                '<path d="M18.5 13l7 5-7 5z" fill="#86efac" />'
                '<rect x="44" y="11" width="%d" height="6" rx="3" fill="#ffffff" fill-opacity="0.3" />'
                '<rect x="44" y="23" width="%d" height="5" rx="2.5" fill="#ffffff" fill-opacity="0.15" />'
                '<text x="286" y="22" text-anchor="end" font-family="%s" font-size="10" font-weight="700" fill="#f9a8d4">%d</text>'
                '</g>' % (50 + i * 44, 178 - i * 22, 118 - i * 16, MONO, i + 1)
                for i in range(5))

    return ('<g transform="translate(52 96)">'
            '<rect width="272" height="308" rx="18" fill="#200a19" fill-opacity="0.92" stroke="#ffffff" stroke-opacity="0.12" />'
            '<text x="24" y="34" font-family="%s" font-size="11.5" font-weight="700" fill="#fbcfe8" letter-spacing="0.8">LANGUAGE</text>'
            '<g transform="translate(24 46)">%s</g>'
            '<text x="24" y="124" font-family="%s" font-size="11.5" font-weight="700" fill="#fbcfe8" letter-spacing="0.8">MOOD</text>'
            '<g transform="translate(24 136)">%s</g>'
            '<text x="24" y="288" font-family="%s" font-size="10" fill="#f9a8d4">90,000+ track dataset</text>'
            '</g>'
            '<g stroke="#f472b6" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="5 7" fill="none">'
            '<path d="M338 250h44" /></g><circle cx="386" cy="250" r="3.5" fill="#f472b6" />'
            '<g transform="translate(400 96)">'
            '<rect width="348" height="308" rx="18" fill="#2a0f21" fill-opacity="0.94" stroke="#f472b6" stroke-opacity="0.34" />'
            '<text x="24" y="34" font-family="%s" font-size="12.5" font-weight="700" fill="#fce7f3">Recommended for you</text>'
            '%s'
            '<g transform="translate(24 276)">'
            '<path d="M0 8a8 8 0 1116 0" stroke="#f9a8d4" stroke-width="2" fill="none" />'
            '<text x="24" y="12" font-family="%s" font-size="10" fill="#f9a8d4">likes and skips refine the next run</text>'
            '</g></g>' % (SANS, langs, SANS, mood_rows, MONO, SANS, results, MONO))


def srms():
    rows = [('Mathematics', '78', '100', '#6ee7b7'), ('Physics', '71', '100', '#6ee7b7'),
            ('Chemistry', '64', '100', '#fcd34d'), ('Computer Sci.', '92', '100', '#6ee7b7')]
    table = J('<g transform="translate(0 %d)">'
              '<rect x="20" y="0" width="390" height="40" rx="10" fill="#ffffff" fill-opacity="0.04" />'
              '<circle cx="40" cy="20" r="6" fill="%s" fill-opacity="0.85" />'
              '<text x="58" y="25" font-family="%s" font-size="12.5" fill="#e2e8f0">%s</text>'
              '<text x="318" y="25" text-anchor="end" font-family="%s" font-size="13" font-weight="700" fill="%s">%s</text>'
              '<text x="394" y="25" text-anchor="end" font-family="%s" font-size="12" fill="#64748b">%s</text>'
              '</g>' % (92 + i * 50, c, SANS, n, MONO, c, sc, MONO, mx)
              for i, (n, sc, mx, c) in enumerate(rows))

    summary = J('<g transform="translate(24 %d)">'
                '<text x="0" y="0" font-family="%s" font-size="11.5" fill="#94a3b8">%s</text>'
                '<text x="158" y="0" text-anchor="end" font-family="%s" font-size="13" font-weight="700" fill="%s">%s</text>'
                '</g>' % (218 + i * 40, SANS, k, MONO, c, v)
                for i, (k, v, c) in enumerate([('Total', '305 / 400', '#e2e8f0'),
                                               ('Grade', 'B+', '#a5b4fc'),
                                               ('Status', 'PASS', '#6ee7b7')]))

    return (grid() +
            '<g transform="translate(48 86)">'
            '<rect width="430" height="326" rx="16" fill="#0a1029" fill-opacity="0.94" stroke="#ffffff" stroke-opacity="0.13" />'
            '<rect x="20" y="20" width="96" height="20" rx="10" fill="#6366f1" fill-opacity="0.22" stroke="#818cf8" stroke-opacity="0.45" />'
            '<text x="68" y="34" text-anchor="middle" font-family="%s" font-size="10" font-weight="700" fill="#c7d2fe" letter-spacing="1.2">MARKS</text>'
            '<line x1="20" y1="58" x2="410" y2="58" stroke="#ffffff" stroke-opacity="0.12" />'
            '<text x="20" y="76" font-family="%s" font-size="10" fill="#94a3b8" letter-spacing="0.6">SUBJECT</text>'
            '<text x="318" y="76" text-anchor="end" font-family="%s" font-size="10" fill="#94a3b8" letter-spacing="0.6">SCORED</text>'
            '<text x="394" y="76" text-anchor="end" font-family="%s" font-size="10" fill="#94a3b8" letter-spacing="0.6">MAX</text>'
            '%s</g>'
            '<g stroke="#818cf8" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="5 7" fill="none">'
            '<path d="M492 250h34" /></g><circle cx="530" cy="250" r="3.5" fill="#818cf8" />'
            '<g transform="translate(546 86)">'
            '<rect width="206" height="326" rx="16" fill="#0b1130" fill-opacity="0.94" stroke="#818cf8" stroke-opacity="0.36" />'
            '<text x="24" y="38" font-family="%s" font-size="11.5" font-weight="700" fill="#c7d2fe" letter-spacing="0.8">RESULT</text>'
            '<g transform="translate(103 128)">'
            '<circle r="56" fill="none" stroke="#ffffff" stroke-opacity="0.09" stroke-width="12" />'
            '<circle r="56" fill="none" stroke="#818cf8" stroke-width="12" stroke-linecap="round" '
            'stroke-dasharray="271 352" transform="rotate(-90)" />'
            '<text y="2" text-anchor="middle" font-family="%s" font-size="30" font-weight="700" fill="#e2e8f0">76.3</text>'
            '<text y="22" text-anchor="middle" font-family="%s" font-size="11" fill="#94a3b8">percent</text>'
            '</g>%s'
            '<text x="24" y="306" font-family="%s" font-size="9.5" fill="#64748b">computed, never typed in</text>'
            '</g>' % (SANS, SANS, SANS, SANS, table, SANS, MONO, SANS, summary, MONO))


def storysofar():
    people = [('Priya', '#fbbf24'), ('Arjun', '#38bdf8'), ('You', '#34d399')]
    tiles = J('<g transform="translate(%d %d)">'
              '<rect width="150" height="96" rx="11" fill="#1c1206" stroke="#ffffff" stroke-opacity="0.12" />'
              '<circle cx="75" cy="40" r="20" fill="%s" fill-opacity="0.2" stroke="%s" stroke-opacity="0.5" />'
              '<text x="75" y="46" text-anchor="middle" font-family="%s" font-size="15" font-weight="700" fill="%s">%s</text>'
              '<text x="12" y="84" font-family="%s" font-size="10.5" fill="#fde68a">%s</text>'
              '</g>' % (12 + (i % 2) * 162, 12 + (i // 2) * 108, c, c, SANS, c, n[0], SANS, n)
              for i, (n, c) in enumerate(people))

    rows = [('Summary', 'what the meeting was about', '#fcd34d'),
            ('Decisions', 'settled, stated plainly', '#fbbf24'),
            ('Action items', 'with owner and date', '#f59e0b')]
    panel = J('<g transform="translate(22 %d)">'
              '<rect width="272" height="60" rx="12" fill="#150d04" stroke="#ffffff" stroke-opacity="0.1" />'
              '<circle cx="22" cy="30" r="8" fill="%s" fill-opacity="0.22" stroke="%s" stroke-opacity="0.55" />'
              '<path d="M18.5 30l2.5 2.8 5-5.6" stroke="%s" stroke-width="2" fill="none" '
              'stroke-linecap="round" stroke-linejoin="round" />'
              '<text x="42" y="26" font-family="%s" font-size="12" font-weight="700" fill="#fef3c7">%s</text>'
              '<text x="42" y="43" font-family="%s" font-size="10" fill="#d97706">%s</text>'
              '</g>' % (58 + i * 72, c, c, c, SANS, t, SANS, sub)
              for i, (t, sub, c) in enumerate(rows))

    return ('<g transform="translate(44 96)">'
            '<rect width="338" height="240" rx="16" fill="#0f0a03" fill-opacity="0.94" stroke="#ffffff" stroke-opacity="0.13" />'
            '%s'
            '<g transform="translate(94 204)">'
            '<rect width="150" height="30" rx="15" fill="#f59e0b" fill-opacity="0.9" />'
            '<circle cx="26" cy="15" r="5.5" fill="#1a1105" />'
            '<text x="46" y="20" font-family="%s" font-size="12" font-weight="700" fill="#1a1105">Recording</text>'
            '</g></g>'
            '<g stroke="#fbbf24" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="5 7" fill="none">'
            '<path d="M396 216h30" /></g><circle cx="430" cy="216" r="3.5" fill="#fbbf24" />'
            '<g transform="translate(444 74)">'
            '<rect width="312" height="352" rx="16" fill="#1a1105" fill-opacity="0.95" stroke="#f59e0b" stroke-opacity="0.36" />'
            '<text x="22" y="34" font-family="%s" font-size="12.5" font-weight="700" fill="#fef3c7">Minutes</text>'
            '<text x="290" y="34" text-anchor="end" font-family="%s" font-size="9.5" fill="#d97706">ready in seconds</text>'
            '%s'
            '<line x1="22" y1="288" x2="290" y2="288" stroke="#ffffff" stroke-opacity="0.12" />'
            '<text x="22" y="310" font-family="%s" font-size="10.5" fill="#fbbf24">Priya to send the revised deck</text>'
            '<text x="22" y="330" font-family="%s" font-size="9.5" fill="#92400e">full transcript kept alongside</text>'
            '</g>' % (tiles, SANS, SANS, MONO, panel, SANS, MONO))


SCENES = {'ai-news': ai_news, 'teampulse': teampulse, 'feelthebeat': feelthebeat,
          'mood2music': mood2music, 'srms': srms, 'storysofar': storysofar}


def cover(pid, fit='slice'):
    """fit='slice' crops to fill the box (cards); 'meet' shows all of it."""
    p = PALETTE[pid]
    return (
        '<svg class="pcover" viewBox="0 0 800 500" preserveAspectRatio="xMidYMid %s" '
        'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s">'
        '<defs>'
        '<linearGradient id="pc-bg-%s" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="%s" /><stop offset="0.55" stop-color="%s" /><stop offset="1" stop-color="%s" />'
        '</linearGradient>'
        '<radialGradient id="pc-glow-%s" cx="0.5" cy="0.18" r="0.71">'
        '<stop offset="0" stop-color="%s" stop-opacity="0.8" />'
        '<stop offset="0.5" stop-color="%s" stop-opacity="0.22" />'
        '<stop offset="1" stop-color="%s" stop-opacity="0" />'
        '</radialGradient>'
        '<linearGradient id="pc-paper-%s" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#f8fafc" /><stop offset="1" stop-color="#dbe2ee" />'
        '</linearGradient>'
        '<radialGradient id="pc-vig-%s" cx="0.5" cy="0.45" r="0.78">'
        '<stop offset="0.5" stop-color="#000" stop-opacity="0" />'
        '<stop offset="1" stop-color="#000" stop-opacity="0.75" />'
        '</radialGradient>'
        '</defs>'
        '<rect width="800" height="500" fill="url(#pc-bg-%s)" />'
        '<rect width="800" height="500" fill="url(#pc-glow-%s)" />'
        '%s'
        '<rect width="800" height="500" fill="url(#pc-vig-%s)" />'
        '</svg>' % (fit, LABEL[pid], pid, p['bg'][0], p['bg'][1], p['bg'][2],
                    pid, p['glow'], p['glow'], p['glow'], pid, pid, pid, pid,
                    SCENES[pid](), pid))


if __name__ == '__main__':
    out = {pid: cover(pid) for pid in PALETTE}
    io.open('covers.json', 'w', encoding='utf-8').write(json.dumps(out))
    for pid, svg in out.items():
        print('%-12s %6d chars' % (pid, len(svg)))
