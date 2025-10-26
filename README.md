# 🛍️ KestShop — Tienda Virtual con Flask

**KestShop** es una aplicación web desarrollada con **Flask** que simula una tienda virtual de joyería de lujo.  
Permite visualizar productos, ver detalles individuales y gestionar un carrito de compras.  
El proyecto incluye conexión a base de datos **SQLite**, empaquetado con **Docker** y despliegue en **AWS EC2**.

---

## 🚀 Características principales

- 🧩 Desarrollado con **Flask (Python)**  
- 💾 Base de datos **SQLite** para almacenar productos  
- 🎨 Interfaz limpia con HTML, CSS y Jinja2  
- 🛒 Carrito de compras funcional con sesión de usuario  
- 🐳 Contenerización con **Docker**  
- ☁️ Despliegue en **Amazon EC2**  
- 📦 Estructura modular y fácil de mantener  

---

## 🏗️ Estructura del proyecto

```
Project_cloud/
│
├── app.py                     # Aplicación principal Flask
├── database.db                # Base de datos SQLite
├── init_db.py                 # Script para crear la base de datos
├── requirements.txt           # Dependencias del proyecto
├── Dockerfile                 # Configuración del contenedor
│
├── static/
│   ├── css/
│   │   └── styles.css         # Estilos del sitio
│   └── img/                   # Imágenes de productos y logo
│
└── templates/
    ├── index.html             # Página principal (catálogo)
    ├── product.html           # Detalle de producto
    └── cart.html              # Carrito de compras
```

---

## 🧱 Instalación local

### 1️⃣ Clona el repositorio
```bash
git clone https://github.com/KeinerAstos/project_cloud.git
cd project_cloud
```

### 2️⃣ Crea un entorno virtual (opcional pero recomendado)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Crea la base de datos
Ejecuta el script para generar la tabla y los productos:

```bash
python init_db.py
```

### 5️⃣ Ejecuta la aplicación
```bash
python app.py
```

Abre en tu navegador:  
👉 http://127.0.0.1:5000/

---

## 🐳 Uso con Docker

### 1️⃣ Construir la imagen
```bash
docker build -t kestshop-app .
```

### 2️⃣ Ejecutar el contenedor
```bash
docker run -d -p 5000:5000 kestshop-app
```

La aplicación estará disponible en:  
👉 http://localhost:5000

---

## ☁️ Despliegue en AWS EC2

1. Crea una instancia EC2 con Ubuntu o Amazon Linux.  
2. Instala Docker:
   ```bash
   sudo apt update
   sudo apt install docker.io -y
   sudo systemctl start docker
   sudo systemctl enable docker
   ```
3. Clona el repositorio:
   ```bash
   git clone https://github.com/KeinerAstos/project_cloud.git
   cd project_cloud
   ```
4. Construye y ejecuta el contenedor:
   ```bash
   sudo docker build -t kestshop-app .
   sudo docker run -d -p 80:5000 kestshop-app
   ```
5. Accede desde tu navegador con la **IP pública** de tu instancia:
   ```
   http://<tu-ip-ec2>/
   ```

---

## 💎 Productos de ejemplo

| Producto         | Descripción breve                                         | Precio     |
|------------------|-----------------------------------------------------------|-------------|
| Cartier Cubano   | Combo de reloj, pulsera y anillo con detalles dorados 💎  | $2,500,000 |
| Rolex Plateado   | Reloj de acero inoxidable con microzircones ✨             | $3,100,000 |
| Richard Mille    | Diseño moderno y elegante ⚡️                              | $4,800,000 |
| Cadena Púas      | Cadena dorada con diseño en púas 💎                       | $520,000   |
| Anillo Blessd    | Inspirado en el artista Blessd 💍                         | $400,000   |

---

## 🧑‍💻 Autor

**Keiner Astos**  
💼 Desarrollador de Software y Bases de Datos  
📧 keinerastos@gmail.com

---

## 📜 Licencia

Este proyecto fue desarrollado con fines educativos como parte del curso de **Computación en la Nube**.  
Uso libre con atribución.
