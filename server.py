#!/usr/bin/env python3
"""Live+Nat · tienda PWA. Sin dependencias: python3 server.py  ->  http://localhost:8000
Variables opcionales: PORT, ADMIN_KEY (para ver pedidos en /api/pedidos?clave=...)"""
import json, os, sqlite3, mimetypes
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.abspath(__file__))
PUB, DB = os.path.join(ROOT, 'public'), os.path.join(ROOT, 'tienda.db')
ADMIN, PORT = os.environ.get('ADMIN_KEY', ''), int(os.environ.get('PORT', 8000))
J, C = 'Jarabes y suspensiones', 'Colágenos y alimentos'
R = lambda a, b, c, d: {'Frasco': a, 'Porción': b, 'Porciones por envase': c, 'Registro INVIMA': d}

# PRECIOS DE EJEMPLO (COP): el catálogo no trae precios. Edítalos aquí o directamente en tienda.db.
# (slug, nombre, categoría, descripción, imagen, detalle, [(código, etiqueta, precio)])
SEED = [
 ('tattum', 'Tattum', J, 'Suspensión sin azúcar añadido, apta para diabéticos. Sabor menta.', 'tattum.webp',
  {'Frasco': '360 ml', 'Porción': '15 ml', 'Sabor': 'Menta', 'Registro INVIMA': 'RSA-0031421-2024'}, [('2014', '360 ml', 42000)]),
 ('clorophill', 'Clorophill', J, 'Suspensión Live+Nat sabor menta.', 'clorophill.webp',
  {'Frasco': '500 ml', 'Porción': '30 ml (2 cdas)', 'Porciones por envase': '16 aprox.', 'Sabor': 'Menta', 'Registro INVIMA': 'RSA-0028474-2023'}, [('2011', '500 ml', 48000)]),
 ('calbidenhs', 'Calbidenhs', J, 'Fórmula de cúrcuma y ruibarbo, sabor menta. Disponible en kit.', 'calbidenhs.webp',
  {'Porción': '15 ml', 'Sabor': 'Menta', 'Registro INVIMA': 'RSA-0031421-2024'},
  [('2021', '360 ml', 38000), ('2033', '180 ml', 24000), ('2034', 'Kit 360 ml + 180 ml', 58000)]),
 ('boldo-ruibarbo-alcachofa', 'Boldo + Ruibarbo + Alcachofa', J, 'Combinación de boldo, ruibarbo y alcachofa.', 'boldo.webp',
  R('360 ml', '10 ml', '36', 'RSA-0002675-2020'), [('2037', '360 ml', 36000)]),
 ('hierbamix', 'Hierbamix', J, 'Suspensión Live+Nat de 360 ml.', 'hierbamix.webp',
  R('360 ml', '30 ml (2 cdas)', '12', 'RSA-0024402-2023'), [('2107', '360 ml', 36000)]),
 ('oregano', 'Orégano', J, 'Producto nuevo. Suspensión de orégano de 360 ml.', 'oregano.webp',
  R('360 ml', '30 ml (2 cdas)', '12', 'RSA-0031421-2024'), [('2192', '360 ml', 34000)]),
 ('zarmix', 'Zarmix', J, 'Suspensión Live+Nat de 360 ml.', 'zarmix.webp',
  R('360 ml', '30 ml (2 cdas)', '12', 'RSA-0031421-2024'), [('2057', '360 ml', 36000)]),
 ('dolmit', 'Dolmit', J, 'Maracuyá, cúrcuma y colágeno hidrolizado.', 'dolmit.webp',
  R('360 ml', '30 ml (2 cdas)', '12 servicios', 'RSA-0024402-2023'), [('2106', '360 ml', 44000)]),
 ('colageno-hidrolizado-jarabe', 'Colágeno hidrolizado+', J, 'Colágeno hidrolizado en suspensión líquida.', 'colageno-jarabe.webp',
  R('500 ml', '30 ml (2 cdas)', '16 aprox.', 'RSA-0024402-2023'), [('2013', '500 ml', 52000)]),
 ('live-bron-propoleo', 'Live Bron con propóleo', J, 'Preparación con propóleo en frasco de 250 ml.', 'livebron.webp',
  {'Frasco': '250 ml', 'Porciones por envase': '17 aprox.', 'Registro INVIMA': 'RSA-0033298-2024'}, [('2148', '250 ml', 32000)]),
 ('collagen-marin', 'Collagen Marin + Citrato de magnesio', C, 'Colágeno hidrolizado con citrato de magnesio, endulzado con stevia. Sabor vainilla.', 'collagen-marin.webp',
  {'Sabor': 'Vainilla', 'Porciones 700 g': '23 aprox.', 'Porciones 250 g': '8 aprox.', 'Registro INVIMA': 'RSA-0724-2026'},
  [('2117', '700 g', 89000), ('2120', '250 g · bolsa doypack', 39000)]),
 ('colageno-biotina-uva', 'Colágeno + Biotina + Uva liofilizada', C, 'Sin soya, sin maltodextrina y sin endulzante. Sabor fresa.', 'biotina.webp',
  {'Sabor': 'Fresa', 'Porciones 700 g': '23 aprox.', 'Porciones 250 g': '8 aprox.', 'Registro INVIMA': 'RSA-0025607-2023'},
  [('2122', '700 g', 89000), ('2126', '250 g · bolsa doypack', 39000)]),
 ('junior-live', 'Junior Live', C, 'Sin azúcares añadidos y sin edulcorantes artificiales. Sabor cereza.', 'junior.webp',
  {'Presentación': '700 g', 'Sabor': 'Cereza', 'Porciones': '23 aprox.', 'Registro INVIMA': 'RSA-0021928-2022'}, [('2143', '700 g', 69000)]),
 ('live-flx-zero', 'Live Flx Zero', C, 'Colágeno hidrolizado y citrato de magnesio. Sin azúcares añadidos ni edulcorantes artificiales. Sabor vainilla.', 'flx.webp',
  {'Sabor': 'Vainilla', 'Porciones 700 g': '23 aprox.', 'Porciones 250 g': '8 aprox.', 'Registro INVIMA': 'RSA-0021928-2022'},
  [('2144', '700 g', 95000), ('2150', '250 g · bolsa doypack', 42000)]),
]

S, G, F = 'Suplementos dietarios y alimentos', 'Geles corporales', 'Serum facial'
cap = lambda frasco, reg: {'Frasco por': frasco, 'Registro INVIMA': reg}
gel = lambda reg: {'Frasco gel por': '220 ml', 'Registro INVIMA': reg}
sr = lambda t, reg: {'Tratamiento': t, 'Gotero por': '30 ml', 'Registro INVIMA': reg}
SEED += [
 ('omega-3', 'Omega 3', S, 'Suplemento dietario en cápsulas blandas.', 'omega3.webp', cap('90 cáps. blandas', 'SD2019-0004443'), [('2035', '90 cáps. blandas', 45000)]),
 ('omega-3-6-9', 'Omega 3-6-9', S, 'Suplemento dietario en cápsulas blandas.', 'omega369.webp', cap('90 cáps. blandas', 'SD2021-0004618'), [('2036', '90 cáps. blandas', 48000)]),
 ('colageno-biotina-capsulas', 'Colágeno 200 mg + Biotina 900 mcg', S, 'Suplemento dietario en cápsulas blandas.', 'colageno-caps.webp', cap('60 cáps. blandas', 'SD2020-0004523'), [('2073', '60 cáps. blandas', 46000)]),
 ('complejo-b-zinc', 'Complejo B + Zinc + Vitamina D3', S, 'Suplemento dietario en cápsulas blandas.', 'complejob.webp', cap('60 cáps. blandas', 'SD2019-0004384'), [('2074', '60 cáps. blandas', 42000)]),
 ('vitamina-e-1000', 'Vitamina E 1000 U.I. + Selenio (25 mcg)', S, 'Suplemento dietario en cápsulas blandas.', 'vite1000.webp', cap('60 cáps. blandas', 'SD2014-0003099'), [('2104', '60 cáps. blandas', 40000)]),
 ('calcio-d3', 'Calcio + Vitamina D3', S, 'Suplemento dietario en cápsulas blandas.', 'calcio.webp', cap('60 cáps. blandas', 'SD2013-0003063'), [('2103', '60 cáps. blandas', 38000)]),
 ('biotina-900', 'Biotina 900 mcg', S, 'Suplemento dietario en cápsulas blandas.', 'biotina900.webp', cap('60 cáps. blandas', 'SD2013-0002993'), [('2118', '60 cáps. blandas', 39000)]),
 ('vitamina-e-400', 'Vitamina E 400 U.I. + Selenio (70 mcg)', S, 'Suplemento dietario en cápsulas blandas.', 'vite400.webp', cap('60 cáps. blandas', 'SD2016-0003799'), [('2119', '60 cáps. blandas', 37000)]),
 ('fenogreco-aguaje', 'Fenogreco Aguaje', S, 'Suplemento en tabletas.', 'fenogreco.webp', cap('90 tabletas', 'RSA-0030271-2024'), [('2176', '90 tabletas', 42000)]),
 ('qb-forte', 'QB Forte', S, 'Suplemento en cápsulas.', 'qbforte.webp', cap('90 cápsulas', 'NSA-1789-2025'), [('2177', '90 cápsulas', 44000)]),
 ('oregano-capsulas', 'Orégano en cápsulas', S, 'Orégano en cápsulas blandas.', 'oregano-caps.webp', cap('90 cáps. blandas', 'NSA-1895-2025'), [('2178', '90 cáps. blandas', 36000)]),
 ('gel-castano-de-indias', 'Gel Castaño de Indias', G, 'Gel corporal Live+Nat de 220 ml.', 'gel-castano.webp', gel('NSOC75893-16CO'), [('2022', '220 ml', 28000)]),
 ('gel-calendula-arnica', 'Gel Caléndula + Árnica', G, 'Gel corporal Live+Nat de 220 ml.', 'gel-calendula.webp', gel('NSOC75893-16CO'), [('2025', '220 ml', 28000)]),
 ('gel-caliente-reductor', 'Gel Caliente Reductor', G, 'Gel corporal de efecto caliente, 220 ml.', 'gel-caliente.webp', gel('NSOC98011-19CO'), [('2038', '220 ml', 30000)]),
 ('gel-frio', 'Gel Frío', G, 'Gel corporal de efecto frío, 220 ml.', 'gel-frio.webp', gel('NSOC98033-19CO'), [('2039', '220 ml', 28000)]),
 ('gel-cannabis', 'Gel Cannabis', G, 'Gel corporal Live+Nat de 220 ml.', 'gel-cannabis.webp', gel('NSOC75893-16CO'), [('2082', '220 ml', 32000)]),
 ('livetdol-gel', 'Livetdol Gel', G, 'Gel corporal Live+Nat de 220 ml.', 'livetdol.webp', gel('NSOC 20618-23CO'), [('2115', '220 ml', 30000)]),
 ('serum-antioxidante', 'Live+Skin Antioxidante', F, 'Serum facial antioxidante con vitamina C y caléndula.', 'serum-antioxidante.webp', sr('Antioxidante', 'NSOC05750-21CO'), [('2135', '30 ml', 46000)]),
 ('serum-antiacne', 'Live+Skin Antiacné', F, 'Serum facial antiacné con niacinamida y sangre de drago.', 'serum-antiacne.webp', sr('Antiacné', 'NSOC05750-21CO'), [('2136', '30 ml', 46000)]),
 ('serum-hidratante', 'Live+Skin Hidratante', F, 'Serum facial hidratante con ácido hialurónico y manzanilla.', 'serum-hidratante.webp', sr('Hidratante', 'NSOC05750-21CO'), [('2137', '30 ml', 46000)]),
]
NEWCOL = {'omega-3': '#b0171f', 'omega-3-6-9': '#b0171f', 'colageno-biotina-capsulas': '#7a2a91', 'complejo-b-zinc': '#d4145a',
 'vitamina-e-1000': '#d99a00', 'calcio-d3': '#d4145a', 'biotina-900': '#e87d00', 'vitamina-e-400': '#d99a00', 'fenogreco-aguaje': '#1b5e5a',
 'qb-forte': '#3a7d2c', 'oregano-capsulas': '#7a9a4a', 'gel-castano-de-indias': '#c8620a', 'gel-calendula-arnica': '#d99a00',
 'gel-caliente-reductor': '#d01f26', 'gel-frio': '#1e6fb8', 'gel-cannabis': '#2e8b3e', 'livetdol-gel': '#1fa58f',
 'serum-antioxidante': '#b8921a', 'serum-antiacne': '#a8238f', 'serum-hidratante': '#1f86c8'}

COLORS = {'zarmix': '#d62828', 'dolmit': '#6a2c91', 'colageno-hidrolizado-jarabe': '#6a2c91', 'live-bron-propoleo': '#e8820c',
          'collagen-marin': '#6a2c91', 'colageno-biotina-uva': '#e0127a', 'junior-live': '#3a6fc4', 'live-flx-zero': '#1b8f7a'}
COLORS.update(NEWCOL)
from seed_extra import EXTRA, EXTRA_COLORS, EXTRA_BADGES
SEED += EXTRA
COLORS.update(EXTRA_COLORS)
BADGES = {'oregano': 'Nuevo producto', 'dolmit': 'Nueva imagen', 'calbidenhs': 'Llévalo en kit'}
BADGES.update(EXTRA_BADGES)

def db():
    c = sqlite3.connect(DB); c.row_factory = sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c

def init():
    c = db()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS productos(id INTEGER PRIMARY KEY, slug TEXT UNIQUE, nombre TEXT, categoria TEXT,
      descripcion TEXT, imagen TEXT, detalle TEXT, activo INTEGER DEFAULT 1);
    CREATE TABLE IF NOT EXISTS variantes(id INTEGER PRIMARY KEY, producto_id INTEGER REFERENCES productos(id),
      codigo TEXT, etiqueta TEXT, precio INTEGER, stock INTEGER DEFAULT 100);
    CREATE TABLE IF NOT EXISTS pedidos(id INTEGER PRIMARY KEY, fecha TEXT, cliente TEXT, telefono TEXT, ciudad TEXT,
      direccion TEXT, notas TEXT, total INTEGER, estado TEXT DEFAULT 'nuevo');
    CREATE TABLE IF NOT EXISTS pedido_items(id INTEGER PRIMARY KEY, pedido_id INTEGER REFERENCES pedidos(id),
      variante_id INTEGER, nombre TEXT, cantidad INTEGER, precio INTEGER);''')
    have = {r[0] for r in c.execute('SELECT slug FROM productos')}
    if True:  # agrega solo los productos que aún no existen (no pisa tus precios editados)
        for slug, n, cat, d, img, det, vs in SEED:
            if slug in have: continue
            pid = c.execute('INSERT INTO productos(slug,nombre,categoria,descripcion,imagen,detalle) VALUES(?,?,?,?,?,?)',
                            (slug, n, cat, d, img, json.dumps(det, ensure_ascii=False))).lastrowid
            c.executemany('INSERT INTO variantes(producto_id,codigo,etiqueta,precio) VALUES(?,?,?,?)', [(pid, *v) for v in vs])
    cols = [r[1] for r in c.execute('PRAGMA table_info(productos)')]
    for col in ('color', 'badge'):
        if col not in cols: c.execute(f'ALTER TABLE productos ADD COLUMN {col} TEXT')
    for k, v in COLORS.items(): c.execute('UPDATE productos SET color=? WHERE slug=?', (v, k))
    for k, v in BADGES.items(): c.execute('UPDATE productos SET badge=? WHERE slug=?', (v, k))
    c.commit(); c.close()

class H(BaseHTTPRequestHandler):
    def out(self, code, body, ct='application/json; charset=utf-8', cache='no-cache'):
        b = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code); self.send_header('Content-Type', ct); self.send_header('Content-Length', str(len(b)))
        self.send_header('Cache-Control', cache); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path); p = u.path
        if p.startswith('/api/'): return self.api_get(p, parse_qs(u.query))
        f = os.path.normpath(os.path.join(PUB, p.lstrip('/')))
        if not f.startswith(PUB) or not os.path.isfile(f): f = os.path.join(PUB, 'index.html')
        ct = mimetypes.guess_type(f)[0] or 'application/octet-stream'
        if f.endswith('.webmanifest'): ct = 'application/manifest+json'
        with open(f, 'rb') as fh:
            self.out(200, fh.read(), ct, 'public, max-age=86400' if '/img/' in f else 'no-cache')

    def api_get(self, p, q):
        c = db()
        try:
            if p == '/api/productos':
                rows = c.execute('''SELECT p.slug,p.nombre,p.categoria,p.descripcion resumen,p.imagen,p.color,p.badge,p.detalle,
                    MIN(v.precio) desde,COUNT(*) n,
                    (SELECT id FROM variantes WHERE producto_id=p.id ORDER BY precio LIMIT 1) vid,
                    (SELECT etiqueta FROM variantes WHERE producto_id=p.id ORDER BY precio LIMIT 1) etiqueta,
                    (SELECT codigo FROM variantes WHERE producto_id=p.id ORDER BY precio LIMIT 1) codigo
                    FROM productos p JOIN variantes v ON v.producto_id=p.id WHERE p.activo=1 GROUP BY p.id ORDER BY p.id''').fetchall()
                out = []
                for r in rows:
                    d = dict(r); d['detalle'] = json.loads(d['detalle']); out.append(d)
                return self.out(200, out)
            if p.startswith('/api/productos/'):
                r = c.execute('SELECT * FROM productos WHERE slug=? AND activo=1', (p.split('/')[-1],)).fetchone()
                if not r: return self.out(404, {'error': 'Producto no encontrado'})
                d = dict(r); d['detalle'] = json.loads(d['detalle'])
                d['variantes'] = [dict(v) for v in c.execute(
                    'SELECT id,codigo,etiqueta,precio FROM variantes WHERE producto_id=? ORDER BY id', (r['id'],))]
                return self.out(200, d)
            if p == '/api/pedidos':
                if not ADMIN or q.get('clave', [''])[0] != ADMIN: return self.out(403, {'error': 'No autorizado'})
                ps = [dict(r) for r in c.execute('SELECT * FROM pedidos ORDER BY id DESC LIMIT 200')]
                for o in ps: o['items'] = [dict(i) for i in c.execute('SELECT nombre,cantidad,precio FROM pedido_items WHERE pedido_id=?', (o['id'],))]
                return self.out(200, ps)
            self.out(404, {'error': 'No existe'})
        finally: c.close()

    def do_POST(self):
        if self.path != '/api/pedidos': return self.out(404, {'error': 'No existe'})
        try:
            n = int(self.headers.get('Content-Length', 0))
            if n > 50000: raise ValueError('Solicitud demasiado grande')
            d = json.loads(self.rfile.read(n))
            g = lambda k: str(d.get(k, '')).strip()[:200]
            cli, tel, dire = g('cliente'), ''.join(ch for ch in g('telefono') if ch.isdigit()), g('direccion')
            if len(cli) < 2 or len(tel) < 7 or len(dire) < 5: raise ValueError('Completa nombre, teléfono y dirección')
            items = d.get('items') or []
            if not items or len(items) > 50: raise ValueError('El carrito está vacío')
            c = db()
            try:
                lines, total = [], 0
                for it in items:
                    q = int(it.get('cantidad', 0))
                    v = c.execute('SELECT v.id,v.etiqueta,v.precio,p.nombre FROM variantes v JOIN productos p ON p.id=v.producto_id WHERE v.id=? AND p.activo=1', (int(it.get('variante_id', 0)),)).fetchone()
                    if not v or not 1 <= q <= 99: raise ValueError('Producto o cantidad inválidos')
                    lines.append((v['id'], f"{v['nombre']} {v['etiqueta']}", q, v['precio'])); total += q * v['precio']
                oid = c.execute('INSERT INTO pedidos(fecha,cliente,telefono,ciudad,direccion,notas,total) VALUES(?,?,?,?,?,?,?)',
                                (datetime.now().isoformat(timespec='seconds'), cli, tel, g('ciudad'), dire, g('notas'), total)).lastrowid
                c.executemany('INSERT INTO pedido_items(pedido_id,variante_id,nombre,cantidad,precio) VALUES(?,?,?,?,?)', [(oid, *l) for l in lines])
                c.commit()
            finally: c.close()
            self.out(201, {'id': oid, 'total': total})
        except (ValueError, TypeError, json.JSONDecodeError) as e:
            self.out(400, {'error': str(e) or 'Datos inválidos'})

    def log_message(self, *a): pass

if __name__ == '__main__':
    init()
    try:
        import build_catalogo; build_catalogo.build()  # mantiene la vista previa estática al día
    except Exception as e: print('aviso catalogo.js:', e)
    print(f'Live+Nat en http://localhost:{PORT}')
    ThreadingHTTPServer(('0.0.0.0', PORT), H).serve_forever()
