"""PDF + control de desbordes + PNG por lámina."""
import asyncio, pathlib
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = await b.new_page(viewport={'width': 1248, 'height': 816})
        await pg.goto('file://' + str(D / 'floresta-dossier-diseno.html'), wait_until='load')
        await pg.evaluate('document.fonts.ready')
        over = await pg.evaluate('''[...document.querySelectorAll('.R,.L')].map((e,i)=>{const r=e.getBoundingClientRect();const bad=[];
          e.querySelectorAll('*').forEach(c=>{if(c.closest('.pf'))return;const q=c.getBoundingClientRect();
          if(q.height&&q.bottom>r.bottom-(e.classList.contains('R')?40:0)+1)bad.push(c.className||c.tagName)});
          return bad.length?Math.floor(i/2)+1+':'+bad.slice(0,3).join(','):null}).filter(Boolean)''')
        print('overflow', over)
        await pg.pdf(path=str(D / 'floresta-dossier-diseno.pdf'), width='13in', height='8.5in', print_background=True)
        for i, l in enumerate(await pg.query_selector_all('.lam')):
            await l.screenshot(path=str(D / f'pages/p-{i+1:02d}.png'))
        await b.close()
asyncio.run(main())
