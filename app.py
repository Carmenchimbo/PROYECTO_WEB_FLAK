from flask import Flask, render_template, request, redirect, url_for
from config import get_db_connection

app = Flask(__name__)

# --- Rutas principales ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# --- CRUD Productos (Libros) ---
@app.route("/productos")
def ver_productos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template("productos.html", productos=productos)

@app.route("/productos/agregar", methods=["POST"])
def agregar_producto():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    precio = request.form["precio"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (titulo, autor, precio) VALUES (%s, %s, %s)",
                   (titulo, autor, precio))
    conn.commit()
    conn.close()
    return redirect(url_for("ver_productos"))

@app.route("/productos/eliminar/<int:id>")
def eliminar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("ver_productos"))

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == "POST":
        titulo = request.form["titulo"]
        autor = request.form["autor"]
        precio = request.form["precio"]
        cursor.execute("UPDATE productos SET titulo=%s, autor=%s, precio=%s WHERE id=%s",
                       (titulo, autor, precio, id))
        conn.commit()
        conn.close()
        return redirect(url_for("ver_productos"))
    cursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template("editar_producto.html", producto=producto)

# --- CRUD Clientes ---
@app.route("/clientes")
def ver_clientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return render_template("clientes.html", clientes=clientes)

@app.route("/clientes/agregar", methods=["POST"])
def agregar_cliente():
    nombre = request.form["nombre"]
    email = request.form["email"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nombre, email) VALUES (%s, %s)", (nombre, email))
    conn.commit()
    conn.close()
    return redirect(url_for("ver_clientes"))

@app.route("/clientes/eliminar/<int:id>")
def eliminar_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("ver_clientes"))

@app.route("/clientes/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        cursor.execute("UPDATE clientes SET nombre=%s, email=%s WHERE id=%s", (nombre, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for("ver_clientes"))
    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()
    conn.close()
    return render_template("editar_cliente.html", cliente=cliente)

# --- Inventario (solo lectura de productos) ---
@app.route("/inventario")
def inventario():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template("inventario.html", productos=productos)

if __name__ == "__main__":
    app.run(debug=True)


