# Live+Nat · tienda PWA

## Vista previa en VS Code (sin instalar nada)
1. Instala la extensión **Live Server** (Ritwick Dey).
2. Clic derecho sobre `public/index.html` → **Open with Live Server**.
3. Verás la tienda completa con el catálogo (copia en `public/catalogo.js`). El carrito funciona; los pedidos se guardan solo en tu navegador y se confirman por WhatsApp.

## Con base de datos real
1. En la terminal de VS Code: `python server.py` (o `python3 server.py`).
2. Abre http://localhost:8000
3. Los pedidos quedan en `tienda.db`. Para verlos: `ADMIN_KEY=tuclave python3 server.py` y abre `/api/pedidos?clave=tuclave`.

## Cambios frecuentes
- **Precios:** edita `server.py` (lista `SEED`) y `seed_extra.py`; luego `python3 build_catalogo.py`. Si ya existe `tienda.db`, borra el archivo para que tome los nuevos precios.
- **Número de WhatsApp:** constante `WA` al inicio del script de `public/index.html`.
- **Instalable como app (PWA):** requiere HTTPS al publicarla; en localhost también funciona.
