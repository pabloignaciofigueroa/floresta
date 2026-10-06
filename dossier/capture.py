"""Capturas del sitio para el dossier (computador 1440×900 @1.5, celular 390×844 @2.5)."""
import asyncio, sys, pathlib
from playwright.async_api import async_playwright
OUT = pathlib.Path(__file__).parent / 'shots'
U = 'http://localhost:8765/index.html'
# clave, selector, modo, valor
DESK = [('hero', '.hero', 'top', 0), ('cont', '.cont__top', 'top', 0), ('cinta', '.cinta', 'dy', -90),
        ('ramos', '#ramos', 'offset', .02), ('esm', '.esm__grid', 'top', 0), ('invierno', '.invierno', 'frac', .98),
        ('hist', '#historia', 'offset', .18), ('nati', '.hist__nati', 'center', 0), ('ocas', '.ocas__title', 'dy', -120),
        ('jardin', '#jardin', 'top', 0), ('alm', '.alm-wrap', 'dy', -110), ('visita', '.visita__main', 'center', 0),
        ('resenas', '.resenas', 'dy', -120), ('foot', '.foot', 'bottom', 0)]
MOB = [('hero', '.hero', 'top', 0), ('cont', '#manifiesto', 'top', 0), ('ramos', '.ramos__slider', 'dy', -120),
       ('esm', '.deck', 'dy', -160), ('hist', '.reels', 'dy', -120), ('ocas', '.panels', 'dy', -40),
       ('alm', '.alm-wrap', 'dy', -40), ('visita', '#visitanos', 'top', 0), ('foot', '.foot', 'bottom', 0)]
async def shoot(p, vh, prefix, lst, hover=None):
    for k, sel, mode, x in lst:
        y = await p.evaluate('''([sel,mode,x,vh])=>{const e=document.querySelector(sel);const top=e.getBoundingClientRect().top+scrollY,h=e.offsetHeight;
          if(mode==='top')return top; if(mode==='frac')return top+(h-vh)*x; if(mode==='offset')return top+h*x; if(mode==='dy')return top+x;
          if(mode==='bottom')return top+h-vh; return top+(h-vh)/2;}''', [sel, mode, x, vh])
        await p.evaluate('y=>scrollTo(0,y)', max(0, y)); await p.wait_for_timeout(400)
        await p.evaluate('y=>scrollTo(0,y)', max(0, y) + 1); await p.mouse.wheel(0, 1); await p.wait_for_timeout(2600)
        if hover and k in hover:
            box = await p.evaluate(f"(()=>{{const r=document.querySelector('{hover[k]}').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}})()")
            await p.mouse.move(*box); await p.wait_for_timeout(1200)
        await p.evaluate("()=>{const n=document.querySelector('[data-nav]');n&&n.classList.remove('is-hidden')}")
        await p.wait_for_timeout(500)
        await p.screenshot(path=str(OUT / f'{prefix}-{k}.jpg'), type='jpeg', quality=84)
        await p.mouse.move(2, 2)
async def main():
    only = sys.argv[1:]
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        c = await b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1.5, locale='es-CL')
        p = await c.new_page(); await p.goto(U); await p.wait_for_timeout(1050)
        await p.screenshot(path=str(OUT / 'd-loader.jpg'), type='jpeg', quality=84)
        await p.wait_for_function("!document.querySelector('.loader')", timeout=20000); await p.wait_for_timeout(2600)
        await shoot(p, 900, 'd', [s for s in DESK if not only or s[0] in only], hover={'esm': '.deck'})
        # menú y pedido
        await p.evaluate('scrollTo(0,0)'); await p.set_viewport_size({'width': 1000, 'height': 900}); await p.wait_for_timeout(900)
        await p.click('[data-menu-open]'); await p.wait_for_timeout(1500)
        await p.screenshot(path=str(OUT / 'd-menu.jpg'), type='jpeg', quality=84)
        await p.keyboard.press('Escape'); await p.wait_for_timeout(1000); await p.set_viewport_size({'width': 1440, 'height': 900})
        await p.evaluate("document.querySelector('#ramos').scrollIntoView()"); await p.wait_for_timeout(1500)
        await p.evaluate("document.querySelector('[data-product=\"Rosas Rojas\"] [data-add]').click();document.querySelector('[data-product=\"Ramos Silvestres\"] [data-add]').click()")
        await p.wait_for_timeout(600); await p.evaluate("document.querySelector('[data-cart-open]').click()"); await p.wait_for_timeout(1300)
        await p.screenshot(path=str(OUT / 'd-cart.jpg'), type='jpeg', quality=84)
        await c.close()
        m = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2.5, is_mobile=True, has_touch=True, locale='es-CL')
        q = await m.new_page(); await q.goto(U)
        await q.wait_for_function("!document.querySelector('.loader')", timeout=20000); await q.wait_for_timeout(2600)
        await shoot(q, 844, 'm', [s for s in MOB if not only or s[0] in only])
        await b.close()
asyncio.run(main())
