"""QA visual: recorre el sitio con Playwright, captura cada sección y mide saltos de layout (CLS).
uso: python3 tools/qa.py [ancho] [alto] [carpeta]   (servidor local en :8765)"""
import sys, json, os
from playwright.sync_api import sync_playwright
W = int(sys.argv[1]) if len(sys.argv) > 1 else 1536
H = int(sys.argv[2]) if len(sys.argv) > 2 else 864
OUT = sys.argv[3] if len(sys.argv) > 3 else f'/tmp/claude-0/qa_{W}'
os.makedirs(OUT, exist_ok=True)
SECS = ['.hero', '#manifiesto', '.cinta', '#ramos', '#esmeralda', '.invierno', '#historia', '#ocasiones', '#jardin', '#visitanos', '.resenas', '#debes-saber', '.foot']
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
    pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=1)
    errs = []
    pg.on('console', lambda m: errs.append(m.text) if m.type in ('error', 'warning') else None)
    pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)))
    pg.add_init_script("""window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries()){if(!e.hadRecentInput)window.__cls+=e.value}}).observe({type:'layout-shift',buffered:true});""")
    pg.goto('http://localhost:8765/index.html', wait_until='load')
    pg.wait_for_timeout(7000)
    pg.screenshot(path=f'{OUT}/00_portada.jpg', quality=70, type='jpeg')
    cls_load = pg.evaluate('window.__cls')
    for i, s in enumerate(SECS[1:], 1):
        y = pg.evaluate(f"(()=>{{const e=document.querySelector('{s}');return e?e.getBoundingClientRect().top+scrollY:0}})()")
        pg.evaluate(f'window.scrollTo(0,{y})'); pg.mouse.wheel(0, 1); pg.wait_for_timeout(1600)
        pg.screenshot(path=f'{OUT}/{i:02d}_{s.strip("#.")}.jpg', quality=70, type='jpeg')
    total = pg.evaluate('window.__cls')
    ow = pg.evaluate('document.documentElement.scrollWidth - innerWidth')
    print(json.dumps({'cls_carga': round(cls_load, 4), 'cls_total': round(total, 4), 'desborde_x': ow, 'errores': errs[:12]}, ensure_ascii=False, indent=1))
    b.close()
