from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave-segura-cloudshop'

# --- Productos simulados (puedes conectar a DB luego) ---
productos = [
    {"id": 1, "nombre": "Reloj Cartier", "precio": 120000, "imagen": "cartier_dorado.jpg"},
    {"id": 2, "nombre": "Reloj Rolex", "precio": 78000, "imagen": "rolex_plateado.jpg"},
    {"id": 3, "nombre": "Reloj Richard Mille", "precio": 95000, "imagen": "richard_millie.jpg"}
]

@app.route('/')
def index():
    return render_template('index.html', productos=productos)

@app.route('/producto/<int:id>')
def producto(id):
    item = next((p for p in productos if p['id'] == id), None)
    return render_template('product.html', producto=item)

@app.route('/agregar/<int:id>')
def agregar(id):
    producto = next((p for p in productos if p['id'] == id), None)
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

if __name__ == '__main__':
    app.run(debug=True)
