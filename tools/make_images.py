"""Generate site images from ../site-revamp/images. Re-runnable."""
from PIL import Image, ImageDraw, ImageFont
import os, shutil
SRC='/workspace/threetinybrushes/site-revamp/images'
OUT=os.path.join(os.path.dirname(__file__),'..','img')
kits=['unicorn-wishes-personalized-paintable-name-kit','dino-mite-personalized-paintable-name-kit',
      'donut-dreams-personalized-paintable-name-kit','big-bro-paint-kit','big-sis-paint-kit']
short={'unicorn-wishes-personalized-paintable-name-kit':'unicorn-wishes','dino-mite-personalized-paintable-name-kit':'dino-mite',
       'donut-dreams-personalized-paintable-name-kit':'donut-dreams','big-bro-paint-kit':'big-bro','big-sis-paint-kit':'big-sis'}
def save(im,base,w,q=80):
    h=round(im.height*w/im.width)
    r=im.resize((w,h),Image.LANCZOS) if w!=im.width else im
    r.save(f'{OUT}/{base}-{w}.webp','WEBP',quality=q,method=6)
    r.save(f'{OUT}/{base}-{w}.jpg','JPEG',quality=80 if w<1600 else 82,optimize=True,progressive=True)
for k in kits:
    im=Image.open(f'{SRC}/{k}.jpg').convert('RGB')
    # 1600 JPEG = the new spec file, copied verbatim
    shutil.copy(f'{SRC}/{k}.jpg',f'{OUT}/{short[k]}-1600.jpg')
    im.save(f'{OUT}/{short[k]}-1600.webp','WEBP',quality=78,method=6)
    for w in (400,600,800): save(im,short[k],w,78)
hero=Image.open(f'{SRC}/hero-kits-collage.jpg').convert('RGB')
for w in (560,800,1100): save(hero,'hero-kits',w,78)
# logos
lt=Image.open(f'{SRC}/logo-600-transparent.png').convert('RGBA')
for s in (64,128):
    r=lt.resize((s,s),Image.LANCZOS); r.save(f'{OUT}/logo-{s}.png',optimize=True); r.save(f'{OUT}/logo-{s}.webp','WEBP',quality=85,method=6)
lo=Image.open(f'{SRC}/logo-600.png').convert('RGBA')
for s in (96,):
    r=lo.resize((s,s),Image.LANCZOS); r.save(f'{OUT}/logo-solid-{s}.png',optimize=True); r.save(f'{OUT}/logo-solid-{s}.webp','WEBP',quality=85,method=6)
os.makedirs(f'{OUT}/..',exist_ok=True)
lo.resize((32,32),Image.LANCZOS).save(f'{OUT}/../favicon-32.png',optimize=True)
lo.convert('RGB').resize((180,180),Image.LANCZOS).save(f'{OUT}/../apple-touch-icon.png',optimize=True)
lo.resize((32,32),Image.LANCZOS).save(f'{OUT}/../favicon.ico',sizes=[(32,32)])
# OG 1200x630 from the hero collage
og=Image.new('RGB',(1200,630),'#FFE3EE')
c=hero.resize((round(1400*600/1310),600),Image.LANCZOS)
og.paste(c,(1200-c.width-10,15))
d=ImageDraw.Draw(og)
qs='/usr/share/fonts/truetype/sand-box/google/Quicksand/Quicksand-VariableFont_wght.ttf'
nu='/usr/share/fonts/truetype/sand-box/google/Nunito/Nunito-VariableFont_wght.ttf'
f1=ImageFont.truetype(qs,70); f1.set_variation_by_axes([700])
f2=ImageFont.truetype(nu,26); f2.set_variation_by_axes([800])
f3=ImageFont.truetype(qs,30); f3.set_variation_by_axes([700])
logo=lt.resize((96,96),Image.LANCZOS); og.paste(logo,(60,60),logo)
d.text((168,90),'Three Tiny Brushes',font=f3,fill='#3A3350')
d.text((60,215),'PERSONALIZED PAINT NAME KITS',font=f2,fill='#C2185B')
d.text((60,260),'Their name,',font=f1,fill='#3A3350')
d.text((60,340),'their colors',font=f1,fill='#FF6FA3')
d.text((60,470),'Pickup at Orange Otter Toys',font=f2,fill='#3A3350')
d.text((60,506),'North Augusta, SC',font=f2,fill='#3A3350')
og.save(f'{OUT}/og.jpg','JPEG',quality=85,optimize=True,progressive=True)
