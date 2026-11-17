"""Page-specific content for the inner pages (imported by build_pages.py).

Each inner page has its own sections here, so it doesn't repeat the home page.
Edit the text in this file, then run:  python3 tools/build_pages.py
"""

TEL = 'tel:+16048254070'
PHONE = '604-825-4070'
EMAIL = 'shiv@sksdevelopments.com'
FB = 'https://www.facebook.com/sksdevelopments'
ARROW = '<span class="btn__icon" aria-hidden="true"><svg viewBox="0 0 16 16"><path d="M3 8h10M9 4l4 4-4 4"/></svg></span>'


# ---------- small building blocks ----------
def section(eyebrow, title, body, side='', tone='light', sid=''):
    head_cls = 'sec-head sec-head--split' if side else 'sec-head'
    side_html = f'\n          <p class="sec-head__side-note reveal">{side}</p>' if side else ''
    sid_attr = f' id="{sid}"' if sid else ''
    frame = 'frame frame--dark' if tone == 'dark' else 'frame'
    return f'''    <section class="section section--{tone}"{sid_attr}>
      <div class="{frame}">
        <header class="{head_cls}">
          <div>
            <p class="eyebrow">{eyebrow}</p>
            <h2 class="display reveal">{title}</h2>
          </div>{side_html}
        </header>
{body}
      </div>
    </section>

'''


def cards(items, cols=4):
    """items: (title, text) — small white cards (2 per row on phones)."""
    html = '\n'.join(f'          <div class="perk reveal"><h3>{t}</h3><p>{d}</p></div>' for t, d in items)
    return f'        <div class="perks perks--{cols}">\n{html}\n        </div>'


def rows(items):
    """items: (num, title, text, [ticks]) — numbered rows with tick lists."""
    out = []
    for n, t, d, ticks in items:
        lis = ''.join(f'<li>{x}</li>' for x in ticks)
        out.append(f'''          <article class="disc-row reveal"><span class="disc-row__num">{n}</span><h3>{t}</h3><p>{d}</p><ul class="ticks">{lis}</ul></article>''')
    return '        <div class="disc-grid">\n' + '\n'.join(out) + '\n        </div>'


def faq(items):
    out = '\n'.join(f'''          <details class="faq__item reveal"><summary>{q}<span class="faq__plus" aria-hidden="true"></span></summary><p>{a}</p></details>''' for q, a in items)
    return f'        <div class="faq">\n{out}\n        </div>'


def story(paras, facts):
    p = ''.join(f'<p>{x}</p>' for x in paras)
    f = ''.join(f'<li><strong>{a}</strong><span>{b}</span></li>' for a, b in facts)
    return f'''        <div class="story">
          <div class="story__text reveal">{p}</div>
          <ul class="story__facts reveal">{f}</ul>
        </div>'''


def chips(words):
    return '        <ul class="tags reveal">' + ''.join(f'<li>{w}</li>' for w in words) + '</ul>'


def contact_cards():
    items = [
        ('Call', f'<a href="{TEL}">{PHONE}</a>', 'Talk to us directly about your project.'),
        ('Email', f'<a href="mailto:{EMAIL}">{EMAIL}</a>', 'Send photos, drawings or a few lines about what you need.'),
        ('Facebook', f'<a href="{FB}" target="_blank" rel="noopener">facebook.com/sksdevelopments</a>', 'See recent work and send us a message.'),
    ]
    html = '\n'.join(f'          <div class="info-card reveal"><span class="info-card__label">{l}</span><p class="info-card__value">{v}</p><p>{d}</p></div>' for l, v, d in items)
    return f'        <div class="info-cards">\n{html}\n        </div>'


# ---------- page sections ----------
def about_main():
    return (
        section('Our Story', 'Built in Surrey,<br />Built to Last',
                story([
                    'SKS Developments started seventeen years ago with a simple idea: homeowners deserve a builder who treats their home like their own. What began with small renovations and extensions has grown into a team that plans, designs and builds complete homes and developments.',
                    'We still work the same way we did on day one. One point of contact, honest pricing, tidy sites and work we’re proud to put our name on. Most of our new projects come from past clients and their neighbours, and that’s the measure we care about most.',
                ], [('17', 'Years building'), ('1', 'Point of contact per project'), ('2-5-10', 'Year warranty on new homes'), ('Free', 'Site visit and written quote')]))
        + section('What We Believe', 'The Way We Work',
                  cards([
                      ('Straight talk', 'Clear quotes, honest timelines and no surprises hidden in the small print.'),
                      ('Craft first', 'We would rather take longer on a detail than hand over something we’re not proud of.'),
                      ('Respect your home', 'Protected floors, clean sites and crews who treat your house like their own.'),
                      ('Built to code', 'Permits, inspections and BC Energy Step Code requirements handled properly.'),
                  ]), side='Four things you can expect on every SKS job, big or small.')
        + section('Who We Help', 'From One Room<br />to a Whole Block',
                  cards([
                      ('Homeowners', 'Extensions, conversions, kitchens and full renovations for the home you already love.'),
                      ('Families building new', 'Custom homes designed around how your family actually lives.'),
                      ('Property investors', 'Duplexes, suites and multiplex projects planned for long-term value.'),
                      ('Businesses', 'Offices and commercial spaces fitted out around how your team works.'),
                  ]), side='Every project gets the same team, the same standards and the same attention.')
        + section('Where We Work', 'Surrey &amp; the<br />Lower Mainland',
                  chips(['Surrey', 'South Surrey', 'White Rock', 'Langley', 'Delta', 'Burnaby', 'New Westminster', 'Coquitlam', 'Richmond'])
                  + f'\n        <p class="note reveal">Not on the list? Call <a href="{TEL}">{PHONE}</a> — we often travel for the right project.</p>',
                  side='Based in Surrey, working right across the region.')
    )


def process_main():
    return (
        section('Step by Step', 'What Happens,<br />and When',
                rows([
                    ('01', 'First call', 'Tell us what you want to change and roughly when. We’ll talk budget ranges honestly from the start.', ['Same-week call back', 'Rough budget guidance', 'No obligation']),
                    ('02', 'Free site visit', 'We visit, measure and look at structure, access and services so nothing is guessed later.', ['Measurements and photos', 'Structural and access check', 'Ideas and options']),
                    ('03', 'Design &amp; quote', 'Drawings, finishes and a written quote that lists exactly what’s included.', ['Drawings and layouts', 'Itemised written quote', 'Programme and milestones']),
                    ('04', 'Permits', 'We prepare and submit what your municipality needs and deal with any questions.', ['Building permit applications', 'Engineering where required', 'Energy Step Code compliance']),
                    ('05', 'Build', 'Our crew and trusted trades get to work on an agreed schedule, with regular updates.', ['One site lead', 'Weekly progress updates', 'Inspections booked for you']),
                    ('06', 'Handover', 'Final walkthrough, snag list closed, documents and warranty paperwork handed over.', ['Final walkthrough', 'Warranty documents', 'Aftercare contact']),
                ]), side='Six stages, one team, and you always know what’s next.')
        + section('Typical Timelines', 'How Long Things<br />Usually Take',
                  cards([
                      ('Kitchen fitting', 'Usually 3–6 weeks on site once materials are ready.'),
                      ('Loft or garage conversion', 'Usually 6–10 weeks, depending on structure and permits.'),
                      ('Home extension', 'Usually 3–5 months on site, plus design and permit time.'),
                      ('New custom home', 'Usually 10–16 months from permit to keys.'),
                  ]), side='Every home is different — your quote includes a programme for your project. Permit times vary by municipality.')
        + section('Questions', 'Process FAQ',
                  faq([
                      ('Do I need a permit for my project?', 'Most extensions, structural changes, conversions and new builds need a building permit. We check what your municipality requires during the site visit and handle the application for you.'),
                      ('Can we stay at home while you work?', 'Often yes, especially for extensions and kitchen fits. We plan the work to keep your home usable and tell you in advance about any days with no water or power.'),
                      ('How are payments scheduled?', 'Payments are tied to clear milestones set out in your contract, so you only pay as work is completed.'),
                      ('Who do I talk to during the build?', 'You get one site lead for day-to-day questions, plus direct access to us by phone or email.'),
                      ('What happens if something changes?', 'Changes are priced and agreed in writing before the work is done, so the budget never drifts quietly.'),
                  ]))
    )


def projects_main(grid_html):
    return (
        grid_html
        + section('What We Build', 'Types of Projects<br />We Take On',
                  rows([
                      ('01', 'Custom homes', 'New homes designed and built around your lot, your family and your budget.', ['Design and permits', 'Full construction', '2-5-10 home warranty']),
                      ('02', 'Duplexes &amp; multiplexes', 'More homes on one lot, planned to meet BC’s small-scale housing rules.', ['Feasibility and zoning check', 'Multi-unit design', 'Strata-ready handover']),
                      ('03', 'Suites &amp; laneway homes', 'Basement suites, coach houses and laneway homes for family or rental income.', ['Separate entrances and services', 'Fire and sound separation', 'Permit-ready drawings']),
                      ('04', 'Additions &amp; renovations', 'Extensions, conversions and whole-home renovations that work with what you have.', ['Structural changes', 'Kitchens and bathrooms', 'Finishing and carpentry']),
                  ]), side='From a single room to a full development — with the same team throughout.')
        + section('Your Project', 'Thinking About<br />Something Similar?',
                  f'''        <div class="cta-strip reveal">
          <p>Send us photos, drawings or just an address. We’ll come out for a free site visit and tell you honestly what’s possible.</p>
          <a href="contact.html" class="btn"><span class="btn__label">Book a site visit</span>{ARROW}</a>
        </div>''')
    )


SERVICES = [
    ('home-extensions', 'Home Extensions', 'Single and double storey extensions that add real space and value, designed to look like they were always there.', ['Rear, side and wrap-around extensions', 'Matching materials and rooflines', 'Structural design and permits'], 'Growing families who love their area'),
    ('loft-conversions', 'Loft Conversions', 'Turn unused attic space into a bedroom, office or studio with proper headroom, light and insulation.', ['Dormers and skylights', 'Stairs designed to fit', 'Insulation to current code'], 'Extra rooms without losing the garden'),
    ('garage-conversions', 'Garage Conversions', 'A warm, finished living space in the footprint you already have — often the quickest way to add a room.', ['Insulated floors and walls', 'Windows, heating and electrics', 'Seamless link to the house'], 'Home offices, gyms and guest rooms'),
    ('structural', 'Structural Wall Removal', 'Open up your layout safely, with engineered steel or beams and the permits to match.', ['Engineer’s calculations', 'Steel beam installation', 'Making good and finishing'], 'Open-plan kitchens and living areas'),
    ('kitchens', 'Kitchen Fitting', 'Complete kitchens planned, plumbed, wired and finished — one team instead of five trades.', ['Layout and design', 'Plumbing, electrics and appliances', 'Worktops, tiling and finishing'], 'Kitchens that are used every day'),
    ('renovations', 'Home Renovations', 'Whole-home updates that rethink layouts, comfort and energy use in one coordinated project.', ['Layout redesign', 'Rewiring, plumbing and heating', 'Flooring, drywall and decoration'], 'Older homes ready for the next chapter'),
    ('carpentry', 'Bespoke Carpentry', 'Made-to-measure joinery that gives a home its character.', ['Media walls and built-in storage', 'Staircases and railings', 'Panelling and trim'], 'The details that make a house yours'),
    ('new-homes', 'New Homes &amp; Development', 'Custom homes, duplexes and small developments from feasibility through to keys.', ['Lot and feasibility review', 'Design, permits and build', 'Warranty and handover'], 'Building new, or building more on one lot'),
]


def services_main(disciplines_html):
    rows_html = []
    for sid, title, text, ticks, good in SERVICES:
        lis = ''.join(f'<li>{t}</li>' for t in ticks)
        rows_html.append(f'''          <article class="svc-row reveal" id="{sid}">
            <h3>{title}</h3>
            <p>{text}</p>
            <ul class="ticks">{lis}</ul>
            <p class="svc-row__good"><span>Best for</span>{good}</p>
          </article>''')
    return (
        section('Service Guide', 'Every Service,<br />Explained',
                '        <div class="svc-rows">\n' + '\n'.join(rows_html) + '\n        </div>',
                side='What each service covers, and who it suits best.')
        + disciplines_html
        + section('Questions', 'Services FAQ',
                  faq([
                      ('Do you handle design as well as building?', 'Yes. We can produce drawings in-house or work with your architect or designer — either way, one team takes responsibility for the build.'),
                      ('Can you combine several services in one project?', 'Most of our projects do — an extension with a new kitchen, or a renovation with bespoke carpentry. One quote, one schedule, one team.'),
                      ('Do you do small jobs?', 'We take on everything from a single structural wall to a full new home. If it’s too small for us, we’ll tell you honestly and point you to someone good.'),
                      ('Are your quotes fixed?', 'Your written quote sets out exactly what’s included. If you ask for changes, they’re priced and agreed in writing before work starts.'),
                  ]))
    )


def contact_main(form_section):
    return (
        section('Reach Us', 'Talk to the Team',
                contact_cards(),
                side='We reply to every enquiry within one business day.')
        + form_section
        + section('Questions', 'Before You Get in Touch',
                  faq([
                      ('Is the site visit really free?', 'Yes. We come out, look at the property and talk through options with no charge and no obligation.'),
                      ('What should I send you?', 'Your address, a few photos and a rough idea of what you want. Drawings help if you have them, but they’re not needed.'),
                      ('How soon can you start?', 'It depends on design and permit time for your project. We’ll give you realistic dates in your quote.'),
                      ('Which areas do you cover?', 'Surrey and across the Lower Mainland. If you’re a little further out, call us — we often travel for the right project.'),
                  ]))
    )


def careers_extra():
    return (
        section('What We Look For', 'Skills Matter.<br />Attitude Matters More.',
                cards([
                    ('Takes pride', 'You care how the finished job looks, even the parts nobody sees.'),
                    ('Safe by habit', 'You follow site safety without being asked.'),
                    ('Team player', 'You help the next trade and keep the site tidy.'),
                    ('Keen to learn', 'Apprentices and career-changers are welcome to apply.'),
                ]))
        + section('How to Apply', 'Three Simple Steps',
                  rows([
                      ('01', 'Send your CV', f'Email <a href="mailto:{EMAIL}">{EMAIL}</a> with your CV and the role you’re interested in.', ['Tell us your trade', 'Recent projects or photos', 'Your availability']),
                      ('02', 'Chat with us', 'A short call or site meeting to get to know each other.', ['No formal panel', 'Meet the team', 'Ask anything']),
                      ('03', 'Start on site', 'We’ll walk you through our site rules, safety and the project you’re joining.', ['Site induction', 'Safety briefing', 'Paired with a lead']),
                  ]))
    )


# ---------- projects: before / after cards ----------
U = 'https://images.unsplash.com/{}?auto=format&fit=crop&w=700&h=600&q=65'
BEFORE_AFTER = [
    (['Extensions', 'Renovations'], 'A rear extension that opened up the ground floor',
     'A cramped back room became one bright kitchen, dining and living space with doors onto the garden.',
     'photo-1541888946425-d81bb19240f5', 'photo-1600047509807-ba8f99d2cdde'),
    (['Renovations', 'New homes'], 'A dated house rebuilt as a modern family home',
     'Stripped back to the frame, re-planned inside and finished with new cladding, glazing and landscaping.',
     'photo-1508450859948-4e04fabaa4ea', 'photo-1613977257363-707ba9348227'),
    (['Kitchens', 'Structural'], 'Walls out, a kitchen built for everyday family life',
     'A load-bearing wall replaced with steel to create an open kitchen with an island and plenty of storage.',
     'photo-1504307651254-35680f356dfd', 'photo-1556911220-bff31c812dba'),
    (['New homes', 'Development'], 'From an empty lot to a finished custom home',
     'Site preparation, foundations and a full build, handed over with warranty and aftercare in place.',
     'photo-1517089596392-fb9a9033e05b', 'photo-1580587771525-78b9dba3b914'),
]


def before_after_grid():
    out = []
    for tags, title, text, before, after in BEFORE_AFTER:
        t = ''.join(f'<li>{x}</li>' for x in tags)
        out.append(f'''          <article class="ba reveal">
            <div class="ba__pics">
              <figure><img src="{U.format(before)}" alt="Before: {title}" loading="lazy" /><figcaption>Before</figcaption></figure>
              <figure><img src="{U.format(after)}" alt="After: {title}" loading="lazy" /><figcaption class="is-after">After</figcaption></figure>
            </div>
            <div class="ba__body">
              <ul class="ba__tags">{t}</ul>
              <h3>{title}</h3>
              <p>{text}</p>
              <a href="contact.html" class="ba__link">Start a similar project <span aria-hidden="true">→</span></a>
            </div>
          </article>''')
    return section('Before &amp; After', 'Transformations',
                   '        <div class="ba-grid">\n' + '\n'.join(out) + '\n        </div>',
                   side='How homes looked when we arrived, and how we handed them back.', sid='projects')


# =====================================================================
# Richer About + Process (keep the original home sections, add designed
# extras in between). S = dict of reusable home sections from build_pages.
# =====================================================================
IMG = 'https://images.unsplash.com/{}?auto=format&fit=crop&w=1000&q=70'
ICONS = {
    'talk': '<path d="M21 15a2 2 0 0 1-2 2H8l-5 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 9h8M8 13h5"/>',
    'craft': '<path d="M14 4l6 6-9 9H5v-6z"/><path d="M12 6l6 6"/>',
    'home': '<path d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z"/>',
    'shield': '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    'pin': '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
}


def icon(name):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'


def story_band():
    facts = [('17', 'years building in Surrey'), ('1', 'point of contact, start to finish'), ('2-5-10', 'year warranty on new homes'), ('0', 'cost for your first site visit')]
    f = ''.join(f'<li><strong>{a}</strong><span>{b}</span></li>' for a, b in facts)
    return f'''    <section class="section section--dark story-band">
      <div class="frame frame--dark">
        <div class="story2">
          <figure class="story2__img reveal"><img src="images/hero-building.webp" alt="A terraced stone and glass residence at golden hour" loading="lazy" /><figcaption>Built to last, built in Surrey</figcaption></figure>
          <div class="story2__text">
            <p class="eyebrow eyebrow--mono">Our Story</p>
            <h2 class="display reveal">Seventeen Years,<br />One Standard</h2>
            <p class="story2__lead reveal">SKS started with a simple idea: homeowners deserve a builder who treats their home like their own.</p>
            <p class="reveal">What began with small renovations and extensions has grown into a team that plans, designs and builds complete homes and developments. We still work the way we did on day one — one point of contact, honest pricing, tidy sites and work we’re proud to put our name on.</p>
            <ul class="facts2 reveal">{f}</ul>
          </div>
        </div>
      </div>
    </section>

'''


def values_grid():
    vals = [('talk', 'Straight talk', 'Clear quotes, honest timelines and no surprises in the small print.'),
            ('craft', 'Craft first', 'We’d rather take longer on a detail than hand over something we’re not proud of.'),
            ('home', 'Respect your home', 'Protected floors, clean sites and crews who treat your house like their own.'),
            ('shield', 'Built to code', 'Permits, inspections and BC Energy Step Code handled properly, every time.')]
    cards_html = '\n'.join(f'''          <article class="vcard reveal"><span class="vcard__icon">{icon(i)}</span><span class="vcard__num">0{n}</span><h3>{t}</h3><p>{d}</p></article>'''
                           for n, (i, t, d) in enumerate(vals, 1))
    return section('What We Believe', 'The Way<br />We Work', f'        <div class="vgrid">\n{cards_html}\n        </div>',
                   side='Four promises you can hold us to on every SKS job, big or small.')


def who_we_help():
    items = [('photo-1600596542815-ffad4c1539a9', 'Homeowners', 'Extensions, conversions and renovations for the home you already love.'),
             ('photo-1613977257363-707ba9348227', 'Families building new', 'Custom homes designed around how your family lives.'),
             ('photo-1574362848149-11496d93a7c7', 'Property investors', 'Duplexes, suites and multiplexes planned for long-term value.'),
             ('photo-1497366216548-37526070297c', 'Businesses', 'Offices and commercial spaces fitted out around your team.')]
    html = '\n'.join(f'''          <article class="pcard reveal"><img src="{IMG.format(p)}" alt="" loading="lazy" /><div class="pcard__body"><h3>{t}</h3><p>{d}</p></div></article>''' for p, t, d in items)
    return section('Who We Help', 'From One Room<br />to a Whole Block', f'        <div class="pgrid">\n{html}\n        </div>',
                   side='Every client gets the same team, the same standards and the same attention.')


def areas_band():
    areas = ['Surrey', 'South Surrey', 'White Rock', 'Langley', 'Delta', 'Burnaby', 'New Westminster', 'Coquitlam', 'Richmond']
    chips_html = ''.join(f'<li>{icon("pin")}{a}</li>' for a in areas)
    return f'''    <section class="section section--dark areas-band">
      <div class="frame frame--dark">
        <div class="areas2">
          <div>
            <p class="eyebrow eyebrow--mono">Where We Work</p>
            <h2 class="display reveal">Surrey &amp; the<br />Lower Mainland</h2>
            <p class="areas2__lead reveal">Based in Surrey and working right across the region. Not on the list? Call <a href="{TEL}">{PHONE}</a> — we often travel for the right project.</p>
          </div>
          <ul class="areas2__chips reveal">{chips_html}</ul>
        </div>
      </div>
    </section>

'''


def about_page(S, off):
    return (off(S['split']) + story_band() + off(S['pillars']) + values_grid()
            + who_we_help() + off(S['stats']) + areas_band() + off(S['cta']))


def timeline():
    steps = [('First call', 'Tell us what you want to change and roughly when. We talk budget ranges honestly from the start.', ['Same-week call back', 'Rough budget guidance']),
             ('Free site visit', 'We measure and look at structure, access and services so nothing is guessed later.', ['Measurements &amp; photos', 'Options and ideas']),
             ('Design &amp; quote', 'Drawings, finishes and a written quote that lists exactly what’s included.', ['Itemised quote', 'Programme &amp; milestones']),
             ('Permits', 'We prepare and submit what your municipality needs and answer any questions.', ['Permit applications', 'Engineering if required']),
             ('Build', 'Our crew and trusted trades work to an agreed schedule with regular updates.', ['One site lead', 'Weekly updates']),
             ('Handover', 'Final walkthrough, snag list closed, documents and warranty handed over.', ['Warranty documents', 'Aftercare contact'])]
    items = []
    for n, (t, d, tags) in enumerate(steps, 1):
        tg = ''.join(f'<li>{x}</li>' for x in tags)
        items.append(f'''          <li class="tl__item reveal"><span class="tl__dot">0{n}</span><div class="tl__body"><h3>{t}</h3><p>{d}</p><ul class="tl__tags">{tg}</ul></div></li>''')
    return section('Step by Step', 'What Happens,<br />and When', '        <ol class="tl">\n' + '\n'.join(items) + '\n        </ol>',
                   side='Six stages, one team — and you always know what’s next.')


def durations():
    jobs = [('Kitchen fitting', '3–6 weeks', 6), ('Loft or garage conversion', '6–10 weeks', 10), ('Home extension', '3–5 months', 22), ('New custom home', '10–16 months', 69)]
    mx = 69
    rows_html = '\n'.join(f'''          <li class="dur__row reveal" style="--w:{max(w / mx * 100, 9):.0f}%"><span class="dur__name">{n}</span><span class="dur__bar"><span></span></span><span class="dur__time">{t}</span></li>''' for n, t, w in jobs)
    return section('Typical Timelines', 'How Long Things<br />Usually Take',
                   f'        <ul class="dur">\n{rows_html}\n        </ul>\n        <p class="note reveal">Time on site once permits and materials are ready. Your quote includes a programme for your project; permit times vary by municipality.</p>',
                   side='A rough guide so you can plan around the work.')


PROCESS_FAQ = [
    ('Do I need a permit for my project?', 'Most extensions, structural changes, conversions and new builds need a building permit. We check what your municipality requires during the site visit and handle the application for you.'),
    ('Can we stay at home while you work?', 'Often yes, especially for extensions and kitchen fits. We plan the work to keep your home usable and warn you in advance about any days without water or power.'),
    ('How are payments scheduled?', 'Payments are tied to clear milestones in your contract, so you only pay as work is completed.'),
    ('Who do I talk to during the build?', 'You get one site lead for day-to-day questions, plus direct access to us by phone or email.'),
    ('What happens if something changes?', 'Changes are priced and agreed in writing before the work is done, so the budget never drifts quietly.'),
]


def process_page(S, off):
    return (off(S['process']) + timeline() + durations() + off(S['compare'])
            + section('Questions', 'Process FAQ', faq(PROCESS_FAQ)) + off(S['cta']))
