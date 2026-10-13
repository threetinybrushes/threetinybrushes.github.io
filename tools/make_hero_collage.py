# Builds the hero collage (Reese + Henry name kits, Big Bro kit, Unicorn & Rainbow + Happy Birthday party packs; overlapping layout, Oct 12 2026) -> site-revamp/images/hero-kits-collage.jpg; then resize to img/hero-kits-{560,800,1100}.
from PIL import Image,ImageDraw,ImageFilter
S='/workspace/threetinybrushes/site-revamp/images/';P='/workspace/threetinybrushes/incoming/2026-10-06-party-packs/'
old=Image.open(S+'hero-kits-collage.jpg').convert('RGB');bg=old.getpixel((10,10))
W,H=1400,1310;c=Image.new('RGBA',(W,H),bg+(255,))
def card(path,w,h,crop=None,border=22,r=44):
    im=Image.open(path).convert('RGB')
    if crop: im=im.crop(crop)
    iw,ih=w-2*border,h-2*border
    s=max(iw/im.width,ih/im.height);im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    l=(im.width-iw)//2;t=(im.height-ih)//2;im=im.crop((l,t,l+iw,t+ih))
    cd=Image.new('RGBA',(w,h),(0,0,0,0));m=Image.new('L',(w,h));ImageDraw.Draw(m).rounded_rectangle((0,0,w-1,h-1),r,fill=255)
    cd.paste((255,255,255,255),(0,0),m)
    m2=Image.new('L',(iw,ih));ImageDraw.Draw(m2).rounded_rectangle((0,0,iw-1,ih-1),r-14,fill=255)
    cd.paste(im,(border,border),m2);return cd
def place(cd,x,y,ang):
    cd=cd.rotate(ang,Image.BICUBIC,expand=True)
    m=Image.new('L',(W,H));m.paste(cd.split()[3].point(lambda v:int(v*0.28)),(x+6,y+24))
    m=m.filter(ImageFilter.GaussianBlur(22));sh=Image.new('RGBA',(W,H),(120,60,90,255));sh.putalpha(m)
    c.alpha_composite(sh);c.alpha_composite(cd,(x,y))
# name kits: crop to the package area (pkg ~145..895 x 225..785 of 1024 scale on 1600 -> *1.5625)
k=lambda a:(int(a[0]*1.5625),int(a[1]*1.5625),int(a[2]*1.5625),int(a[3]*1.5625))
place(card(S+'big-bro-paint-kit.jpg',600,525,k((70,150,970,880))),40,640,-3)
place(card(S+'unicorn-wishes-personalized-paintable-name-kit.jpg',640,560,k((70,150,970,880))),50,80,4)
place(card(S+'dino-mite-personalized-paintable-name-kit.jpg',630,550,k((70,150,970,880))),700,110,-4)
place(card(P+'happy-birthday-pack.png',390,515),985,650,6)
place(card(P+'party-pack-1.png',390,515),595,700,-4)
c.convert('RGB').save('hero-kits-collage.jpg',quality=92)
