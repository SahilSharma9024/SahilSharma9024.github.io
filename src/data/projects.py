# -*- coding: utf-8 -*-
"""
Project content.

Everything the old accordions said is still here; it is cut into labelled
pieces rather than left as paragraphs, so a reader can scan it. Nothing about
internal architecture that was not already public has been added.
"""

# Small line icons for the feature rows. Drawn on a 24 box, stroked, so they
# inherit currentColor and match the icons already used elsewhere on the page.
ICON = {
    'search': '<path d="M11 19a8 8 0 100-16 8 8 0 000 16zM21 21l-4.35-4.35"/>',
    'spark': '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>',
    'send': '<path d="M22 2L11 13M22 2l-7 20-4-9-9-4z"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    'list': '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    'users': '<path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/>',
    'calendar': '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    'chart': '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
    'bell': '<path d="M18 8a6 6 0 10-12 0c0 7-3 8-3 8h18s-3-1-3-8"/><path d="M13.7 21a2 2 0 01-3.4 0"/>',
    'book': '<path d="M4 19.5A2.5 2.5 0 016.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/>',
    'swap': '<path d="M7 16H3M3 16l4-4M3 16l4 4"/><path d="M17 8h4M21 8l-4-4M21 8l-4 4"/>',
    'heart': '<path d="M20.8 4.6a5.5 5.5 0 00-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 00-7.8 7.8l8.8 8.8 8.8-8.8a5.5 5.5 0 000-7.8z"/>',
    'music': '<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>',
    'filter': '<path d="M22 3H2l8 9.5V19l4 2v-8.5z"/>',
    'db': '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 5v14c0 1.7-4 3-9 3s-9-1.3-9-3V5"/><path d="M21 12c0 1.7-4 3-9 3s-9-1.3-9-3"/>',
    'lock': '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/>',
    'check': '<path d="M20 6L9 17l-5-5"/>',
    'cloud': '<path d="M18 10h-1.3A7 7 0 104 15.9"/><path d="M13 19l3-3 3 3M16 16v6"/>',
    'code': '<path d="M16 18l6-6-6-6M8 6l-6 6 6 6"/>',
}

PROJECTS = [
    # ------------------------------------------------------------- TeamPulse --
    {
        'id': 'teampulse',
        'brand': 'TeamPulse',
        'subtitle': 'Team Operations Platform',
        'category': 'Team Ops',
        'status': 'live',
        'status_label': 'Product build',
        'pad': 'pad-lav',
        'summary': 'Meetings, standups, tasks, attendance and a live wiki in one role-aware '
                     'platform, built end to end and used by the team daily.',
        'meta': 'ASP.NET Core 9 · SQL Server · SignalR',
        'meta_note': 'Shipped as a real internal tool',
        'tags': ['Meetings', 'Standups', 'Attendance'],
        'lead': 'Most teams run on a scatter of spreadsheets, chat threads and calendar '
                'invites. TeamPulse replaces that with one role-aware web application where '
                'work is planned, tracked, reviewed and documented. Background jobs handle the '
                'recurring housekeeping — attendance close-outs, leave accrual, scheduled '
                'reminders — so the system keeps itself current without anyone maintaining it.',
        'features': [
            ('lock', 'Role-based access', 'Separate experiences for Admins, Leads and Members, enforced server-side.'),
            ('calendar', 'Meetings suite', 'Scheduling with approvals, live rooms, chat, Meet links, automated minutes.'),
            ('list', 'Standups and tasks', 'Assign, comment, raise issues, reassign, finalise against evidence.'),
            ('clock', 'Attendance and leave', 'Requests, disputes, holidays, per-designation policies, monthly accrual.'),
            ('chart', 'Objectives and KPIs', 'Define objectives, run check-ins, capture KPI snapshots over time.'),
            ('book', 'Collaborative wiki', 'Real-time multi-user editing, rich and Markdown modes, sanitised HTML.'),
            ('bell', 'Notifications and mentions', 'Live in-app panel with unread counts, plus email and WhatsApp delivery.'),
            ('users', 'Dashboards', 'Global and per-team views with point-in-time snapshots and CSV export.'),
        ],
        'workflow': [
            'Members log daily standups and progress; leads plan work and review submissions.',
            'Meetings are scheduled, approved and run in live rooms; minutes are summarised to attendees automatically.',
            'Attendance and leave requests flow to leads; approvals adjust balances and stop false absences on approved-leave days.',
            'Background services accrue leave monthly, close out attendance daily, and push review reminders on schedule.',
            'Teams document processes in the shared wiki, editing concurrently with live sync.',
        ],
        'tech': ['C#', 'ASP.NET Core 9 (MVC)', 'EF Core 9', 'SQL Server', 'ASP.NET Core Identity',
                 'SignalR', 'Hosted Services', 'Markdig', 'HtmlSanitizer', 'SMTP', 'WhatsApp',
                 'Razor', 'Bootstrap 5'],
        'role': 'I designed and built the platform end to end — the data model and migrations, '
                'role-based authorization, and every module: meetings, standups and tasks, the '
                'attendance and leave accrual engine, objectives and KPIs, the real-time wiki, '
                'dashboards with CSV export, and the notification system. I also wrote the '
                'background job services, the email/WhatsApp/Meet integrations, and the '
                'responsive UI across desktop and mobile.',
        'links': [('private', 'GitHub Repository', '', 'Private')],
    },

    # ------------------------------------------------------------ StorySoFar --
    {
        'id': 'storysofar',
        'brand': 'StorySoFar',
        'subtitle': 'Minutes for Google Meet',
        'category': 'Meeting AI',
        'status': 'live',
        'status_label': 'Product build',
        'pad': 'pad-lemon',
        'summary': 'One click in a Meet call and structured minutes are waiting when it '
                     'ends: summary, decisions and action items. Nothing joins the call.',
        'meta': 'Chrome extension \u00b7 Google Meet',
        'meta_note': 'Nothing joins the call',
        'tags': ['Minutes', 'Transcripts', 'No bot'],
        'lead': 'You join the call as usual. One click starts StorySoFar, and when the meeting '
                'ends you have clean, structured minutes within seconds. Nothing joins the '
                'call, so there is no recording assistant in the participant list for anyone '
                'to notice, question or approve.',
        'features': [
            ('users', 'Captures everyone', 'Both sides of the call, so your own commitments land in the action items.'),
            ('check', 'Names real people', 'Participants come from the call, so it reads \u201cPriya to send the deck\u201d.'),
            ('clock', 'Ready when you stop', 'Written the moment the call ends \u2014 no upload, no queue, no waiting.'),
            ('cloud', 'Light on the machine', 'Audio is discarded as it goes; a two-hour meeting leaves kilobytes of text.'),
            ('shield', 'Never loses a meeting', 'A closed tab, a dropped call or a sleeping laptop is recovered, not lost.'),
            ('code', 'Yours to edit', 'Minutes open in an editor \u2014 fix a name, sharpen a decision, save.'),
            ('spark', 'Regenerate anytime', 'Rebuild the write-up from the stored transcript as often as you like.'),
            ('search', 'Searchable history', 'Every meeting and transcript in one list, with full-text search.'),
        ],
        'workflow': [
            'You join a Google Meet call as normal and click Start.',
            'The conversation is turned into text continuously, in short passes, while the audio behind it is discarded.',
            'Stopping the recording \u2014 or simply leaving the call \u2014 ends the capture.',
            'The minutes are generated within seconds and a notification says they are ready.',
            'You get summary, key points, decisions, action items with owners and dates, plus the full transcript.',
            'Edit, regenerate, copy, or download as Markdown or plain text.',
        ],
        'tech': ['Chrome Extension', 'JavaScript', 'Google Meet', 'Speech-to-text',
                 'LLM summarisation', 'Markdown export'],
        'role': 'I made this one \u2014 the in-call capture, the continuous transcription pass, '
                'the minutes generation, the editor, the export options and the searchable '
                'history.',
        'links': [('private', 'GitHub Repository', '', 'Private')],
    },

    # -------------------------------------------------------------- SnippetsAI --
    {
        'id': 'ai-news',
        'brand': 'SnippetsAI',
        'subtitle': 'AI News Snippet Automation',
        'category': 'Automation',
        'status': 'live',
        'status_label': 'Personal project',
        'pad': 'pad-sky',
        'summary': 'Finds trending AI news, writes a short summary of each with Gemini, then '
                     'posts them to Twitter, LinkedIn and WhatsApp on its own.',
        'meta': 'Python · Selenium · Gemini',
        'meta_note': 'Runs unattended end to end',
        'tags': ['News search', 'Summary', 'Auto-posting'],
        'lead': 'Keeping an audience current on AI normally means searching for news, writing '
                'posts and publishing them to each platform by hand. SnippetsAI does the whole '
                'loop on its own: it finds what is trending, turns each article into a short, '
                'readable summary, and posts it everywhere at once.',
        'features': [
            ('search', 'Automated discovery', 'Serper and SerpAPI surface trending AI stories against set keywords.'),
            ('spark', 'AI summaries', 'Gemini condenses each article into a short post written for social media.'),
            ('send', 'Multi-platform posting', 'One workflow publishes to Twitter (X), LinkedIn and WhatsApp groups.'),
            ('shield', 'Profile-based login', 'Selenium drives an already-signed-in Chrome profile, so no credentials are handled.'),
            ('list', 'Activity logging', 'Every summary and post is written to CSV, Markdown or text for review.'),
        ],
        'workflow': [
            'Searches Serper and SerpAPI for trending AI topics and collects article URLs.',
            'Sends the collected links to Gemini, which returns short summaries suited to social posts.',
            'Launches Chrome through Selenium using a pre-authenticated profile.',
            'Posts the summaries to Twitter (X) and LinkedIn with platform-appropriate formatting.',
            'Sends the same summaries to selected WhatsApp groups.',
            'Records every post locally for future reference and auditing.',
        ],
        'tech': ['Python', 'Selenium', 'Google Gemini API', 'Serper API', 'SerpAPI', 'CSV / MD / TXT'],
        'role': 'I designed and built the entire pipeline on my own: the news discovery '
                'integrations, the Gemini summarisation layer, Selenium automation for all '
                'three platforms, Chrome profile management for authenticated sessions, the '
                'logging layer, and the testing and tuning needed to make an unattended run '
                'reliable.',
        'links': [('private', 'GitHub Repository', '', 'Private'),
                  ('demo', 'Watch Demo Video',
                   'https://drive.google.com/file/d/1gk5Jqcu7jY6SeG5mIQ6x5z4iL5KbDtPN/view?usp=drive_link', '')],
    },

    # ------------------------------------------------------------ FeelTheBeat --
    {
        'id': 'feelthebeat',
        'brand': 'FeelTheBeat',
        'subtitle': 'Weekly playlist builder',
        'category': 'Music AI',
        'status': 'live',
        'status_label': 'Personal project',
        'pad': 'pad-peach',
        'summary': 'Tracks what you have on repeat, rebuilds a discovery playlist every '
                     'week, and sends an AI-written wrap-up to WhatsApp. No server.',
        'meta': 'Python · Spotify / YT Music · Gemini',
        'meta_note': 'Runs free on GitHub Actions',
        'tags': ['Playlists', 'Weekly wrap-up', 'Hands-off'],
        'lead': 'FeelTheBeat is a serverless music assistant that curates listening on a '
                'schedule. The same codebase drives both Spotify and YouTube Music — switching '
                'between them is a one-line config change, because both sit behind a shared '
                'five-function contract.',
        'features': [
            ('swap', 'Platform-agnostic', 'Spotify and YouTube Music are interchangeable behind one shared contract.'),
            ('heart', 'Library curation', 'Detects heavy rotation over a rolling window; skips anything already saved.'),
            ('music', 'Weekly discovery', 'Rebuilds a playlist each week seeded by what you are listening to now.'),
            ('spark', 'AI wrap-up', 'Gemini writes the weekly summary, with a deterministic fallback if the call fails.'),
            ('send', 'WhatsApp delivery', 'Twilio content templates bypass the 24-hour window for unattended sending.'),
            ('clock', 'Config-driven schedule', 'Run day, hour and timezone live in config, not in CI YAML.'),
            ('cloud', 'Zero-cost hosting', 'GitHub Actions cron — no server, no database, no hosting bill.'),
        ],
        'workflow': [
            'GitHub Actions triggers the application hourly.',
            'It checks the configured day, hour and timezone, and exits immediately if nothing is due.',
            'The selected backend authenticates, with credentials reconstructed from CI secrets at runtime.',
            'Recent listening history is fetched and play counts are tallied across a rolling window.',
            'Tracks over the repeat threshold are filtered against the library, and the rest are saved.',
            'On the weekly run those favourites seed the recommendation engine and the playlist is rebuilt.',
            'Gemini writes a personalised summary and Twilio delivers it to WhatsApp.',
        ],
        'tech': ['Python', 'Spotify API (Spotipy)', 'YouTube Music API (ytmusicapi)',
                 'Google Gemini API', 'Twilio WhatsApp API', 'GitHub Actions', 'cron'],
        'role': 'Designed and built the whole system — the abstraction unifying two separate '
                'music APIs, the heavy-rotation heuristic, the recommendation and playlist '
                'pipeline, the Gemini summarisation layer, WhatsApp delivery through Twilio, '
                'and the config-driven CI scheduling.',
        'links': [('repo', 'GitHub Repository', 'https://github.com/SahilSharma9024/FeelTheBeat', '')],
    },

    # ------------------------------------------------------------- Mood2Music --
    {
        'id': 'mood2music',
        'brand': 'Mood2Music',
        'subtitle': 'Mood-based recommendations',
        'category': 'Recommender',
        'status': 'live',
        'status_label': 'Personal project',
        'pad': 'pad-rose',
        'summary': 'Pick a language and a mood, and it ranks matches from a 90,000-track '
                     'dataset, plays them on Spotify and learns as you go.',
        'meta': 'Python · Pandas · Flask',
        'meta_note': '90,000+ track dataset',
        'tags': ['Mood based', 'Ranked picks', 'Learns'],
        'lead': 'A recommendation system built around how people actually choose music — by '
                'mood and language, not by chart position. It surfaces top matches from a large '
                'dataset, plays them directly on Spotify, and quietly sharpens future '
                'suggestions from the feedback it collects.',
        'features': [
            ('filter', 'Filtering and ranking', 'Matches across 90,000+ songs on genre, tempo and tags.'),
            ('heart', 'Mood and language driven', 'Tuned for personal fit rather than generic popularity.'),
            ('music', 'Spotify playback', 'Every recommended track plays through the Spotify API.'),
            ('spark', 'Random discovery', 'A play-random option pulls from the recommended set for exploration.'),
            ('check', 'Feedback loop', 'Likes and dislikes are logged and shape later recommendations.'),
        ],
        'workflow': [
            'The user picks a language, a mood and how many recommendations they want.',
            'The dataset is filtered down on language and mood.',
            'The top n songs are ranked by relevance and popularity, then listed.',
            'Each track plays on Spotify, or one is chosen at random.',
            'Likes and dislikes are logged to personalise the next run.',
        ],
        'tech': ['Python', 'Pandas', 'Flask', 'Spotify API'],
        'role': 'Built the full pipeline: user selection, dataset filtering, recommendation '
                'ranking, Spotify playback and feedback logging.',
        'links': [('repo', 'GitHub Repository', 'https://github.com/SahilSharma9024/Mood2Music', '')],
    },

    # ------------------------------------------------------------------- SRMS --
    {
        'id': 'srms',
        'brand': 'SRMS',
        'subtitle': 'Student result management',
        'category': 'Database',
        'status': 'live',
        'status_label': 'Academic project',
        'pad': 'pad-mint',
        'summary': 'Students, subjects, marks and results on a normalised schema, with '
                     'role-based access and every grade computed rather than typed.',
        'meta': 'Python · MySQL · Flask',
        'meta_note': 'Normalised relational schema',
        'tags': ['Marks entry', 'Auto results', 'Roles'],
        'lead': 'A database-driven replacement for manual result handling. The schema is '
                'normalised, access is scoped by role, and totals, percentage, grade and '
                'pass/fail are derived from the recorded marks rather than entered by hand.',
        'features': [
            ('db', 'Normalised schema', 'Relational design covering students, subjects and results.'),
            ('lock', 'Role-based auth', 'Separate Admin and Teacher paths; inactive users blocked, not deleted.'),
            ('list', 'Management modules', 'Student records, subject catalogue and marks entry, each role-scoped.'),
            ('chart', 'Automated results', 'Total, percentage, grade and pass/fail computed, never typed.'),
            ('shield', 'Data integrity', 'Validation against maximum marks and prevention of duplicate entries.'),
        ],
        'workflow': [
            'A user signs in; credentials, role and active status are checked before any dashboard loads.',
            'Admins manage the student roster and subject catalogue, including maximum and passing marks.',
            'Teachers enter marks per student per subject, validated against the subject maximum.',
            'The system computes totals, percentage, grade and pass/fail from the recorded marks.',
            'Final results are surfaced to whichever roles are authorised to see them.',
        ],
        'tech': ['Python', 'MySQL', 'Flask'],
        'role': 'Designed the database schema and built the authentication, management and '
                'result computation layers, keeping UI, logic and data cleanly separated.',
        'links': [('repo', 'GitHub Repository',
                   'https://github.com/SahilSharma9024/Student-Result-Management-System-SRMS-', '')],
    },
]
