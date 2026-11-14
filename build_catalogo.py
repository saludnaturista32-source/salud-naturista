#!/usr/bin/env python3
"""Genera public/catalogo.js (copia estática del catálogo) para la vista previa SIN servidor.
Úsalo después de cambiar precios:  python3 build_catalogo.py   (el servidor también lo hace al iniciar)"""
import json, os
import server

def build():
    server.init()
    c = server.db()
    lista, detalle = [], {}
    for r in c.execute('''SELECT p.slug,p.nombre,p.categoria,p.descripcion resumen,p.imagen,p.color,p.badge,p.detalle,
        MIN(v.precio) desde,COUNT(*) n,
        (SELECT id FROM variantes WHERE producto_id=p.id ORDER BY precio LIMIT 1) vid,
        (SELECT etiqueta FROM variantes WHERE producto_id=p.id ORDER BY precio LIMIT 1) etiqueta,
        (SELECT codigo FROM variantes WHERE producto_id=p.id ORDER BY precio LIMIT 1) codigo
        FROM productos p JOIN variantes v ON v.producto_id=p.id WHERE p.activo=1 GROUP BY p.id ORDER BY p.id'''):
        d = dict(r); d['detalle'] = json.loads(d['detalle']); lista.append(d)
    for r in c.execute('SELECT * FROM productos WHERE activo=1 ORDER BY id'):
        d = dict(r); d['detalle'] = json.loads(d['detalle'])
        d['variantes'] = [dict(v) for v in c.execute('SELECT id,codigo,etiqueta,precio FROM variantes WHERE producto_id=? ORDER BY id', (r['id'],))]
        detalle[d['slug']] = d
    c.close()
    out = os.path.join(server.PUB, 'catalogo.js')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('window.CATALOGO=' + json.dumps({'productos': lista, 'detalle': detalle}, ensure_ascii=False, separators=(',', ':')) + ';')
    return len(lista)

if __name__ == '__main__':
    print(build(), 'productos escritos en public/catalogo.js')
