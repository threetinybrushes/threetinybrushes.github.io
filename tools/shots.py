import sys
from playwright.sync_api import sync_playwright
url=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:8765/'
out=sys.argv[2] if len(sys.argv)>2 else 'shots'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for name,w,dpr,mob in [('desktop-1280',1280,1,False),('mobile-390',390,2,True),('mobile-360',360,2,True)]:
        pg=b.new_page(viewport={'width':w,'height':900},device_scale_factor=dpr,is_mobile=mob,has_touch=mob)
        pg.goto(url,wait_until='networkidle')
        # scroll through to trigger lazy images
        h=pg.evaluate('document.body.scrollHeight')
        for y in range(0,h,400): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(80)
        pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_load_state('networkidle'); pg.wait_for_timeout(500)
        ov=pg.evaluate('document.documentElement.scrollWidth>window.innerWidth')
        print(name,'horizontal overflow:',ov, 'h1 count:',pg.evaluate("document.querySelectorAll('h1').length"))
        pg.screenshot(path=f'{out}/{name}.png',full_page=True)
        pg.close()
    b.close()
