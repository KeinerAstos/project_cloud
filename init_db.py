import sqlite3

def crear_bd():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # === CREAR TABLAS ===
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        imagen TEXT NOT NULL,
        descripcion TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        total REAL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS detalle_compra (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        compra_id INTEGER NOT NULL,
        producto_id INTEGER NOT NULL,
        nombre_producto TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (compra_id) REFERENCES compras (id)
    );
    ''')

    # === INSERTAR PRODUCTOS INICIALES ===
    productos = [
        ('Cartier Cubano', 2500000, 'cartier_dorado.jpg',
         'COMBO DE RELOJ CUBANO CARTIER, PULSERA Y ANILLO 💎⚡️ Envíos a toda Colombia.'),
        ('Rolex Plateado', 3100000, 'rolex_plateado.jpg',
         'Reloj Rolex plateado con detalles brillantes 💎✨, fabricado en acero inoxidable, resistente al agua y con cierre tipo mariposa.'),
        ('Richard Mille', 4800000, 'richard_millie.jpg',
         'Reloj Richard Mille de diseño moderno y elegante ⚡️💎, ideal para quienes buscan lujo y estilo.'),
        ('Rolex Dorado', 4500000, 'rolex_dorado.jpg',
         'Rolex dorado de alta gama con incrustaciones de microzircones ✨💎, una pieza imponente y sofisticada.'),
        ('Anillo Rolex', 380000, 'anillo_rolex.jpg',
         'Anillo en acero inoxidable con diseño de corona Rolex 💍💎 — resistente, brillante y lleno de estilo.'),
        ('Rolex Negro', 4200000, 'rolex_negro.jpg',
         'Reloj Rolex negro con microzircones de alta calidad 💎⚡️ — elegancia y poder en cada detalle.'),
        ('Grillz', 600000, 'grillz.jpg',
         'Grillz en color plateado y dorado 💎✨ — ajustables, brillantes y perfectos para destacar tu estilo urbano.'),
        ('Cadena Púas', 520000, 'cadena_puas.jpg',
         'Cadena dorada en forma de púas ✨💎 — excelente calidad, resistente y ajustable a cualquier medida 📏🔥.'),
        ('Anillo Blessd', 400000, 'anillo_blessd.jpg',
         'Anillo inspirado en el artista Blessd 💍⚡️ — diseño exclusivo, elaborado en acero premium con detalles únicos.')
    ]

    cursor.executemany('INSERT INTO productos (nombre, precio, imagen, descripcion) VALUES (?, ?, ?, ?)', productos)
    conn.commit()
    conn.close()

    print("✅ Base de datos creada y poblada con éxito.")

# === EJECUTAR CREACIÓN ===
if __name__ == "__main__":
    crear_bd()
