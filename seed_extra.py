# Productos adicionales del catálogo Live+Nat (páginas 18 a 31).
# PRECIOS DE EJEMPLO (COP): el catálogo no trae precios. Edítalos aquí; los productos nuevos se agregan al reiniciar el servidor.
S = 'Suplementos dietarios y alimentos'
mast = lambda sab, reg: {'Sabor': sab, 'Frasco por': '60 masticables', 'Registro INVIMA': reg}
reg = lambda r: {'Registro INVIMA': r}
sp = lambda a, b, c=None: [(a, 'Spray 120 ml', 26000), (b, 'Spray 250 ml', 40000)] + ([(c, 'Kit 250 ml + 120 ml', 58000)] if c else [])

EXTRA = [
 # --- Suplementos masticables y magnesio
 ('melena-leon-ganoderma-cordyceps', 'Melena de León + Ganoderma Lucidum + Micelio Cordyceps', S, 'Suplemento masticable. Sabor frutos rojos.', 'melena.webp', mast('Frutos rojos', 'RSA-0297-2025'), [('2172', '60 masticables', 54000)]),
 ('curcuma-pimienta-negra', 'Cúrcuma + Pimienta Negra', S, 'Suplemento masticable. Sabor naranja.', 'curcuma.webp', mast('Naranja', 'RSA-0036415-2025'), [('2158', '60 masticables', 50000)]),
 ('colageno-resveratrol', 'Colágeno Hidrolizado + Resveratrol', S, 'Suplemento masticable. Sabor uva.', 'colageno-resv.webp', mast('Uva', 'RSA-0036415-2025'), [('2159', '60 masticables', 52000)]),
 ('vitaminas-masticables', 'Vitaminas masticables', S, 'Suplemento masticable. Sabor fresa.', 'vitaminas-mast.webp', mast('Fresa', 'RSA-0031367-2024'), [('2169', '60 masticables', 46000)]),
 ('citrato-de-potasio', 'Citrato de Potasio', S, 'Suplemento masticable. Sabor fresa.', 'citrato-potasio.webp', mast('Fresa', 'RSA-0034078-2024'), [('2170', '60 masticables', 44000)]),
 ('probioticos-prebioticos', 'Probióticos y Prebióticos', S, 'Suplemento masticable. Sabor naranja.', 'probioticos.webp', mast('Naranja', 'RSA-0036415-2025'), [('2171', '60 masticables', 52000)]),
 ('bisglicinato-citrato-magnesio', 'Bisglicinato de Magnesio + Citrato de Magnesio', S, 'Suplemento masticable. Sabor vainilla.', 'bisglicinato.webp', mast('Vainilla', 'RSA-0036415-2025'), [('2157', '60 masticables', 50000)]),
 ('movflex', 'Movflex', S, 'Colágeno hidrolizado, cartílago bovino, cúrcuma, cloruro de magnesio, biotina y vitamina D3. Sabor vainilla.', 'movflex.webp',
  {'Sabor': 'Vainilla', 'Frasco por': '100 masticables', 'Registro INVIMA': 'RSA-0034078-2024'}, [('2195', '100 masticables', 68000)]),
 ('super-mag', 'Super Mag · Citrato de magnesio', S, 'Citrato de magnesio. Sabor limón.', 'supermag.webp',
  {'Sabor': 'Limón', 'Porción por': '30 g', 'Registro INVIMA': 'RSA-0036271-2025 (240 g) · NSA-4231-2026 (cápsulas)'}, [('2151', '240 g', 62000), ('2196', '100 cáps. blandas', 58000)]),
 # --- Fitolive
 ('fito-castano-de-indias', 'Castaño de Indias', 'Fitolive', 'Línea Fitolive de Live+Nat.', 'fito-castano.webp', reg('PFT 2021-0002813'), [('2058', '100 cápsulas', 46000), ('2059', '30 cápsulas', 22000)]),
 ('fito-alcachofa-boldo', 'Alcachofa + Boldo', 'Fitolive', 'Línea Fitolive de Live+Nat.', 'fito-alcachofa.webp', reg('PFT2024-0002955'), [('2124', '100 cápsulas', 46000), ('2125', '60 cápsulas', 32000)]),
 ('fito-cardo-mariano', 'Cardo Mariano (Silimarina)', 'Fitolive', 'Línea Fitolive de Live+Nat.', 'fito-cardo.webp', reg('PFT2025-0003089'), [('2174', '60 cápsulas', 34000), ('2175', '100 cápsulas', 48000)]),
 ('fito-valeriana-passiflora-toronjil', 'Valeriana + Passiflora + Toronjil', 'Fitolive', 'Línea Fitolive de Live+Nat. Presentación en gotero.', 'fito-valeriana.webp', reg('PFT2024-0002982'),
  [('2133', 'Gotero 60 ml', 36000), ('2134', 'Gotero 30 ml', 22000), ('2173', 'Kit 60 ml + 30 ml', 54000)]),
 ('fito-sangre-de-drago', 'Sangre de Drago', 'Fitolive', 'Línea Fitolive de Live+Nat. Presentación en gotero.', 'fito-sangre.webp', reg('PFT2021-0002814'),
  [('2083', 'Gotero 60 ml', 38000), ('2084', 'Gotero 30 ml', 24000), ('2130', 'Kit 60 ml + 30 ml', 56000)]),
 # --- Aceites
 ('tea-tree-oil', 'Tea Tree Oil', 'Aceites esenciales', 'Aceite de árbol de té puro.', 'tea-tree.webp', {'Frasco por': '10 ml', 'Registro INVIMA': 'NSOC17005-22CO'}, [('2087', '10 ml', 32000)]),
 ('kb-drops-15', 'KB Drops 15', 'Aceites esenciales', 'Presentación en gotero.', 'kb-drops.webp', reg('NSOC16824-22CO'), [('2123', 'Gotero 30 ml', 58000), ('2127', 'Muestra médica 3 ml', 9000)]),
 ('aceite-naranja', 'Aceite de Naranja', 'Aceites naturales', 'Aceite natural en spray.', 'aceite-naranja.webp', reg('NSOC04879-21CO'), [('2004', 'Spray 120 ml', 26000)]),
 ('aceite-almendras', 'Aceite de Almendras', 'Aceites naturales', 'Aceite natural en spray.', 'aceite-almendras.webp', reg('NSOC04879-21CO'), [('2003', 'Spray 120 ml', 26000), ('2101', 'Spray 250 ml', 42000)]),
 ('aceite-argan', 'Aceite de Argán', 'Aceites naturales', 'Aceite natural en spray.', 'aceite-argan.webp', reg('NSOC04879-21CO'), [('2002', 'Spray 120 ml', 30000), ('2100', 'Spray 250 ml', 46000)]),
 ('aceite-coco', 'Aceite de Coco', 'Aceites naturales', 'Aceite natural en spray.', 'aceite-coco.webp', reg('NSOC04879-21CO'), [('2005', 'Spray 120 ml', 26000), ('2102', 'Spray 250 ml', 42000)]),
 # --- Tónicos naturales
 ('tonico-agua-de-rosas', 'Tónico Agua de Rosas', 'Tónicos naturales', 'Tónico con botánicos naturales.', 'tonico-rosas.webp', reg('NSOC23777-23CO'), sp('2007', '2008', '2030')),
 ('tonico-coco-arroz', 'Tónico de Coco y Arroz', 'Tónicos naturales', 'Tónico con botánicos naturales.', 'tonico-coco.webp', reg('NSOC23777-23CO'), [('2108', 'Spray 120 ml', 26000)]),
 ('tonico-sin-akn', 'Tónico Sin Akn', 'Tónicos naturales', 'Tónico con botánicos naturales.', 'tonico-sinakn.webp', reg('NSOC23777-23CO'), [('2109', 'Spray 120 ml', 26000)]),
 ('tonico-n-piox', 'Tónico N-Piox', 'Tónicos naturales', 'Tónico con botánicos naturales.', 'tonico-npiox.webp', reg('NSOC23777-23CO'), [('2111', 'Spray 120 ml', 26000)]),
 ('tonico-te-tree', 'Tónico Té Tree', 'Tónicos naturales', 'Tónico con botánicos naturales.', 'tonico-tetree.webp', reg('NSOC23777-23CO'), [('2162', 'Spray 120 ml', 26000)]),
 # --- Lociones, desodorante, pomada, capilar
 ('locion-hielo-mineral', 'Loción Hielo Mineral', 'Lociones refrescantes', 'Loción de sensación refrescante.', 'loc-hielo.webp', {'Sensación': 'Refrescante', 'Registro INVIMA': 'NSOC06299-21CO'}, sp('2006', '2049', '2051')),
 ('locion-livetdol', 'Loción Livetdol', 'Lociones refrescantes', 'Loción de sensación refrescante.', 'loc-livetdol.webp', {'Sensación': 'Refrescante', 'Registro INVIMA': 'NSOC06299-21CO'}, sp('2046', '2044', '2050')),
 ('locion-r-laxol', 'Loción R-Laxol', 'Lociones refrescantes', 'Loción de sensación caliente.', 'loc-rlaxol.webp', {'Sensación': 'Caliente', 'Registro INVIMA': 'NSOC06299-21CO'}, sp('2113', '2114', '2116')),
 ('locion-live-refresho-cannabis', 'Loción Live+Refresho con cannabis', 'Lociones refrescantes', 'Loción refrescante con cannabis.', 'loc-refresho.webp', reg('NSOC06299-21CO'), [('2088', 'Spray 120 ml', 30000)]),
 ('live-sweat', 'Desodorante Live+Sweat', 'Desodorantes', 'Desodorante botánico vegano con piedra alumbre, bicarbonato de sodio, arroz, aceite de coco y bambú. Para manos, pies y axilas. Unisex.', 'live-sweat.webp',
  reg('NSOC42274-25CO'), [('2160', 'Spray 60 ml', 28000), ('2161', 'Roll on 80 ml', 28000)]),
 ('pomada-calendula', 'Pomada de Caléndula', 'Pomada', 'Pomada de caléndula de 40 ml.', 'pomada.webp', reg('NSOC11526-22CO'), [('2056', '40 ml', 22000)]),
 ('shampoo-live-hair', 'Shampoo Live+Hair acción capilar', 'Cuidado capilar', 'Con aminexil, romero, quinua, pantenol, biotina y argán.', 'shampoo-hair.webp', reg('NSOC82738-17CO'), [('2105', '400 ml', 36000), ('2132', 'Kit Shampoo + Tónico', 64000)]),
 ('tonico-live-hair', 'Tónico Live+Hair', 'Cuidado capilar', 'Tónico capilar en spray de 120 ml.', 'tonico-hair.webp', reg('NSOC23777-23CO'), [('2112', 'Spray 120 ml', 34000)]),
]

# --- Esencias florales (spray 30 ml, uso oral) y Línea verde (gotero 30 ml)
for slug, nombre, cod, img in [('rescate', 'Rescate', '2060', 'rescate'), ('ansiedad', 'Ansiedad (angustia, intranquilidad)', '2061', 'ansiedad'), ('miedos', 'Miedos', '2062', 'miedos'),
  ('estres', 'Estrés', '2063', 'estres'), ('adicciones', 'Adicciones', '2064', 'adicciones'), ('duelo', 'Duelo', '2065', 'duelo'), ('valeriana', 'Valeriana', '2066', 'valeriana'),
  ('depresion', 'Depresión', '2067', 'depresion'), ('passiflora', 'Passiflora', '2068', 'passiflora'), ('control-apetito', 'Control apetito', '2069', 'control-apetito'),
  ('desapego-tusa', 'Desapego tusa', '2070', 'desapego-tusa'), ('formula-estudiante', 'Fórmula del estudiante', '2071', 'formula-estudiante'), ('sexualidad', 'Sexualidad', '2072', 'sexualidad'),
  ('hierba-san-juan', 'Hierba de San Juan', '2076', 'hierba-san-juan'), ('sueno', 'Sueño', '2145', 'sueno')]:
    EXTRA.append(('esencia-' + slug, 'Esencia floral ' + nombre, 'Esencias florales', 'Esencia floral en spray de 30 ml, uso oral.', f'esencia-{img}.webp', {'Uso': 'Oral'}, [(cod, 'Spray 30 ml', 22000)]))
for slug, nombre, cod in [('arnica', 'Árnica', '2139'), ('sililive', 'Sililive', '2140'), ('echinacea', 'Echinacea', '2141'), ('angelica', 'Angélica', '2138'),
  ('tabaclive', 'Tabaclive', '2163'), ('actelive', 'Actelive', '2164'), ('sawlive', 'Sawlive', '2165')]:
    EXTRA.append(('lv-' + slug, nombre, 'Línea verde', 'Línea verde Live+Nat en frasco gotero de 30 ml, uso oral.', f'lv-{slug}.webp', {'Uso': 'Oral'}, [(cod, 'Gotero 30 ml', 28000)]))

EXTRA_COLORS = {'melena-leon-ganoderma-cordyceps': '#8b1a1a', 'curcuma-pimienta-negra': '#e8a000', 'colageno-resveratrol': '#6a2c91', 'vitaminas-masticables': '#d99a00',
 'citrato-de-potasio': '#d4145a', 'probioticos-prebioticos': '#a08a3c', 'bisglicinato-citrato-magnesio': '#3aa6a6', 'movflex': '#1f6fa8', 'super-mag': '#1d78b5',
 'tea-tree-oil': '#3d7a35', 'kb-drops-15': '#3d7a35', 'aceite-naranja': '#e8820c', 'aceite-almendras': '#8c7a12', 'aceite-argan': '#8c7a12', 'aceite-coco': '#6b3a12',
 'tonico-agua-de-rosas': '#d6247b', 'tonico-coco-arroz': '#b5173d', 'tonico-sin-akn': '#c2185b', 'tonico-n-piox': '#b8620a', 'tonico-te-tree': '#4a8f2f',
 'locion-hielo-mineral': '#1e72b8', 'locion-livetdol': '#1fa58f', 'locion-r-laxol': '#d01f26', 'locion-live-refresho-cannabis': '#4a9a2f',
 'live-sweat': '#7bb32e', 'pomada-calendula': '#e8820c', 'shampoo-live-hair': '#7b3fa0', 'tonico-live-hair': '#7b3fa0'}
EXTRA_BADGES = {'movflex': 'Nuevo producto', 'super-mag': 'Nuevo producto', 'fito-valeriana-passiflora-toronjil': 'Nuevo producto', 'fito-sangre-de-drago': 'Llévalo en kit',
 'tonico-agua-de-rosas': 'Llévalo en kit', 'tonico-te-tree': 'Nuevo producto', 'locion-hielo-mineral': 'Nueva imagen', 'locion-livetdol': 'Llévalo en kit',
 'locion-r-laxol': 'Llévalo en kit', 'locion-live-refresho-cannabis': 'Nueva presentación', 'shampoo-live-hair': 'Llévalo en kit'}
