from flask import Flask, render_template, redirect, url_for, session
import sqlite3

# === CONFIGURACIÓN BÁSICA ===
app = Flask(__name__)
app.secret_key = 'clave_secreta'
DB_PATH = 'database.db'

# === FUNCIÓN PARA CONECTAR A LA BD ===
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder por nombre (ej: row['nombre'])
    return conn

# === CONSULTAS A LA BASE DE DATOS ===
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

# === RUTAS PRINCIPALES ===
@app.route('/')
def index():
    productos = get_productos()
    return render_template('index.html', productos=productos)

@app.route('/producto/<int:id>')
def producto(id):
    p = get_producto(id)
    if not p:
        return redirect(url_for('index'))
    return render_template('product.html', producto=p)

# === CARRITO ===
@app.route('/agregar/<int:id>')
def agregar(id):
    producto = get_producto(id)
    if producto:
        if 'carrito' not in session:
            session['carrito'] = []
        session['carrito'].append(producto)
    return redirect(url_for('carrito'))

@app.route('/carrito')
def carrito():
    carrito = session.get('carrito', [])
    total = sum([p['precio'] for p in carrito])
    return render_template('cart.html', carrito=carrito, total=total)

@app.route('/vaciar')
def vaciar():
    session.pop('carrito', None)
    return redirect(url_for('index'))

# === EJECUCIÓN LOCAL ===
if __name__ == '__main__':
    app.run(debug=True)
