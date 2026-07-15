# -*- coding: utf-8 -*-
"""Bra Bangladesh — static site builder. content/*.html বডি থেকে সম্পূর্ণ পেজ বানায়।"""
import json, os, io

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
CONTENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'content')
DOMAIN = 'https://bra.bd'
SITE = 'ব্রা বাংলাদেশ'
AUTHOR = 'সাবরিনা হক'
AUTHOR_TITLE = 'ফ্যাশন ও ইনারওয়্যার বিষয়ক লেখক'

CATS = {
 'size-fitting': {'name':'সাইজ ও ফিটিং','emoji':'📏','desc':'সঠিক ব্রা সাইজ মাপা, ভুল ফিটিং চেনা এবং নিখুঁত ফিট পাওয়ার সম্পূর্ণ গাইড।'},
 'bra-types':    {'name':'ব্রার ধরন','emoji':'👚','desc':'টি-শার্ট, স্পোর্টস, পুশ-আপসহ সব ধরনের ব্রা — কোনটা কখন পরবেন।'},
 'care-cleaning':{'name':'যত্ন ও পরিচর্যা','emoji':'🧺','desc':'ব্রা ধোয়া, শুকানো, সংরক্ষণ এবং দীর্ঘদিন টেকসই রাখার নিয়ম।'},
 'health-comfort':{'name':'স্বাস্থ্য ও কমফোর্ট','emoji':'💗','desc':'প্রথম ব্রা থেকে মাতৃত্বকাল — স্বাস্থ্য ও আরামের সব প্রশ্নের উত্তর।'},
}

from datetime import date
with io.open(os.path.join(CONTENT,'manifest.json'),encoding='utf-8') as f:
    ALL_ARTICLES = json.load(f)  # cat, slug, title, desc, excerpt, minutes, alt, faq_schema, publishAt(optional)
TODAY = date.today().isoformat()
ARTICLES = [a for a in ALL_ARTICLES if a.get('publishAt', '') <= TODAY]
SCHEDULED = [a for a in ALL_ARTICLES if a.get('publishAt', '') > TODAY]

def by_cat(c): return [a for a in ARTICLES if a['cat']==c]
BN='০১২৩৪৫৬৭৮৯'
def bn(n): return ''.join(BN[int(d)] for d in str(n))
YEAR = bn(date.today().year)

# ---------- seeded comments: content/seed-comments.json থেকে (এডমিন এডিটরে এডিটযোগ্য) ----------
with io.open(os.path.join(CONTENT,'seed-comments.json'),encoding='utf-8') as f:
    SEED_COMMENTS = json.load(f)

AV_COLORS = ['#1A6B5A','#E07B2A','#8E44AD','#2471A3','#B03A5B','#5D6D2E']
def comments_html(slug):
    rows = SEED_COMMENTS.get(slug, [])
    n = len(rows)
    items = ''
    for i, c in enumerate(rows):
        col = AV_COLORS[i % len(AV_COLORS)]
        items += (f'<div class="cmt"><div class="cmt-head"><span class="cmt-avatar" style="background:{col}">{c["name"][0]}</span>'
                  f'<span class="cmt-name">{c["name"]}</span></div><p>{c["body"]}</p>')
        if c.get('reply'):
            items += (f'<div class="cmt-author"><div class="cmt-head"><span class="cmt-avatar cmt-avatar-author">{AUTHOR[0]}</span>'
                      f'<span class="cmt-name">{AUTHOR} <span class="cmt-badge">✓ লেখক</span></span></div><p>{c["reply"]}</p></div>')
        items += '</div>'
    return f'''<div class="comments-wrap"><h2 class="cmt-title">💬 পাঠকদের মন্তব্য ({bn(n)})</h2>
<div id="cmt-list">{items}</div>
<div class="cmt-form"><h3>মন্তব্য করুন</h3>
<input type="text" id="cmt-nm" placeholder="আপনার নাম">
<textarea id="cmt-bd" rows="3" placeholder="আপনার মন্তব্য লিখুন…"></textarea>
<button onclick="bbComment('{slug}')">মন্তব্য পাঠান</button>
<p class="cmt-note" id="cmt-msg">মন্তব্য যাচাইয়ের পর প্রকাশিত হয়।</p></div></div>
<script>function bbComment(s){{var n=document.getElementById('cmt-nm').value.trim(),b=document.getElementById('cmt-bd').value.trim(),m=document.getElementById('cmt-msg');
if(!n||!b){{m.textContent='নাম ও মন্তব্য দুটোই লিখুন।';return;}}
if(window.BB_SB){{BB_SB.insert('comments',{{slug:s,name:n,body:b}}).then(function(){{m.textContent='✓ ধন্যবাদ! আপনার মন্তব্য যাচাইয়ের পর প্রকাশিত হবে।';document.getElementById('cmt-nm').value='';document.getElementById('cmt-bd').value='';}}).catch(function(){{m.textContent='দুঃখিত, এই মুহূর্তে পাঠানো যাচ্ছে না — পরে আবার চেষ্টা করুন।';}});}}
else m.textContent='দুঃখিত, এই মুহূর্তে পাঠানো যাচ্ছে না।';}}
if(window.BB_SB){{BB_SB.get('comments?slug=eq.{slug}&approved=eq.true&order=created_at').then(function(rows){{if(!rows||!rows.length)return;var L=document.getElementById('cmt-list');rows.forEach(function(r){{var d=document.createElement('div');d.className='cmt';d.innerHTML='<div class="cmt-head"><span class="cmt-avatar" style="background:#2471A3"></span><span class="cmt-name"></span></div><p></p>';d.querySelector('.cmt-avatar').textContent=(r.name||'?').charAt(0);d.querySelector('.cmt-name').textContent=r.name;d.querySelector('p').textContent=r.body;L.appendChild(d);}});}}).catch(function(){{}});}}
</script>'''

GA_ID = 'G-TNYN5RX17H'
GA_SNIPPET = ('<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
"gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});"
"if(localStorage.getItem('bb_cookie_choice')==='all'){gtag('consent','update',{ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted',analytics_storage:'granted'});}"
f"gtag('js',new Date());gtag('config','{GA_ID}');</script>\n"
f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>')

GFONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;600;700&family=Noto+Serif+Bengali:wght@700&display=swap" rel="stylesheet">'

def head(title, desc, path, ogtype='website', schema='', ogimage=''):
    url = DOMAIN + path
    og = f'<meta property="og:image" content="{DOMAIN}{ogimage}">\n<meta name="twitter:image" content="{DOMAIN}{ogimage}">\n' if ogimage else ''
    return ('<!DOCTYPE html>\n<html lang="bn">\n<head>\n<meta charset="UTF-8">\n'
    f'{GA_SNIPPET}\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
    f'<meta name="author" content="{AUTHOR}">\n<meta name="theme-color" content="#8B2A5B">\n'
    f'<link rel="canonical" href="{url}">\n'
    '<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n'
    f'<link rel="alternate" type="application/rss+xml" title="{SITE}" href="/feed.xml">\n'
    f'<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n'
    f'<meta property="og:url" content="{url}">\n<meta property="og:type" content="{ogtype}">\n'
    f'<meta property="og:site_name" content="{SITE}">\n'
    f'<meta property="og:locale" content="bn_BD">\n{og}<meta name="twitter:card" content="summary_large_image">\n'
    f'<meta name="twitter:title" content="{title}">\n<meta name="twitter:description" content="{desc}">\n'
    f'{GFONTS}\n<link rel="stylesheet" href="/shared.css">\n{schema}\n</head>\n<body>\n')

def nav(active=''):
    links = ''.join(f'<a href="/{s}/"{" class=\"active\"" if s==active else ""}>{c["name"]}</a>' for s,c in CATS.items())
    return ('<header><div class="nav-inner"><a href="/" class="logo"><div class="logo-paw">🎀</div>' + SITE + '</a>'
    '<button class="hamburger" id="hamburger" aria-label="মেনু"><span></span><span></span><span></span></button>'
    f'<nav id="main-nav">{links}<a href="/calculator/"{" class=\"active\"" if active=="calculator" else ""}>🧮 সাইজ ক্যালকুলেটর</a><a href="/about/">আমাদের সম্পর্কে</a></nav></div></header>\n'
    '<div class="ad-slot" data-ad-slot="header"></div>\n')

def footer():
    cols = ''
    for s in ['size-fitting','bra-types']:
        cols += f'<div class="footer-col"><h4>{CATS[s]["name"]}</h4>' + ''.join(
            f'<a href="/{a["cat"]}/{a["slug"]}/">{a["title"]}</a>' for a in by_cat(s)) + '</div>'
    cols += ('<div class="footer-col"><h4>সাইট</h4><a href="/articles/">📚 সব আর্টিকেল</a><a href="/glossary/">📖 পরিভাষা শব্দকোষ</a><a href="/about/">আমাদের সম্পর্কে</a><a href="/contact/">যোগাযোগ</a>'
    '<a href="/privacy-policy/">প্রাইভেসি পলিসি</a><a href="/terms-of-service/">শর্তাবলী</a><a href="/disclaimer/">দাবিত্যাগ</a></div>')
    return ('<div class="ad-slot" data-ad-slot="footer"></div>\n<footer><div class="footer-inner"><div>'
    f'<div class="footer-logo"><div class="footer-logo-paw">🎀</div>{SITE}</div>'
    '<p class="footer-desc">বাংলা ভাষায় ব্রা ও ইনারওয়্যার বিষয়ক নির্ভরযোগ্য তথ্যের ঠিকানা। সাইজ, ফিটিং, যত্ন ও স্বাস্থ্য — সব প্রশ্নের সহজ উত্তর, নারীদের জন্য, বাংলায়।</p></div>'
    + cols + '</div><div class="footer-bottom">'
    f'<span>&copy; <span class="dynamic-year">{YEAR}</span> bra.bd — সর্বস্বত্ব সংরক্ষিত</span>'
    '<div class="footer-bottom-links"><a href="/privacy-policy/">প্রাইভেসি</a><a href="/terms-of-service/">শর্তাবলী</a>'
    '<a href="/disclaimer/">দাবিত্যাগ</a><a href="/contact/">যোগাযোগ</a><a href="/sitemap.xml">সাইটম্যাপ</a></div>'
    '</div></footer>\n<script src="/sb.js"></script>\n<script src="/shared.js"></script>\n<script src="/ads.js"></script>\n</body>\n</html>')

def write(path, html):
    p = os.path.join(ROOT, path.strip('/').replace('/', os.sep), 'index.html') if path!='/' else os.path.join(ROOT,'index.html')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p,'w',encoding='utf-8') as f: f.write(html)
    print('✓', path)

# ---------- article pages ----------
for a in ARTICLES:
    cat = CATS[a['cat']]
    path = f'/{a["cat"]}/{a["slug"]}/'
    body_file = os.path.join(CONTENT, a['slug']+'.html')
    with io.open(body_file,encoding='utf-8') as f: body = f.read()
    schema = ('<script type="application/ld+json">'+json.dumps({
      "@context":"https://schema.org","@type":"Article","headline":a['title'],"description":a['desc'],
      "inLanguage":"bn","author":{"@type":"Person","name":AUTHOR,"url":DOMAIN+"/about/"},
      "publisher":{"@type":"Organization","name":SITE,"url":DOMAIN+"/"},
      "datePublished":a.get('publishAt') or TODAY,"dateModified":a.get('updatedAt') or a.get('publishAt') or TODAY,
      "mainEntityOfPage":{"@type":"WebPage","@id":DOMAIN+path}},ensure_ascii=False)+'</script>')
    schema += '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"হোম","item":DOMAIN+"/"},
      {"@type":"ListItem","position":2,"name":cat['name'],"item":f"{DOMAIN}/{a['cat']}/"},
      {"@type":"ListItem","position":3,"name":a['title']}]},ensure_ascii=False)+'</script>'
    if a.get('faq_schema'):
        schema += '<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage",
          "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}} for q,ans in a['faq_schema']]},ensure_ascii=False)+'</script>'
    others = [x for x in ARTICLES if x['slug']!=a['slug']][:3]
    related = ''.join(f'<a href="/{x["cat"]}/{x["slug"]}/" class="related-card"><div class="related-card-cat">{CATS[x["cat"]]["name"]}</div><div class="related-card-title">{x["title"]}</div></a>' for x in others)
    html = (head(f'{a["title"]} — {SITE}', a['desc'], path, 'article', schema, f'/images/articles/{a["cat"]}/{a["slug"]}.jpg') + nav(a['cat']) +
    f'''<div class="page-wrap">
<nav class="breadcrumb"><a href="/">হোম</a><span class="breadcrumb-sep">›</span><a href="/{a['cat']}/">{cat['name']}</a><span class="breadcrumb-sep">›</span><span>{a['title']}</span></nav>
<div class="article-meta-top"><span class="category-tag">{cat['name']}</span><span class="reading-time">পড়তে সময় লাগবে ~{a['minutes']} মিনিট</span></div>
<h1>{a['title']}</h1>
<p class="article-intro">{a['excerpt']}</p>
<div class="author-row"><div class="author-avatar">👩</div><div><div class="author-name">{AUTHOR}</div><div class="author-title">{AUTHOR_TITLE} — সর্বশেষ আপডেট: <span class="dynamic-date"></span></div></div></div>
<div class="hero-img"><img src="/images/articles/{a['cat']}/{a['slug']}.jpg" alt="{a['alt']}" style="width:100%;height:100%;object-fit:cover" onerror="this.style.display='none'"></div>
{body}
{comments_html(a['slug'])}
<div class="related-section"><div class="related-title">সম্পর্কিত আর্টিকেল</div><div class="related-grid">{related}</div></div>
<p class="last-updated">সর্বশেষ আপডেট: <span class="dynamic-date"></span></p>
</div>''' + footer())
    write(path, html)

# ---------- category pages ----------
for s,c in CATS.items():
    cards = ''.join(f'''<a href="/{a['cat']}/{a['slug']}/" class="cat-img-card"><div class="cat-img-card-img"><img src="/images/articles/{a['cat']}/{a['slug']}.jpg" alt="{a['alt']}" loading="lazy" onerror="this.style.display='none'"></div><div class="cat-img-card-body"><div class="cat-img-card-meta"><span class="cat-img-card-tag">{c['name']}</span><span class="cat-img-card-time">{a['minutes']} মিনিট</span></div><div class="cat-img-card-title">{a['title']}</div><p class="cat-img-card-excerpt">{a['excerpt'][:120]}…</p></div></a>''' for a in by_cat(s))
    html = (head(f'{c["name"]} — {SITE}', c['desc'], f'/{s}/') + nav(s) +
    f'''<div class="cat-hero"><div class="cat-hero-inner"><p style="font-size:13px;letter-spacing:.08em;color:rgba(255,255,255,.6);margin-bottom:8px">{SITE}</p><h1>{c['name']}</h1><p>{c['desc']}</p></div></div>
<div class="cat-list-wrap"><div class="cat-img-grid">{cards}</div></div>''' + footer())
    write(f'/{s}/', html)

# ---------- homepage ----------
cat_cards = ''.join(f'''<a href="/{s}/" style="background:var(--white);border:1px solid var(--border);border-radius:var(--radius-lg);padding:28px 22px;text-decoration:none;display:block"><div style="width:52px;height:52px;border-radius:12px;background:var(--teal-lite);display:flex;align-items:center;justify-content:center;font-size:26px;margin-bottom:16px">{c['emoji']}</div><h3 style="font-family:var(--font-head);font-size:18px;color:var(--text-main);margin-bottom:8px">{c['name']}</h3><p style="font-size:13px;color:var(--text-mute);line-height:1.75;margin-bottom:12px">{c['desc']}</p><span style="font-size:12px;color:var(--teal);font-weight:600">{bn(len(by_cat(s)))}টি আর্টিকেল →</span></a>''' for s,c in CATS.items())
_feat_pick, _feat_seen_cats = [], set()
for a in sorted(ARTICLES, key=lambda x: x.get('publishAt', ''), reverse=True):
    if a['cat'] not in _feat_seen_cats or len(_feat_pick) >= len(CATS):
        _feat_pick.append(a); _feat_seen_cats.add(a['cat'])
    if len(_feat_pick) == 6: break
if len(_feat_pick) < 6:
    for a in sorted(ARTICLES, key=lambda x: x.get('publishAt', ''), reverse=True):
        if a not in _feat_pick:
            _feat_pick.append(a)
        if len(_feat_pick) == 6: break
feat = ''.join(f'''<a href="/{a['cat']}/{a['slug']}/" class="cat-img-card"><div class="cat-img-card-img"><img src="/images/articles/{a['cat']}/{a['slug']}.jpg" alt="{a['alt']}" loading="lazy" onerror="this.style.display='none'"></div><div class="cat-img-card-body"><div class="cat-img-card-meta"><span class="cat-img-card-tag">{CATS[a['cat']]['name']}</span><span class="cat-img-card-time">{a['minutes']} মিনিট</span></div><div class="cat-img-card-title">{a['title']}</div><p class="cat-img-card-excerpt">{a['excerpt'][:110]}…</p></div></a>''' for a in _feat_pick)
home_faq = [
 ('আমার সঠিক ব্রা সাইজ কীভাবে জানবো?','একটি মাপার ফিতা দিয়ে বাসায়ই ব্যান্ড ও বাস্ট মেপে সাইজ বের করা যায়। আমাদের সাইজ মাপার গাইডে ধাপে ধাপে পদ্ধতি দেওয়া আছে।'),
 ('কত দিন পর পর ব্রা বদলানো উচিত?','নিয়মিত ব্যবহারে সাধারণত ৬–১২ মাস পর ব্রার ইলাস্টিক দুর্বল হয়ে যায়। ফিটিং ঠিক না থাকলে আগেই বদলানো ভালো।'),
 ('ব্রা কি প্রতিদিন ধোয়া দরকার?','প্রতিদিন নয়; সাধারণত ২–৩ বার পরার পর ধুলেই যথেষ্ট, তবে ঘাম বেশি হলে আগে ধুতে হবে।'),
 ('রাতে ব্রা পরে ঘুমানো কি ক্ষতিকর?','আরামদায়ক না হলে পরার দরকার নেই। এতে ক্যান্সার হয় — এমন ধারণার কোনো বৈজ্ঞানিক ভিত্তি নেই, তবে ঢিলেঢালা পোশাকই রাতে আরামদায়ক।'),
 ('স্পোর্টস ব্রা কি সবসময় পরা যায়?','ব্যায়ামের সময় স্পোর্টস ব্রা জরুরি, তবে সারাদিন খুব টাইট কম্প্রেশন ব্রা পরলে অস্বস্তি হতে পারে। দৈনন্দিন ব্যবহারে হালকা সাপোর্টের ব্রা ভালো।'),
]
faq_html = ''.join(f'<div class="faq-item"><div class="faq-q">{q}<span class="faq-icon">+</span></div><div class="faq-a"><p>{ans}</p></div></div>' for q,ans in home_faq)
home_schema = ('<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"WebSite","name":SITE,"url":DOMAIN+"/","inLanguage":"bn","description":"বাংলা ভাষায় ব্রা সাইজ, ফিটিং, ধরন, যত্ন ও স্বাস্থ্য বিষয়ক সম্পূর্ণ গাইড।"},ensure_ascii=False)+'</script>'
 +'<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"Organization","name":SITE,"url":DOMAIN+"/","foundingDate":"2026"},ensure_ascii=False)+'</script>'
 +'<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}} for q,ans in home_faq]},ensure_ascii=False)+'</script>')
html = (head(f'{SITE} — ব্রা সাইজ, ফিটিং ও যত্নের সম্পূর্ণ বাংলা গাইড ({YEAR})',
 'বাংলা ভাষায় ব্রা বিষয়ক নির্ভরযোগ্য তথ্য — সঠিক সাইজ মাপা, ব্রার ধরন, যত্ন ও স্বাস্থ্য। বাংলাদেশি নারীদের জন্য সহজ, বিজ্ঞানসম্মত গাইড।','/',
 'website', home_schema) + nav() + f'''
<div class="cat-hero" style="padding:72px 24px"><div class="cat-hero-inner" style="max-width:720px">
<h1>সঠিক ব্রা, সঠিক ফিট —<br>সব প্রশ্নের উত্তর বাংলায়</h1>
<p>প্রতি ১০ জনে ৮ জন নারী ভুল সাইজের ব্রা পরেন। সাইজ মাপা থেকে শুরু করে যত্ন, ধরন ও স্বাস্থ্য — {SITE} আপনাকে দিচ্ছে লজ্জা নয়, তথ্যভিত্তিক সহজ গাইড।</p>
<div style="margin-top:24px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
<a href="/size-fitting/bra-size-measurement-guide/" style="background:var(--amber);color:white;padding:12px 26px;border-radius:8px;text-decoration:none;font-weight:600">সাইজ মাপা শুরু করুন</a>
<a href="/about/" style="background:rgba(255,255,255,.12);color:white;padding:12px 26px;border-radius:8px;text-decoration:none;font-weight:600;border:1px solid rgba(255,255,255,.3)">আমাদের সম্পর্কে</a>
</div></div></div>
<div style="background:var(--white);border-bottom:1px solid var(--border)"><div style="max-width:1100px;margin:0 auto;padding:20px 24px;display:flex;justify-content:space-around;flex-wrap:wrap;gap:16px;font-size:14px;color:var(--text-mute)">
<div><strong style="color:var(--teal);font-size:20px">{bn(len(ARTICLES))}+</strong> বিস্তারিত গাইড</div>
<div><strong style="color:var(--teal);font-size:20px">{bn(len(CATS))}টি</strong> বিষয়ভিত্তিক বিভাগ</div>
<div><strong style="color:var(--teal);font-size:20px">১০০%</strong> বাংলায়</div>
<div><strong style="color:var(--teal);font-size:20px" class="dynamic-year">{YEAR}</strong> হালনাগাদ তথ্য</div>
</div></div>
<section style="max-width:1100px;margin:0 auto;padding:64px 24px">
<div style="text-align:center;margin-bottom:36px"><h2 style="font-family:var(--font-head);font-size:28px;color:var(--text-main)">যা জানতে চান, সব এখানে</h2><p style="color:var(--text-mute)">চারটি বিভাগে সাজানো আমাদের টপিক্যাল গাইড</p></div>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px">{cat_cards}</div>
</section>
<section style="max-width:1100px;margin:0 auto;padding:0 24px 64px">
<div style="text-align:center;margin-bottom:36px"><h2 style="font-family:var(--font-head);font-size:28px;color:var(--text-main)">জনপ্রিয় আর্টিকেল</h2></div>
<div class="cat-img-grid">{feat}</div>
</section>
<section style="max-width:760px;margin:0 auto;padding:0 24px 64px">
<h2 style="font-family:var(--font-head);font-size:28px;color:var(--text-main);margin-bottom:8px;text-align:center">সাধারণ জিজ্ঞাসা</h2>
<p style="text-align:center;color:var(--text-mute);margin-bottom:36px">পাঠকরা সবচেয়ে বেশি যা জানতে চান</p>
{faq_html}
</section>
<div class="newsletter-section"><div class="newsletter-inner"><h2>নতুন আর্টিকেলের খবর পান</h2><p>সপ্তাহে একটি ইমেইল — সাইজ, যত্ন ও স্বাস্থ্য টিপস, সরাসরি আপনার ইনবক্সে।</p><form class="newsletter-form" onsubmit="event.preventDefault();this.innerHTML='<p style=color:white>ধন্যবাদ! আপনি সাবস্ক্রাইব করেছেন।</p>'"><input type="email" placeholder="আপনার ইমেইল" required><button type="submit">সাবস্ক্রাইব</button></form></div></div>
''' + footer())
write('/', html)

# ---------- static pages from content files ----------
for slug,title,desc in [
 ('calculator','ব্রা সাইজ ক্যালকুলেটর','মাত্র দুটি মাপ দিন — আন্ডারবাস্ট ও বাস্ট (ইঞ্চি বা সেন্টিমিটারে)। সাথে সাথে পাবেন আপনার ব্রা সাইজ এবং সিস্টার সাইজ। সম্পূর্ণ ফ্রি, বাংলায়।'),
 ('glossary','ব্রা পরিভাষা শব্দকোষ','ব্যান্ড, কাপ, গোর, আন্ডারওয়্যার, পুশ-আপ, ব্রালেট — ব্রা-জগতের সব প্রচলিত ইংরেজি টার্মের সহজ বাংলা ব্যাখ্যা এক পাতায়।'),
 ('about','আমাদের সম্পর্কে','ব্রা বাংলাদেশ কেন তৈরি হয়েছে, কারা লিখছেন এবং আমাদের সম্পাদকীয় মান সম্পর্কে জানুন।'),
 ('contact','যোগাযোগ','ব্রা বাংলাদেশ টিমের সাথে যোগাযোগ করুন — প্রশ্ন, পরামর্শ বা ভুল সংশোধনের জন্য।'),
 ('privacy-policy','প্রাইভেসি পলিসি','ব্রা বাংলাদেশ কীভাবে আপনার তথ্য সংগ্রহ ও ব্যবহার করে — কুকিজ, অ্যানালিটিক্স ও বিজ্ঞাপন নীতি।'),
 ('terms-of-service','ব্যবহারের শর্তাবলী','bra.bd ব্যবহারের নিয়ম ও শর্তাবলী।'),
 ('disclaimer','দাবিত্যাগ','ব্রা বাংলাদেশের কনটেন্ট শিক্ষামূলক; পেশাদার চিকিৎসা পরামর্শের বিকল্প নয়।')]:
    with io.open(os.path.join(CONTENT,'page-'+slug+'.html'),encoding='utf-8') as f: body=f.read()
    write(f'/{slug}/', head(f'{title} — {SITE}', desc, f'/{slug}/') + nav() + f'<div class="page-wrap"><h1>{title}</h1>{body}</div>' + footer())

# ---------- archive page: সব আর্টিকেল ----------
arch_secs = ''
for s,c in CATS.items():
    arts = by_cat(s)
    rows = ''.join(f'<li><a href="/{a["cat"]}/{a["slug"]}/">{a["title"]}</a><span class="arch-min">{bn(a["minutes"])} মিনিট</span></li>' for a in arts)
    arch_secs += f'''<section style="margin-bottom:40px"><h2 style="font-family:var(--font-head);font-size:22px;color:var(--teal-dark);margin-bottom:6px">{c['emoji']} {c['name']} <span style="font-size:14px;color:var(--text-mute);font-weight:400">({bn(len(arts))}টি)</span></h2>
<p style="font-size:14px;color:var(--text-mute);margin-bottom:14px">{c['desc']}</p>
<ul style="list-style:none;padding:0;display:grid;gap:8px">{rows}</ul></section>'''
arch_html = (head(f'সব আর্টিকেল — {SITE}', f'{SITE}-এর প্রকাশিত সব আর্টিকেল এক পাতায় — সাইজ ও ফিটিং, ব্রার ধরন, যত্ন এবং স্বাস্থ্য ও কমফোর্ট।', '/articles/') + nav() +
 f'''<style>.arch-list li{{background:var(--white);border:1px solid var(--border);border-radius:var(--radius);padding:12px 16px;display:flex;justify-content:space-between;align-items:center;gap:12px}}
.arch-list li a{{color:var(--text-main);text-decoration:none;font-weight:600;font-size:15px}}.arch-list li a:hover{{color:var(--teal)}}
.arch-min{{font-size:12px;color:var(--text-mute);white-space:nowrap}}</style>
<div class="page-wrap arch-list">
<nav class="breadcrumb"><a href="/">হোম</a><span class="breadcrumb-sep">›</span><span>সব আর্টিকেল</span></nav>
<h1>সব আর্টিকেল</h1>
<p style="color:var(--text-mute);margin-bottom:32px">এখন পর্যন্ত প্রকাশিত {bn(len(ARTICLES))}টি গাইড — বিভাগ অনুযায়ী সাজানো। নতুন আর্টিকেল প্রতিদিনই যুক্ত হচ্ছে।</p>
{arch_secs}</div>''' + footer())
write('/articles/', arch_html)

# ---------- sitemap & robots ----------
urls = [('/','weekly','1.0',TODAY)] + [(f'/{s}/','weekly','0.8',TODAY) for s in CATS] + \
 [(f'/{a["cat"]}/{a["slug"]}/','monthly','0.7',a.get('publishAt') or TODAY) for a in ARTICLES] + \
 [('/articles/','weekly','0.6',TODAY),('/glossary/','monthly','0.6',TODAY),('/calculator/','monthly','0.8',TODAY),('/about/','yearly','0.5',TODAY),('/contact/','yearly','0.4',TODAY),('/privacy-policy/','yearly','0.2',TODAY),('/terms-of-service/','yearly','0.2',TODAY),('/disclaimer/','yearly','0.2',TODAY)]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u,cf,pr,lm in urls: sm += f'  <url><loc>{DOMAIN}{u}</loc><lastmod>{lm}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>\n'
sm += '</urlset>\n'
with io.open(os.path.join(ROOT,'sitemap.xml'),'w',encoding='utf-8') as f: f.write(sm)
# ---------- 404 ----------
nf = (head('পেজটি পাওয়া যায়নি — bra.bd', 'দুঃখিত, এই ঠিকানায় কোনো পেজ নেই।', '/404')
 + nav()
 + '<main style="max-width:640px;margin:0 auto;padding:70px 20px;text-align:center">'
 '<div style="font-size:64px;margin-bottom:8px">🎀</div>'
 '<h1 style="font-family:var(--font-head);color:var(--teal-dark);font-size:32px;margin-bottom:12px">পেজটি পাওয়া যায়নি (৪০৪)</h1>'
 '<p style="color:var(--text-mute);margin-bottom:26px">লিংকটি ভুল হতে পারে, অথবা পেজটি সরিয়ে ফেলা হয়েছে। নিচের যেকোনো জায়গা থেকে আবার শুরু করুন:</p>'
 '<p><a class="btn" href="/">🏠 হোমপেজ</a> &nbsp; <a class="btn" style="background:var(--amber)" href="/articles/">📚 সব আর্টিকেল</a></p>'
 '</main>' + footer())
with io.open(os.path.join(ROOT,'404.html'),'w',encoding='utf-8') as f: f.write(nf)
print('✓ 404.html')

with io.open(os.path.join(ROOT,'robots.txt'),'w',encoding='utf-8') as f: f.write(f'User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {DOMAIN}/sitemap.xml\n')
# RSS feed (published articles, newest scheduled-date first)
def rss_date(a):
    d = a.get('publishAt') or '2026-07-10'
    return d
items = ''
for a in sorted(ARTICLES, key=rss_date, reverse=True)[:20]:
    u = f"{DOMAIN}/{a['cat']}/{a['slug']}/"
    items += (f'  <item><title>{a["title"]}</title><link>{u}</link><guid>{u}</guid>'
              f'<pubDate>{rss_date(a)}</pubDate><description>{a["desc"]}</description></item>\n')
rss = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel>\n'
 f'<title>{SITE}</title><link>{DOMAIN}/</link><language>bn</language>\n'
 '<description>বাংলা ভাষায় ব্রা সাইজ, ফিটিং, ধরন, যত্ন ও স্বাস্থ্য বিষয়ক গাইড</description>\n'
 + items + '</channel></rss>\n')
with io.open(os.path.join(ROOT,'feed.xml'),'w',encoding='utf-8') as f: f.write(rss)

# publish queue for admin panel
queue = [{'slug':a['slug'],'cat':a['cat'],'title':a['title'],'publishAt':a.get('publishAt',''),'status':'published'} for a in ARTICLES] + \
        [{'slug':a['slug'],'cat':a['cat'],'title':a['title'],'publishAt':a.get('publishAt',''),'status':'scheduled'} for a in SCHEDULED]
with io.open(os.path.join(ROOT,'admin','queue.json'),'w',encoding='utf-8') as f:
    json.dump(queue, f, ensure_ascii=False)
print('✓ sitemap.xml, robots.txt, queue.json —', len(ARTICLES), 'published,', len(SCHEDULED), 'scheduled')
print('DONE — total pages:', len(ARTICLES)+len(CATS)+6)
