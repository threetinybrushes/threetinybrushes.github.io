"""Writes index.html (cards + JSON-LD generated from one product list). Re-runnable; edit PRODUCTS to change prices."""
import json, os, html as H
SQ='https://threetinybrushes.square.site'
DOMAIN='https://threetinybrushes.com/'
PRODUCTS=[ # name, short, subtitle, full name on Square, price(s), path
 ('Unicorn Wishes','unicorn-wishes','Personalized name kit','Unicorn Wishes Personalized Paintable Name Kit',(18,20),'/product/unicorn-wishes-personalized-paintable-name-kit/DJL3EIU2E24Y5KIVT3AFHHFQ','Unicorn Wishes personalized paint-your-own name kit'),
 ('Dino-Mite','dino-mite','Personalized name kit','Dino-Mite Personalized Paintable Name Kit',(18,20),'/product/dino-mite-personalized-paintable-name-kit/X7LNKIWP7Z5QSPDV2MBJVYXO','Dino-Mite personalized paint-your-own name kit'),
 ('Donut Dreams','donut-dreams','Personalized name kit','Donut Dreams Personalized Paintable Name Kit',(18,20),'/product/donut-dreams-personalized-paintable-name-kit/XVZXHL3UPXNTKXDHEBRHSUZJ','Donut Dreams personalized paint-your-own name kit'),
 ('Big Bro','big-bro','Paint kit','Big Bro Paint Kit',(15,),'/product/big-bro-paint-kit/SIYX23676XSIWKKCX4ZDVVKI','Big Bro paint kit'),
 ('Big Sis','big-sis','Paint kit','Big Sis Paint Kit',(15,),'/product/big-sis-paint-kit/H5QH7S3RQCL5UPOWYXILWPQ4','Big Sis paint kit'),
]
IG='https://www.instagram.com/threetinybrushes'; FB='https://www.facebook.com/threetinybrushes'
EMAIL='threetinybrushes@gmail.com'
MAILTO='mailto:threetinybrushes@gmail.com?subject=Add%20me%20to%20the%20Three%20Tiny%20Brushes%20list'
MAIL_PACKS='mailto:threetinybrushes@gmail.com?subject=Party%20packs'
# Party packs section (#party-packs). Photos: img/party-*-{600,1000}.{webp,jpg} from `python3 tools/make_images.py party`.
# PARTY_SHOP_URL = the "Shop party packs" button. Swap in the Square product URL once the party pack listing exists.
PARTY_SHOP_URL='https://threetinybrushes.square.site/product/party-pack/VT7LMGTIQBLTZOM6BSILZJJO'
PARTY_PRICES=(('$8','each'),('$6','each for 5 or more'),('$5','each for 20 or more'))
PARTY_PROMO='Planning a birthday? Order 15+ party packs and we&rsquo;ll include a free Happy Birthday party pack.'
PARTY_PILL='15+ packs = free Happy Birthday pack'
# Happy Birthday pack: 8th card in the grid (photo/alt = PARTY_BDAY). Flat price, no 5+/20+ discounts; still free with 15+ party packs.
PARTY_BDAY_NAME='Happy Birthday'
PARTY_BDAY_PRICE='$10'
PARTY_BDAY_NOTE='Free with 15+ party packs'
PARTY_PACKS=[ # design name, image base, alt text
 ('Unicorn &amp; Rainbow','party-unicorn-rainbow','Unicorn &amp; Rainbow party pack: a paintable unicorn head and rainbow with three paint pots and a brush'),
 ('Dino Pals','party-dino-pals','Dino Pals party pack: a paintable T-rex and a small spiky dino with three paint pots and a brush'),
 ('Dino Friends','party-dino-friends','Dino Friends party pack: a paintable long-neck dinosaur and triceratops with three paint pots and a brush'),
 ('Smiley &amp; Star','party-smiley-star','Smiley &amp; Star party pack: a paintable smiley face and star with three paint pots and a brush'),
 ('Mermaid &amp; Sun','party-mermaid-sun','Mermaid &amp; Sun party pack: a paintable mermaid tail and sun with three paint pots and a brush'),
 ('Rainbow &amp; Smiley','party-rainbow-smiley','Rainbow &amp; Smiley party pack: a paintable rainbow and smiley face with three paint pots and a brush'),
 ('Princess &amp; Castle','party-princess-castle','Princess &amp; Castle party pack: a paintable princess, castle and crown with three paint pots and a brush'),
]
PARTY_BDAY=('party-happy-birthday','Happy Birthday party pack: a paintable cake, present, party hat and &ldquo;Happy Birthday&rdquo; plaque with three paint pots and a brush')
# Made-to-order / lead time (approved by Rachel 10/10). Short line in Shop + party packs; full text in the FAQ.
MADE_SHORT='Hand poured and made to order. Please allow at least 3 days before your order is ready.'
MADE_FULL='Every piece is hand poured and made to order, so please allow at least 3 days before your order is ready. Because each one is handmade from plaster, no two are exactly alike, and a tiny imperfection here or there is part of the charm.'
# FAQ: (question, answer as plain text). Rendered as <details> + FAQPage JSON-LD.
FAQ=[
 ('How long until my order is ready?',MADE_FULL),
 ('How do I personalize a name kit?','Type your child&rsquo;s name and pick the size when you order: 3&ndash;5 letters $18, 6&ndash;8 letters $20.'),
 ('Can I pick up locally?','Yes. Choose pickup or shipping at checkout. Pickup is at Orange Otter Toys, 507 Georgia Ave, Suite A, North Augusta, SC 29841, and we ship nationwide.'),
 ('Is the paint washable?','Yes. Every kit comes with high-quality, washable, non-toxic paint.'),
]
# REVIEWS: real customer quotes only (never invent). Each: {'quote': ..., 'name': ..., 'detail': ...} (detail optional, e.g. 'Unicorn Wishes kit').
# While empty, the Reviews section is not rendered at all (no placeholder, no schema).
REVIEWS=[]
# All name kits share the same Square setup: required name field + two size options ($18 / $20).
NAME_PROMPT='Please enter the name you would like to order'
NAME_SIZES='3–5 letters $18 · 6–8 letters $20'
DESC="Paint-your-own kits for kids: name kits personalized with your child's name, plus party packs for birthdays. Local pickup in North Augusta, SC or shipping nationwide."
# Dino photo: img/dino-mite-{400,600,800,1600}.{jpg,webp}, used by the Dino-Mite shop card and the pickup section.
# To swap it, replace those 8 files (or rerun tools/make_images.py with a new source) and rerun this script.
fmt=lambda p:'$%.2f'%p
def pic(short,alt,sizes,cls='',lazy=True,w=1600,h=1600,variants=(400,600,800,1600),src_w=800):
    ws=', '.join(f'img/{short}-{v}.webp {v}w' for v in variants)
    js=', '.join(f'img/{short}-{v}.jpg {v}w' for v in variants)
    la=' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    c=f' class="{cls}"' if cls else ''
    return (f'<picture><source type="image/webp" srcset="{ws}" sizes="{sizes}">'
            f'<img src="img/{short}-{src_w}.jpg" srcset="{js}" sizes="{sizes}" width="{w}" height="{h}" alt="{alt}"{c}{la}></picture>')
IG_SVG='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1.1.4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1.1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 2c-3.1 0-3.5 0-4.7.1-1 0-1.6.2-1.9.3-.5.2-.8.4-1.1.7-.3.3-.6.7-.7 1.1-.1.4-.3.9-.3 1.9-.1 1.2-.1 1.6-.1 4.7s0 3.5.1 4.7c0 1 .2 1.6.3 1.9.2.5.4.8.7 1.1.3.3.7.6 1.1.7.4.1.9.3 1.9.3 1.2.1 1.6.1 4.7.1s3.5 0 4.7-.1c1 0 1.6-.2 1.9-.3.5-.2.8-.4 1.1-.7.3-.3.6-.7.7-1.1.1-.4.3-.9.3-1.9.1-1.2.1-1.6.1-4.7s0-3.5-.1-4.7c0-1-.2-1.6-.3-1.9-.2-.5-.4-.8-.7-1.1-.3-.3-.7-.6-1.1-.7-.4-.1-.9-.3-1.9-.3-1.2-.1-1.6-.1-4.7-.1zm0 3.2a4.6 4.6 0 1 1 0 9.2 4.6 4.6 0 0 1 0-9.2zm0 7.6a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm5.8-7.8a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0z"/></svg>'
FB_SVG='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z"/></svg>'
MAIL_SVG='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm1 2.4V17h16V7.4l-8 5.3-8-5.3zM5.2 7l6.8 4.5L18.8 7H5.2z"/></svg>'
cards=[]
for name,short,sub,full,prices,path,alt in PRODUCTS:
    price=fmt(prices[0]) if len(prices)==1 else f'{fmt(prices[0])}–{fmt(prices[1])}'
    sr=f' to {fmt(prices[1])}' if len(prices)>1 else ''
    opts=f'\n   <p class="opts">Add their name · {NAME_SIZES}</p>' if sub=='Personalized name kit' else ''
    cards.append(f'''  <li class="card prod">
   {pic(short,alt,"(min-width:1160px) 196px, (min-width:1040px) 17vw, (min-width:600px) 30vw, 44vw")}
   <h3>{name}</h3><span class="type">{sub}</span>
   <p class="price"><span class="visually-hidden">Price: </span>{price}</p>{opts}
   <a class="btn btn-p btn-sm" href="{SQ}{path}" aria-label="Shop {name} on our Square shop">Shop</a>
  </li>''')
ld_products=[]
for name,short,sub,full,prices,path,alt in PRODUCTS:
    if len(prices)==1:
        offers={"@type":"Offer","price":"%.2f"%prices[0],"priceCurrency":"USD","url":SQ+path}
    else:
        offers={"@type":"AggregateOffer","lowPrice":"%.2f"%prices[0],"highPrice":"%.2f"%prices[1],"priceCurrency":"USD","offerCount":2,"url":SQ+path}
    ld_products.append({"@type":"Product","name":full,"image":f"{DOMAIN}img/{short}-1600.jpg","description":alt[0].upper()+alt[1:]+".","brand":{"@type":"Brand","name":"Three Tiny Brushes"},"url":SQ+path,"offers":offers})
import re
_txt=lambda x:H.unescape(re.sub('<[^>]+>','',x))
ld_faq={"@type":"FAQPage","@id":DOMAIN+"#faq","mainEntity":[{"@type":"Question","name":_txt(q),"acceptedAnswer":{"@type":"Answer","text":_txt(a)}} for q,a in FAQ]}
ld={"@context":"https://schema.org","@graph":[
 {"@type":"Store","@id":DOMAIN+"#store","name":"Three Tiny Brushes","url":DOMAIN,"logo":DOMAIN+"img/logo-128.png","image":DOMAIN+"img/og.jpg",
  "description":DESC,
  "areaServed":[{"@type":"City","name":"Augusta, GA"},{"@type":"City","name":"North Augusta, SC"},{"@type":"Country","name":"United States"}],
  "email":EMAIL,"sameAs":[IG,FB,SQ+"/"],
  "address":{"@type":"PostalAddress","name":"Orange Otter Toys (pickup location)","streetAddress":"507 Georgia Ave, Suite A","addressLocality":"North Augusta","addressRegion":"SC","postalCode":"29841","addressCountry":"US"},
  "makesOffer":[{"@type":"Offer","itemOffered":{"@id":DOMAIN+"#"+p[1]}} for p in PRODUCTS]}
]+[dict(ld_products[i],**{"@id":DOMAIN+"#"+PRODUCTS[i][1]}) for i in range(5)]+[ld_faq]}
ppic=lambda base,alt,sizes:pic(base,alt,sizes,w=600,h=800,variants=(600,1000),src_w=600)
PARTY_SIZES="(min-width:1160px) 245px, (min-width:760px) calc((100vw - 182px) / 4), calc((100vw - 86px) / 2)"
party_items='\n'.join(f'''  <li><figure>{ppic(base,alt,PARTY_SIZES)}<figcaption>{name}</figcaption></figure></li>''' for name,base,alt in PARTY_PACKS)
party_items+=f'''\n  <li class="bday"><figure><div class="pp-img">{ppic(PARTY_BDAY[0],PARTY_BDAY[1],PARTY_SIZES)}<span class="pp-price"><span class="visually-hidden">Price: </span>{PARTY_BDAY_PRICE}</span></div><figcaption>{PARTY_BDAY_NAME}<span class="pp-note">{PARTY_BDAY_NOTE}</span></figcaption></figure></li>'''
party_tiers=' <span class="dot" aria-hidden="true">·</span> '.join(f'<span class="tier"><b>{p}</b> {t}</span>' for p,t in PARTY_PRICES)
faq_items='\n'.join(f'  <details class="card faq-item"><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQ)
def _rev(r):
    d=f'<span class="rev-detail">{H.escape(r["detail"])}</span>' if r.get('detail') else ''
    return f'  <li class="card review"><blockquote><p>&ldquo;{H.escape(r["quote"])}&rdquo;</p></blockquote><p class="rev-name">{H.escape(r["name"])}{d}</p></li>'
REVIEWS_HTML=(f'''<section class="reviews" id="reviews" aria-labelledby="reviews-title"><div class="wrap">
 <p class="kicker">Reviews</p><h2 id="reviews-title">What parents are saying</h2>
 <ul class="rev-grid">
{chr(10).join(_rev(r) for r in REVIEWS)}
 </ul>
</div></section>

''' if REVIEWS else '')
FONTS='https://fonts.googleapis.com/css2?family=Nunito:wght@600;800;900&amp;family=Quicksand:wght@700&amp;display=swap'
html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paint-Your-Own Kits for Kids | Three Tiny Brushes</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{DOMAIN}">
<meta name="theme-color" content="#FFE3EE">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Three Tiny Brushes">
<meta property="og:title" content="Paint-Your-Own Kits for Kids | Three Tiny Brushes">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{DOMAIN}">
<meta property="og:image" content="{DOMAIN}img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Three Tiny Brushes personalized paint name kits: Reese, Henry and James kits">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Paint-Your-Own Kits for Kids | Three Tiny Brushes">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{DOMAIN}img/og.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{FONTS}">
<link rel="stylesheet" href="{FONTS}" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<link rel="stylesheet" href="css/styles.css">
<script src="js/monitoring.js" defer></script>
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False,separators=(',',':'))}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
 <a class="brand" href="#top" aria-label="Three Tiny Brushes, back to top"><picture><source type="image/webp" srcset="img/logo-64.webp 1x, img/logo-128.webp 2x"><img src="img/logo-128.png" width="58" height="58" alt=""></picture><span>Three Tiny Brushes</span></a>
 <nav class="nav" aria-label="Main">
  <a class="link" href="#how">How it works</a>
  <a class="link" href="#story">Our story</a>
  <a class="link" href="#pickup">Pickup</a>
  <a class="btn btn-p btn-sm" href="{SQ}/">Shop kits</a>
 </nav>
</div></header>

<main id="main">
<div class="hero" id="top">
 <div class="blob blob-a" aria-hidden="true"></div><div class="blob blob-b" aria-hidden="true"></div>
 <div class="wrap">
  <div>
   <p class="kicker">Paint-your-own kits for kids</p>
   <h1>Paint kits made<br><span class="accent">just for them</span></h1>
   <p class="sub">Kids' paint kits, including name kits made with your child's name. Local pickup in North Augusta or shipping.</p>
   <div class="row"><a class="btn btn-p" href="{SQ}/">Shop the kits</a><a class="btn btn-s" href="#pickup">Pickup &amp; shipping</a></div>
   <ul class="pills" aria-label="Highlights">
    <li class="pill" style="background:var(--pink-t)"><span aria-hidden="true">🎨</span> Personalized name kits</li>
    <li class="pill" style="background:var(--mint-t)"><span aria-hidden="true">🧼</span> Washable paint</li>
    <li class="pill" style="background:var(--mint-t)"><span aria-hidden="true">📍</span> Local pickup</li>
    <li class="pill" style="background:var(--lav-t)"><span aria-hidden="true">📦</span> Shipping</li>
   </ul>
  </div>
  <div class="hero-img">{pic("hero-kits","Three personalized paint name kits in white frames: Reese unicorn kit, Henry dino kit and James donut kit","(min-width:1160px) 480px, (min-width:900px) 40vw, (min-width:600px) 560px, calc(100vw - 40px)",lazy=False,w=1400,h=1310,variants=(560,800,1100))}</div>
 </div>
</div>

<section id="shop" aria-labelledby="shop-title"><div class="wrap">
 <p class="kicker">Shop kits</p><h2 id="shop-title">Pick a kit</h2>
 <p class="sub">Name kits are personalized with your child's name. Don't forget to enter the name (and pick a size) when you order. Big Bro and Big Sis kits are ready to go.</p>
 <p class="made-note"><span aria-hidden="true">🤍</span> {MADE_SHORT}</p>
 <ul class="grid5">
{chr(10).join(cards)}
 </ul>
 <div class="center"><a class="btn btn-s" href="{SQ}/">See all kits</a></div>
</div></section>

<section class="party" id="party-packs" aria-labelledby="party-title"><div class="wrap">
 <p class="kicker">For birthdays &amp; class parties</p><h2 id="party-title">Party packs</h2>
 <p class="sub">Paint-it-yourself packs for every kid at the party. Each pack has paintable figures, three washable, non-toxic paints and a brush. Ages 3+.</p>
 <ul class="party-grid" aria-label="Party pack designs">
{party_items}
 </ul>
 <div class="party-buy">
  <div class="card party-price">
   <h3>Pricing</h3>
   <p class="range-price"><span class="visually-hidden">Price range: </span>$5 to $10</p>
   <p class="tiers-label">Seven designs</p>
   <p class="tiers" aria-label="Party pack pricing for the seven designs">{party_tiers}</p>
   <p class="bday-price">Happy Birthday pack: <b>{PARTY_BDAY_PRICE}</b> (free with 15+ party packs)</p>
   <p class="made-note sm">{MADE_SHORT}</p>
   <div class="row"><a class="btn btn-p" href="{PARTY_SHOP_URL}">Shop party packs</a><a class="btn btn-s" href="{MAIL_PACKS}">Ask about party packs</a></div>
  </div>
  <div class="card party-promo">
   <p class="pill deal"><span aria-hidden="true">🎁</span> {PARTY_PILL}</p>
   <div class="promo-img">{ppic(PARTY_BDAY[0],PARTY_BDAY[1],"(min-width:760px) 180px, 110px")}</div>
   <div class="promo-text">
    <p class="offer">{PARTY_PROMO}</p>
    <p class="promo-note">Your free pack: a cake, present, party hat and &ldquo;Happy Birthday&rdquo; plaque to paint.</p>
   </div>
  </div>
 </div>
</div></section>

<section class="more" id="more" aria-labelledby="more-title"><div class="wrap">
 <p class="kicker">More to paint</p><h2 id="more-title">Not just name kits</h2>
 <p class="sub">Seasonal kits are on the way, and party packs are ready for your next celebration. Have something in mind? Just ask.</p>
 <ul class="steps">
  <li class="card step"><div class="ico" style="background:var(--pink-t)" aria-hidden="true">🍂</div><p class="num" style="color:var(--pink-text)">COMING SOON</p><h3>Seasonal kits</h3><p>Paint kits for holidays and the seasons. Sign up below to hear when they're ready.</p><a class="btn btn-s btn-sm" href="#loop">Get updates</a></li>
  <li class="card step party">
   <div class="ico" style="background:var(--pink-t)" aria-hidden="true">🎉</div><p class="num" style="color:var(--pink-text)">NEW</p><h3>Party packs</h3>
   <p>Seven paint-it-yourself party pack designs, plus a Happy Birthday pack. For birthdays and class parties, $5 to $10 each.</p>
   <a class="btn btn-s btn-sm" href="#party-packs">See party packs</a>
  </li>
 </ul>
</div></section>

<section class="how" id="how" aria-labelledby="how-title"><div class="wrap">
 <p class="kicker">How it works</p><h2 id="how-title">Three tiny steps</h2>
 <ol class="steps">
  <li class="card step"><div class="ico" style="background:var(--pink-t)" aria-hidden="true">🖌️</div><p class="num" style="color:var(--pink-text)">STEP 1</p><h3>Pick your kit</h3><p>A name kit (unicorn, dino or donuts), a Big Bro / Big Sis kit, or whatever's new in the shop.</p></li>
  <li class="card step"><div class="ico" style="background:var(--mint-t)" aria-hidden="true">✏️</div><p class="num" style="color:var(--mint-text)">STEP 2</p><h3>Add the details</h3><p>Name kit? Type your child's name and pick the size when you order. Other kits are ready to go.</p></li>
  <li class="card step"><div class="ico" style="background:var(--lav-t)" aria-hidden="true">📍</div><p class="num" style="color:var(--lav-text)">STEP 3</p><h3>Pickup or shipping</h3><p>Choose local pickup in North Augusta or shipping at checkout, then paint together.</p></li>
 </ol>
</div></section>


<section class="paint" id="paint" aria-labelledby="paint-title"><div class="wrap">
 <div class="card paint-note">
  <p class="kicker">About our paint</p>
  <h2 id="paint-title">Washable, non-toxic paint</h2>
  <p>We fill every kit with high-quality, washable, non-toxic paint so tiny artists can create freely and parents can enjoy the fun with less worry about cleanup. More colorful memories, less stress about the mess! 🎨</p>
 </div>
</div></section>

<section class="story" id="story" aria-labelledby="story-title"><div class="wrap story-in">
 <div class="story-logo"><picture><source type="image/webp" srcset="img/logo-240.webp 1x, img/logo-480.webp 2x"><img src="img/logo-240.png" srcset="img/logo-240.png 1x, img/logo-480.png 2x" width="240" height="240" alt="Three Tiny Brushes logo: three paintbrushes in pink, mint and lavender" loading="lazy" decoding="async"></picture></div>
 <div><p class="kicker">A family project</p><h2 id="story-title">Our story</h2>
 <p>Three Tiny Brushes began when our oldest daughter was just six years old. She came to me with a sweet idea: she wanted to start a craft business with her two little sisters. We&rsquo;ve always loved crafting together and making special things for the people we love, so dreaming up craft kits to share felt like a natural next step.</p>
 <p>Together, we designed our logo with three tiny brushes&mdash;one for each of our girls, in their favorite color. Every kit is created and packaged by hand and holds a little piece of our family&rsquo;s love of crafting, ready to bring joy to your tiny artist.</p></div>
</div></section>

<section id="siblings" aria-labelledby="sib-title"><div class="wrap split">
 <div class="polaroid-wrap">{pic("big-sis","Big Sis paint kit","(min-width:1160px) 460px, (min-width:760px) 40vw, calc(100vw - 40px)",cls="polaroid tilt-l")}</div>
 <div><p class="kicker">Sibling kits</p><h2 id="sib-title">For the new<br><span class="accent">big brother or big sister</span></h2>
 <p class="sub">Our Big Bro and Big Sis paint kits give older siblings something of their own to paint.</p>
 <div class="row"><a class="btn btn-p" href="{SQ}{PRODUCTS[4][5]}">Shop Big Sis</a><a class="btn btn-s" href="{SQ}{PRODUCTS[3][5]}">Shop Big Bro</a></div></div>
</div></section>

<section class="pickup" id="pickup" aria-labelledby="pickup-title"><div class="wrap split rev">
 <div class="polaroid-wrap">{pic("dino-mite","Dino-Mite personalized paint-your-own name kit","(min-width:1160px) 460px, (min-width:760px) 40vw, calc(100vw - 40px)",cls="polaroid tilt-r")}</div>
 <div><p class="kicker">Pickup &amp; shipping</p><h2 id="pickup-title">Pick up locally or get it shipped</h2>
 <p class="sub lead-local">We&rsquo;re a local Augusta / North Augusta shop &mdash; pick up at Orange Otter Toys, or we ship nationwide.</p>
 <p class="sub">Just choose pickup or shipping at checkout.</p>
 <address class="card addr"><strong><span aria-hidden="true">📍</span> Orange Otter Toys</strong>507 Georgia Ave, Suite A<br>North Augusta, SC 29841</address></div>
</div></section>

{REVIEWS_HTML}<section class="faq" id="faq" aria-labelledby="faq-title"><div class="wrap">
 <p class="kicker">Good to know</p><h2 id="faq-title">Questions, answered</h2>
 <div class="faq-list">
{faq_items}
 </div>
</div></section>

<section class="news" id="loop" aria-labelledby="loop-title"><div class="wrap">
 <p class="kicker">Stay in the loop</p><h2 id="loop-title">New kits and restocks, first</h2>
 <div class="row"><a class="btn btn-p" href="{MAILTO}">{MAIL_SVG.replace('<svg','<svg width="20" height="20" fill="currentColor"')} Sign up</a></div>
 <p class="sub">Or follow us:</p>
 <div class="follow">
  <a class="btn btn-s btn-sm" href="{IG}" rel="noopener">{IG_SVG} Instagram</a>
  <a class="btn btn-s btn-sm" href="{FB}" rel="noopener">{FB_SVG} Facebook</a>
 </div>
</div></section>
</main>

<footer class="site-footer"><div class="wrap">
 <a class="brand" href="#top"><picture><source type="image/webp" srcset="img/logo-solid-96.webp"><img src="img/logo-solid-96.png" width="48" height="48" alt="" loading="lazy"></picture><span>Three Tiny Brushes</span></a>
 <div class="foot-links">
  <a href="mailto:{EMAIL}">{MAIL_SVG} {EMAIL}</a>
  <a href="{IG}" rel="noopener">{IG_SVG} Instagram</a>
  <a href="{FB}" rel="noopener">{FB_SVG} Facebook</a>
 </div>
 <div class="foot-meta">
  <p class="foot-local"><span>Local to Augusta &amp; North Augusta</span> · <span>Shipping nationwide</span></p>
  <p class="small">© 2026 Three Tiny Brushes · Checkout by Square</p>
 </div>
</div></footer>
</body>
</html>
'''
open(os.path.join(os.path.dirname(__file__),'..','index.html'),'w').write(html)
print('ok',len(html))
