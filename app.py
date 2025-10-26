from flask import Flask, render_template, redirect, url_for, session, flash, request
import sqlite3
import datetime
import os

# === CONFIGURACIÓN BÁSICA ===
app = Flask(__name__)
app.secret_key = 'clave_secreta'
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

# === FUNCIONES DE BASE DE DATOS ===
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_productos():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, precio, imagen FROM productos')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_producto(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, precio, imagen, descripcion FROM productos WHERE id = ?', (id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def registrar_compra(carrito):
    conn = get_db()
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO compras (fecha, total) VALUES (?, ?)', (fecha, total))
    compra_id = cursor.lastrowid
    for item in carrito.values():
        cursor.execute('''
            INSERT INTO detalle_compra (compra_id, producto_id, nombre_producto, cantidad, subtotal)
            VALUES (?, ?, ?, ?, ?)
        ''', (compra_id, item['id'], item['nombre'], item['cantidad'], item['precio'] * item['cantidad']))
    conn.commit()
    conn.close()

# === VERIFICACIÓN DE TABLAS ===
def verificar_tablas():
    """Devuelve True si todas las tablas necesarias existen"""
    tablas_necesarias = {'productos', 'compras', 'detalle_compra'}
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas_existentes = {t[0] for t in cursor.fetchall()}
    conn.close()
    faltantes = tablas_necesarias - tablas_existentes
    if faltantes:
        print(f"⚠️ Tablas faltantes en la base de datos: {faltantes}")
        return False
    return True

@app.context_processor
def inject_db_warning():
    tablas_ok = verificar_tablas()
    return dict(db_warning=not tablas_ok)

# === RUTAS PRINCIPALES ===
@app.route('/')
def index():
    productos = get_productos()
    return render_template('index.html', productos=productos)

@app.route('/agregar/<int:id>')
def agregar(id):
    producto = get_producto(id)
    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for('index'))

    carrito = session.get('carrito', {})
    if str(id) in carrito:
        carrito[str(id)]['cantidad'] += 1
    else:
        carrito[str(id)] = {
            'id': producto['id'],
            'nombre': producto['nombre'],
            'precio': producto['precio'],
            'cantidad': 1,
            'imagen': producto['imagen']  # <-- imagen incluida
        }

    session['carrito'] = carrito
    flash(f"{producto['nombre']} agregado al carrito 🛒", "success")
    return redirect(url_for('index'))

@app.route('/carrito')
def carrito():
    carrito = session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    return render_template('cart.html', carrito=carrito, total=total)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    carrito = session.get('carrito', {})
    if str(id) in carrito:
        del carrito[str(id)]
        session['carrito'] = carrito
        flash("Producto eliminado del carrito ❌", "info")
    return redirect(url_for('carrito'))

@app.route('/finalizar', methods=['POST'])
def finalizar():
    carrito = session.get('carrito', {})
    if not carrito:
        flash("Tu carrito está vacío.", "warning")
        return redirect(url_for('index'))

    # Chequeo de tablas antes de registrar compra
    tablas_existentes = verificar_tablas()
    if not tablas_existentes:
        flash("Error: Las tablas necesarias no existen en la base de datos.", "danger")
        return redirect(url_for('carrito'))

    registrar_compra(carrito)
    session.pop('carrito', None)
    flash("Compra registrada exitosamente ✅ ¡Gracias por tu pedido!", "success")
    return redirect(url_for('historial'))

@app.route('/historial')
def historial():
    conn = get_db()
    compras = conn.execute('SELECT * FROM compras ORDER BY fecha DESC').fetchall()
    conn.close()
    return render_template('historial.html', compras=compras)

# === EJECUCIÓN ===
if __name__ == '__main__':
    if not verificar_tablas():
        print("❌ Advertencia: La base de datos no tiene todas las tablas necesarias.")
        print("Ejecuta init_db.py para crear las tablas antes de usar la app.")
    app.run(debug=True)
