"""Recapturas para el dossier v4 (no escribe en el repo). Uso: python3 capture_v4.py PUERTO"""
import asyncio, sys, pathlib
from playwright.async_api import async_playwright

OUT = pathlib.Path('/tmp/claude-0/dossier-v4/shots'); OUT.mkdir(exist_ok=True)
U = f'http://localhost:{sys.argv[1]}/index.html'


async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--lang=es-CL'], env={'LANG': 'es_CL.UTF-8', 'LANGUAGE': 'es_CL'})
        c = await b.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1.5, locale='es-CL', timezone_id='America/Santiago')
        p = await c.new_page(); await p.goto(U)
        await p.wait_for_function("!document.querySelector('.loader')", timeout=20000); await p.wait_for_timeout(2600)
        # Esmeralda 198: mazo sin pasar por encima (sin el distintivo «Arrastrar»)
        y = await p.evaluate("(()=>{const e=document.querySelector('.esm__grid');return e.getBoundingClientRect().top+scrollY})()")
        await p.evaluate('y=>scrollTo(0,y)', y); await p.wait_for_timeout(400)
        await p.evaluate('y=>scrollTo(0,y)', y + 1); await p.mouse.wheel(0, 1); await p.wait_for_timeout(2600)
        await p.mouse.move(2, 450); await p.wait_for_timeout(1200)
        await p.evaluate("()=>{const n=document.querySelector('[data-nav]');n&&n.classList.remove('is-hidden')}"); await p.wait_for_timeout(500)
        await p.screenshot(path=str(OUT / 'd-esm.jpg'), type='jpeg', quality=86)
        # Pedido con fecha escrita
        await p.evaluate("document.querySelector('#ramos').scrollIntoView()"); await p.wait_for_timeout(1500)
        await p.evaluate("document.querySelector('[data-product=\"Rosas Rojas\"] [data-add]').click();document.querySelector('[data-product=\"Ramos Silvestres\"] [data-add]').click()")
        await p.wait_for_timeout(600); await p.evaluate("document.querySelector('[data-cart-open]').click()"); await p.wait_for_timeout(1300)
        await p.evaluate("""()=>{const d=document.querySelector('.cart input[type=date], input[type=date]'); if(d){d.value='2026-10-14'; d.dispatchEvent(new Event('input',{bubbles:true})); d.dispatchEvent(new Event('change',{bubbles:true}));}}""")
        await p.mouse.move(2, 450); await p.wait_for_timeout(1500)
        await p.screenshot(path=str(OUT / 'd-cart.jpg'), type='jpeg', quality=86)
        await b.close()

asyncio.run(main())
