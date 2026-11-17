#!/usr/bin/env python3
"""Build the inner pages of the SKS Developments site from index.html.

index.html is the source of truth for everything shared (head, header, mobile
menu, footer, phone tab bar, scripts) and for the sections that are reused on
inner pages. This script copies that shell into each page, swaps in the page's
own <main> content, and marks the page's link as current.

Run from the project root:   python3 tools/build_pages.py
Re-run it after editing the header, footer or a reused section in index.html.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda f: os.path.join(ROOT, f)

UNSPLASH = 'https://images.unsplash.com/{}?auto=format&fit=crop&w=2000&q=70'
FB = 'https://www.facebook.com/sksdevelopments'
TEL = 'tel:+16048254070'
EMAIL = 'shiv@sksdevelopments.com'


def read(f):
    with open(P(f), encoding='utf-8') as fh:
        return fh.read()


def write(f, s):
    with open(P(f), 'w', encoding='utf-8') as fh:
        fh.write(s)


# ---------------------------------------------------------------------------
# 1. Shared chrome in index.html: point header / menu / footer / tab bar links
#    at the new pages (safe to run more than once).
# ---------------------------------------------------------------------------
index = read('index.html')

swaps = [
    # header nav + contact
    ('<a href="#top">Home</a>', '<a href="index.html">Home</a>'),
    ('<a href="#about-us">About</a>\n        <a href="#process">Process</a>\n        <a href="#portfolio">Projects</a>\n        <a href="#services">Services</a>',
     '<a href="about.html">About</a>\n        <a href="process.html">Process</a>\n        <a href="projects.html">Projects</a>\n        <a href="services.html">Services</a>'),
    ('<a href="#contact" class="header__contact">Contact</a>', '<a href="contact.html" class="header__contact">Contact</a>'),
    # logos
    ('<a href="#top" class="logo"', '<a href="index.html" class="logo"'),
    ('<a href="#top" class="logo logo--light"', '<a href="index.html" class="logo logo--light"'),
    # mobile menu
    ('<a href="#about-us"><small>01</small>About</a>\n      <a href="#process"><small>02</small>Process</a>\n      <a href="#services"><small>03</small>Services</a>\n      <a href="#portfolio"><small>04</small>Projects</a>\n      <a href="#contact"><small>05</small>Contact</a>',
     '<a href="about.html"><small>01</small>About</a>\n      <a href="process.html"><small>02</small>Process</a>\n      <a href="services.html"><small>03</small>Services</a>\n      <a href="projects.html"><small>04</small>Projects</a>\n      <a href="contact.html"><small>05</small>Contact</a>\n      <a href="careers.html"><small>06</small>Careers</a>'),
    # footer
    ('<a href="#about-us">About</a><a href="#process">Process</a><a href="#portfolio">Projects</a><a href="#contact">Careers</a>',
     '<a href="about.html">About</a><a href="process.html">Process</a><a href="projects.html">Projects</a><a href="careers.html">Careers</a><a href="contact.html">Contact</a>'),
    ('<a href="#services">Development</a><a href="#services">Construction</a><a href="#services">Design</a><a href="#services">Management</a>',
     '<a href="services.html#development">Development</a><a href="services.html#construction">Construction</a><a href="services.html#design">Design</a><a href="services.html#management">Management</a>'),
    ('<a href="#">Privacy</a> · <a href="#">Terms</a> · <a href="#">Licences</a>',
     '<a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a> · <a href="licences.html">Licences</a>'),
    # phone tab bar
    ('<a href="#top" class="is-current">', '<a href="index.html" class="is-current">'),
    ('    <a href="#about-us">\n      <svg', '    <a href="about.html">\n      <svg'),
    ('    <a href="#portfolio">\n      <svg', '    <a href="projects.html">\n      <svg'),
    ('    <a href="#contact">\n      <svg', '    <a href="contact.html">\n      <svg'),
    # loader only on the home page
    ('<html lang="en">', '<html lang="en" data-loader>'),
    ("      if (!localStorage.getItem('sks-visited') && !matchMedia",
     "      if (document.documentElement.hasAttribute('data-loader') && !localStorage.getItem('sks-visited') && !matchMedia"),
]
for old, new in swaps:
    if old in index:
        index = index.replace(old, new)

# home page: mark Home as current in the header nav
index = index.replace('<a href="index.html">Home</a>', '<a href="index.html" class="is-current">Home</a>', 1) \
    if 'class="is-current">Home</a>' not in index else index
write('index.html', index)


# ---------------------------------------------------------------------------
# 2. Pull reusable sections out of index.html
# ---------------------------------------------------------------------------
MARKS = [
    ('split', '<!-- ============ ABOUT SKS'),
    ('wwd', '<!-- ============ WHAT WE DO'),
    ('pillars', '<!-- ============ INTRO / PILLARS'),
    ('process', '<!-- ============ PROCESS'),
    ('stats', '<!-- ============ STATS'),
    ('divisions', '<!-- ============ SERVICES'),
    ('compare', '<!-- ============ COMPARISON'),
    ('portfolio', '<!-- ============ PORTFOLIO'),
    ('cta', '<!-- ============ CTA BANNER'),
    ('contact', '<!-- ============ CONTACT'),
]
main_end = index.index('  </main>')
SEC = {}
for i, (key, mark) in enumerate(MARKS):
    a = index.index(mark)
    a = index.rindex('\n', 0, a) + 1
    b = index.index(MARKS[i + 1][1]) if i + 1 < len(MARKS) else main_end
    b = index.rindex('\n', 0, b) + 1
    SEC[key] = index[a:b]


def offpage(html):
    """Reused sections link to #contact on the home page; elsewhere go to the page."""
    return html.replace('href="#contact"', 'href="contact.html"')


# ---------------------------------------------------------------------------
# 3. Page hero
# ---------------------------------------------------------------------------
def page_hero(crumb, title, lead, img=None, pos='50% 50%'):
    media = (f'        <img class="page-hero__img" src="{img}" alt="" fetchpriority="high" style="object-position:{pos}" />\n'
             if img else '')
    plain = '' if img else ' page-hero--plain'
    return f'''    <!-- ============ PAGE HERO ============ -->
    <section class="page-hero{plain}" aria-label="{crumb}">
      <div class="page-hero__card">
{media}        <div class="page-hero__inner">
          <nav class="crumbs" aria-label="Breadcrumb">
            <a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{crumb}</span>
          </nav>
          <h1 class="page-hero__title">{title}</h1>
          <p class="page-hero__lead">{lead}</p>
        </div>
      </div>
    </section>

'''


ARROW = '<span class="btn__icon" aria-hidden="true"><svg viewBox="0 0 16 16"><path d="M3 8h10M9 4l4 4-4 4"/></svg></span>'


def btn(label, href='contact.html'):
    return f'<a href="{href}" class="btn"><span class="btn__label">{label}</span>{ARROW}</a>'


# ---------------------------------------------------------------------------
# 4. New page-only sections
# ---------------------------------------------------------------------------
def projects_section():
    cards = re.findall(r'(        <article class="card">.*?</article>)', SEC['portfolio'], re.S)
    types = ['residential', 'residential', 'commercial', 'commercial', 'residential', 'commercial']
    out = []
    for c, t in zip(cards, types):
        out.append(c.replace('<article class="card">', f'<article class="card reveal" data-type="{t}">').replace('\n        ', '\n          ').replace('        <article', '          <article', 1))
    grid = '\n'.join(out)
    return f'''    <!-- ============ PROJECTS GRID ============ -->
    <section class="section section--light" id="projects">
      <div class="frame">
        <header class="sec-head sec-head--split">
          <div>
            <p class="eyebrow">Portfolio</p>
            <h2 class="display reveal">Landmarks Delivered</h2>
          </div>
          <div class="chips" role="group" aria-label="Filter projects">
            <button type="button" class="chip" data-filter="all" aria-pressed="true">All</button>
            <button type="button" class="chip" data-filter="residential" aria-pressed="false">Residential</button>
            <button type="button" class="chip" data-filter="commercial" aria-pressed="false">Commercial</button>
          </div>
        </header>
        <div class="projects-grid">
{grid}
        </div>
      </div>
    </section>

'''


DISCIPLINES = [
    ('development', 'Development', 'From first site appraisal to approved plans, we find and shape the opportunity.',
     ['Site and feasibility studies', 'Planning, zoning and permits', 'Budget and programme from day one']),
    ('construction', 'Construction', 'Our own crews and trusted trades deliver to one schedule, on one contract.',
     ['Extensions, conversions and new builds', 'Structural work and steel installation', 'Weekly progress updates from site']),
    ('design', 'Design', 'Layouts, finishes and details shaped around how you actually live.',
     ['Architectural drawings and 3D layouts', 'Kitchen, bathroom and interior design', 'Energy Step Code–ready specifications']),
    ('management', 'Management', 'One point of contact from the first visit to the final handover.',
     ['Project management and scheduling', 'Inspections and building sign-off', 'Home warranty paperwork and aftercare']),
]


def disciplines_section():
    rows = []
    for n, (sid, title, text, items) in enumerate(DISCIPLINES, 1):
        lis = ''.join(f'<li>{i}</li>' for i in items)
        rows.append(f'''          <article class="disc-row reveal" id="{sid}">
            <span class="disc-row__num">0{n}</span>
            <h3>{title}</h3>
            <p>{text}</p>
            <ul class="ticks">{lis}</ul>
          </article>''')
    rows = '\n'.join(rows)
    return f'''    <!-- ============ DISCIPLINES ============ -->
    <section class="section section--light" id="disciplines">
      <div class="frame">
        <header class="sec-head">
          <p class="eyebrow">Disciplines</p>
          <h2 class="display reveal">Four Disciplines,<br />One Team</h2>
        </header>
        <div class="disc-grid">
{rows}
        </div>
      </div>
    </section>

'''


def next_steps_section():
    steps = [('01', 'Call or message', f'Ring <a href="{TEL}">604-825-4070</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a> with a few lines about your project.'),
             ('02', 'Free site visit', 'We come out, take a proper look and talk through what you want to achieve.'),
             ('03', 'Clear written quote', 'You get a no-obligation quote that sets out scope, timeline and cost.')]
    cells = '\n'.join(f'''          <div class="next reveal"><span class="next__num">{n}</span><h3>{t}</h3><p>{d}</p></div>''' for n, t, d in steps)
    return f'''    <!-- ============ WHAT HAPPENS NEXT ============ -->
    <section class="section section--light">
      <div class="frame frame--tight">
        <header class="sec-head">
          <p class="eyebrow">What Happens Next</p>
          <h2 class="display reveal">Three Simple Steps</h2>
        </header>
        <div class="next-grid">
{cells}
        </div>
      </div>
    </section>

'''


def careers_section():
    perks = [('Steady work', 'A full pipeline of homes, extensions and renovations across Surrey.'),
             ('Learn the trade', 'Work beside experienced builders who take the time to teach.'),
             ('Safety first', 'Proper equipment, clear site rules and no shortcuts.'),
             ('Pride in the work', 'We build homes people live in for decades, and it shows.')]
    roles = [('Site Supervisor', 'Runs day-to-day on site, trades and quality.'),
             ('Carpenter', 'Framing, finishing and bespoke joinery.'),
             ('General Labourer', 'Keeps the site moving, safe and tidy.'),
             ('Project Coordinator', 'Schedules, suppliers and client updates.')]
    perk_html = '\n'.join(f'          <div class="perk reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in perks)
    role_html = '\n'.join(
        f'''          <li class="role"><div><h3>{t}</h3><p>{d}</p></div>
            <a class="role__apply" href="mailto:{EMAIL}?subject=Application%20%E2%80%93%20{t.replace(' ', '%20')}">Apply <span aria-hidden="true">↗</span></a></li>'''
        for t, d in roles)
    return f'''    <!-- ============ CAREERS ============ -->
    <section class="section section--light" id="careers">
      <div class="frame">
        <header class="sec-head sec-head--split">
          <div>
            <p class="eyebrow">Join SKS</p>
            <h2 class="display reveal">Good People<br />Build Good Homes</h2>
          </div>
          <p class="sec-head__side-note reveal">We’re a hands-on team of builders, carpenters and project people working across Surrey and the Lower Mainland.</p>
        </header>
        <div class="perks">
{perk_html}
        </div>

        <div class="wwd-sub">
          <h3 class="wwd-sub__title reveal">Roles we regularly hire for</h3>
          <p class="sec-head__side-note reveal">Don’t see your role? Send your CV to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
        </div>
        <ul class="roles">
{role_html}
        </ul>
      </div>
    </section>

'''


def prose_section(body):
    return f'''    <!-- ============ CONTENT ============ -->
    <section class="section section--light">
      <div class="frame frame--tight">
        <article class="prose">
{body}
        </article>
      </div>
    </section>

'''


PRIVACY = f'''          <p class="prose__meta">Effective 18 November 2026</p>
          <p>SKS Developments (“SKS”, “we”, “us”) respects your privacy. This policy explains what personal information we collect through this website and when you contact us, how we use it, and the choices you have. We follow British Columbia’s <em>Personal Information Protection Act</em> (PIPA).</p>
          <h2>What we collect</h2>
          <ul>
            <li>Details you give us when you call, email or use the enquiry form — such as your name, email address, phone number and information about your property or project.</li>
            <li>Basic technical information our website host records automatically, such as your IP address, browser type and the pages you visit. We do not use advertising or tracking cookies.</li>
          </ul>
          <h2>How we use it</h2>
          <ul>
            <li>To reply to your enquiry, arrange a site visit and prepare a quote.</li>
            <li>To plan, deliver and manage your project if you become a client.</li>
            <li>To meet our legal, warranty, insurance and record-keeping obligations.</li>
          </ul>
          <h2>Sharing</h2>
          <p>We never sell your information. We share it only where needed to deliver your project — for example with trades, suppliers, designers, inspectors or warranty providers — and with service providers who help us run this website and our business, under appropriate confidentiality.</p>
          <h2>Storage and retention</h2>
          <p>We keep personal information only as long as we need it for the purposes above or as the law requires, and we protect it with reasonable security measures.</p>
          <h2>Your choices</h2>
          <p>You can ask to see or correct the personal information we hold about you, or withdraw consent for future contact, at any time.</p>
          <h2>Contact</h2>
          <p>Questions about privacy? Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="{TEL}">604-825-4070</a>.</p>'''

TERMS = f'''          <p class="prose__meta">Effective 18 November 2026</p>
          <p>These terms apply to your use of the SKS Developments website. By using the site you agree to them.</p>
          <h2>Information only</h2>
          <p>Content on this website is general information about our services. It is not a quote, an offer or professional advice. Every project is priced and agreed in a separate written quote and contract.</p>
          <h2>Images and content</h2>
          <p>Text, logos and images on this site belong to SKS Developments or are used with permission. Some photographs are illustrative and may not show our own projects. Please don’t copy or reuse site content without asking us first.</p>
          <h2>Partner logos</h2>
          <p>Partner and affiliation logos are the trademarks of their respective owners and are shown to indicate our working relationships.</p>
          <h2>Links to other sites</h2>
          <p>We link to third-party sites such as Facebook. We aren’t responsible for their content or privacy practices.</p>
          <h2>Liability</h2>
          <p>We work to keep this site accurate and available, but we can’t guarantee it is always complete, current or error-free. To the extent the law allows, we aren’t liable for losses arising from use of the website.</p>
          <h2>Governing law</h2>
          <p>These terms are governed by the laws of British Columbia and the federal laws of Canada that apply there.</p>
          <h2>Changes and contact</h2>
          <p>We may update these terms from time to time. Questions? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>'''

LOGOS = [('bc-housing', 'BC Housing'), ('1up-real-estate', '1UP Real Estate'), ('unimark-developments', 'Unimark Developments'),
         ('energy-step-code', 'Energy Step Code'), ('radiance-developments', 'Radiance Developments Ltd'), ('2-5-10-warranty', '2-5-10 Year Warranty')]
LOGO_GRID = ''.join(f'<li><img src="images/partners/{f}.png" alt="{n}" width="190" height="150" loading="lazy" /></li>' for f, n in LOGOS)

LICENCES = f'''          <p class="prose__meta">Licences, warranty and affiliations</p>
          <p>We build to the standards British Columbia expects of residential builders, and we’re happy to show you the paperwork before you commit.</p>
          <h2>Residential builder licensing</h2>
          <p>New homes in British Columbia must be built by a builder licensed through BC Housing’s Licensing &amp; Consumer Services. Our licence details are available on request.</p>
          <h2>Home warranty</h2>
          <p>New homes are covered by third-party home warranty insurance on the provincial 2-5-10 model: two years on materials and labour, five years on the building envelope and ten years on structure.</p>
          <h2>Energy Step Code</h2>
          <p>We design and build to the BC Energy Step Code level your municipality requires, so new homes are efficient, comfortable and ready for inspection.</p>
          <h2>Insurance</h2>
          <p>We carry liability insurance and WorkSafeBC coverage. Certificates are available on request.</p>
          <h2>Official partner affiliations</h2>
          <ul class="logo-grid">{LOGO_GRID}</ul>
          <h2>Ask for documents</h2>
          <p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="{TEL}">604-825-4070</a> and we’ll send licence, warranty and insurance details.</p>'''


# ---------------------------------------------------------------------------
# 5. Pages
# ---------------------------------------------------------------------------
PAGES = {
    'about.html': dict(
        title='About Us', tab='about.html', nav='about.html',
        desc='SKS Developments — seventeen years of building and renovation across Surrey, with one team from first survey to final key.',
        main=lambda: page_hero('About', 'About SKS Developments',
                               'Seventeen years of planning, designing and building homes across Surrey — one team from first survey to final key.',
                               'images/hero-building.webp', '62% 40%')
        + offpage(SEC['split']) + offpage(SEC['pillars']) + offpage(SEC['stats']) + offpage(SEC['cta'])),
    'process.html': dict(
        title='How We Build', tab=None, nav='process.html',
        desc='How SKS Developments plans, designs and builds — four clear stages and one accountable team.',
        main=lambda: page_hero('Process', 'How We Build',
                               'Four clear stages, one accountable team. Here’s what working with SKS looks like from start to finish.',
                               UNSPLASH.format('photo-1504307651254-35680f356dfd'), '50% 50%')
        + offpage(SEC['process']) + offpage(SEC['compare']) + offpage(SEC['cta'])),
    'projects.html': dict(
        title='Our Projects', tab='projects.html', nav='projects.html',
        desc='Homes, extensions and developments delivered by SKS Developments.',
        main=lambda: page_hero('Projects', 'Our Projects',
                               'Homes, renovations and developments delivered under one standard of craft.',
                               UNSPLASH.format('photo-1545324418-cc1a3fa10c00'), '50% 40%')
        + projects_section() + offpage(SEC['stats']) + offpage(SEC['cta'])),
    'services.html': dict(
        title='Our Services', tab=None, nav='services.html',
        desc='Extensions, loft and garage conversions, structural work, kitchens, renovations and carpentry across Surrey.',
        main=lambda: page_hero('Services', 'Our Services',
                               'Extensions, conversions, renovations and new builds — planned, designed and built by one team.',
                               UNSPLASH.format('photo-1600566753190-17f0baa2a6c3'), '50% 50%')
        + offpage(SEC['wwd']) + disciplines_section() + offpage(SEC['divisions']) + offpage(SEC['cta'])),
    'contact.html': dict(
        title='Contact Us', tab='contact.html', nav='contact.html',
        desc='Contact SKS Developments: 604-825-4070 · shiv@sksdevelopments.com. Book a free site visit.',
        main=lambda: page_hero('Contact', 'Contact Us',
                               'Tell us about your project. We’ll arrange a free site visit and send a clear, no-obligation quote.',
                               UNSPLASH.format('photo-1600585154340-be6161a56a0c'), '50% 60%')
        + SEC['contact'] + next_steps_section()),
    'careers.html': dict(
        title='Careers', tab=None, nav=None,
        desc='Careers at SKS Developments — site supervisors, carpenters, labourers and project coordinators in Surrey.',
        main=lambda: page_hero('Careers', 'Careers',
                               'Build your career with a team that takes pride in every home it hands over.',
                               UNSPLASH.format('photo-1541888946425-d81bb19240f5'), '50% 50%')
        + careers_section() + offpage(SEC['cta'])),
    'privacy.html': dict(
        title='Privacy Policy', tab=None, nav=None, desc='Privacy policy for SKS Developments.',
        main=lambda: page_hero('Privacy', 'Privacy Policy', 'How we collect, use and protect your personal information.')
        + prose_section(PRIVACY)),
    'terms.html': dict(
        title='Terms of Use', tab=None, nav=None, desc='Terms of use for the SKS Developments website.',
        main=lambda: page_hero('Terms', 'Terms of Use', 'The terms that apply when you use this website.')
        + prose_section(TERMS)),
    'licences.html': dict(
        title='Licences & Warranty', tab=None, nav=None,
        desc='SKS Developments licensing, home warranty, Energy Step Code and partner affiliations.',
        main=lambda: page_hero('Licences', 'Licences &amp; Warranty', 'Licensing, warranty and the partners we work with.')
        + prose_section(LICENCES)),
}

loader_a = index.index('  <!-- first-visit loader -->')
loader_b = index.index('  <!-- ============ HEADER')
main_a = index.index('  <main id="main">') + len('  <main id="main">\n')

for fname, cfg in PAGES.items():
    html = index[:loader_a] + index[loader_b:main_a] + '\n' + cfg['main']() + index[main_end:]
    html = html.replace('<html lang="en" data-loader>', '<html lang="en">')
    html = re.sub(r'<title>.*?</title>', f'<title>{cfg["title"]} | SKS Developments</title>', html, count=1)
    html = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{cfg["desc"]}" />', html, count=1)
    # current-page marks: header nav, tab bar
    html = html.replace('<a href="index.html" class="is-current">Home</a>', '<a href="index.html">Home</a>')
    if cfg['nav']:
        html = html.replace(f'<a href="{cfg["nav"]}">', f'<a href="{cfg["nav"]}" class="is-current" aria-current="page">', 1)
    html = html.replace('    <a href="index.html" class="is-current">\n', '    <a href="index.html">\n')
    if cfg['tab']:
        html = html.replace(f'    <a href="{cfg["tab"]}">\n      <svg', f'    <a href="{cfg["tab"]}" class="is-current" aria-current="page">\n      <svg')
    write(fname, html)
    print('built', fname)
