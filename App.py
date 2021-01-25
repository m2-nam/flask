import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask.globals import session
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, send

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Yess', password='12345'))
users.append(User(id=2, username='Sean', password='112233'))
users.append(User(id=3, username='Maslov', password='102030'))

app = Flask(__name__)

#MySQL Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'my76'
app.config['MYSQL_DB'] = 'yanki'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'
socketio = SocketIO(app)

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = 0
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/')
def Index():
    if not g.user:
        return redirect(url_for('Login'))    
    return render_template('main.html')

@app.route('/login/', methods=['GET', 'POST'])
def Login():
    session.clear()
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('Index'))

        return redirect(url_for('Login'))

    return render_template('login.html')
    '''msg = ''
    if request.method == 'POST' and 'email_usuario' in request.form and 'password_usuario' in request.form:
        email_usuario = request.form['email_usuario']
        password_usuario = request.form['password_usuario']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE email_usuario = %s AND password_usuario = %s', (email_usuario, password_usuario))
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id_usuario'] = account['id_usuario']
            session['email_usuario'] = account['email_usuario']
            # Redirect to home page
            return render_template('main.html')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)'''

@app.route('/registro/', methods=['GET', 'POST'])
def Registro():
    if request.method == 'GET':
        return render_template('registro.html')
    else:
        dni = request.form['dni']
        nombre_usuario = request.form['nombre_usuario']
        apellido_usuario = request.form['apellido_usuario']
        ciudad_usuario = request.form['ciudad_usuario']
        email_usuario = request.form['email_usuario']
        password_usuario = request.form['password_usuario']
        descripcion_usuario = request.form['descripcion_usuario']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO usuarios (dni,nombre_usuario,apellido_usuario,ciudad_usuario,email_usuario,password_usuario,descripcion_usuario) VALUES (%s,%s,%s,%s,%s,%s,%s)', (dni, nombre_usuario, apellido_usuario, ciudad_usuario, email_usuario, password_usuario, descripcion_usuario))
        mysql.connection.commit()
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id_usuario'] = account['id_usuario']
            session['email_usuario'] = account['email_usuario']
            # Redirect to home page
            return render_template('main.html')
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
        return redirect(url_for('Login'))


@app.route('/usuarios/')
def Usuarios():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios')
    data = cursor.fetchall()
    return render_template('usuarios.html', usuarios = data)

@app.route('/editar_usuario/<id>')
def get_usuario(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id_usuario = %s',(id))
    data = cursor.fetchall()
    return render_template('editar_usuario.html', cli = data[0])

@app.route('/actualizar_usuario/<id>', methods = ['POST'])
def set_usuario(id):
    if request.method == 'POST':
        id = request.form ['id_usuario']
        dni = request.form['dni']
        nombre_usuario = request.form['nombre_usuario']
        apellido_usuario = request.form['apellido_usuario']
        ciudad_usuario = request.form['ciudad_usuario']
        email_usuario = request.form['email_usuario']
        password_usuario = request.form['password_usuario']
        descripcion_usuario = request.form['descripcion_usuario']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE usuarios SET id_usuario = %s, dni = %s, nombre_usuario = %s, apellido_usuario = %s, ciudad_usuario = %s, email_usuario =  %s, password_usuario = %s, descripcion_usuario = %s WHERE id_usuario = %s', (id, dni, nombre_usuario, apellido_usuario, ciudad_usuario, email_usuario, password_usuario, descripcion_usuario, id))
        mysql.connection.commit()
        flash('Usuario actualizado')
        return redirect(url_for('Usuarios'))

@app.route('/eliminar_usuario/<string:id>')
def eliminar_usuario(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id_usuario = {0}'.format(id))
    mysql.connection.commit()
    flash('Usuario eliminado')
    return redirect(url_for('Usuarios'))
    
@app.route('/articulos/')
def Articulos():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM articulos')
    data = cursor.fetchall()
    return render_template('articulos.html', articulos = data)

@app.route('/editar_articulo/<id>')
def get_articulo(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM articulos WHERE id_articulo = %s',(id))
    data = cursor.fetchall()
    return render_template('editar_articulo.html', cli = data[0])

@app.route('/agregar_articulo/', methods = ['POST'])
def guardar_articulo():
    if request.method == 'POST':
        categoria_articulo = request.form['categoria_articulo']
        nombre_articulo = request.form['nombre_articulo']
        archivo_articulo = request.form['archivo_articulo']
        descripcion_articulo = request.form['descripcion_articulo']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO articulos(categoria_articulo, nombre_articulo, archivo_articulo, descripcion_articulo) VALUES (%s,%s,%s,%s)', (categoria_articulo, nombre_articulo, archivo_articulo, descripcion_articulo))
        mysql.connection.commit()
        flash('Usuario actualizado')
        return redirect(url_for('Articulos'))

@app.route('/actualizar_articulo/<id>', methods = ['POST'])
def set_articulo(id):
    if request.method == 'POST':
        id = request.form ['id_articulo']
        categoria_articulo = request.form['categoria_articulo']
        nombre_articulo = request.form['nombre_articulo']
        archivo_articulo = request.form['archivo_articulo']
        descripcion_articulo = request.form['descripcion_articulo']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE articulos SET id_articulo = %s, nombre_articulo = %s, archivo_articulo = %s, descripcion_articulo = %s WHERE id_articulo = %s', (id, nombre_articulo, archivo_articulo, descripcion_articulo, id))
        mysql.connection.commit()
        flash('Articulo actualizado')
        return redirect(url_for('Articulos'))

@app.route('/eliminar_articulo/<string:id>')
def eliminar_producto(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM articulos WHERE id_articulo = {0}'.format(id))
    mysql.connection.commit()
    flash('Articulo eliminado')
    return redirect(url_for('Articulos'))

@app.route('/articulos/articulo_nin/')
def go_articulo():
    return render_template('articulo_nin.html')

@app.route('/articulos/articulo_hp/')
def go_articulohp():
    return render_template('articulo_hp.html')

@app.route('/articulos/articulo_gt/')
def go_articulogt():
    return render_template('articulo_gt.html')

@app.route('/articulos/articulo_cn/')
def go_articulocn():
    return render_template('articulo_cn.html')

@app.route('/articulos/articulo_ps/')
def go_articulops():
    return render_template('articulo_ps.html')

@app.route('/articulos/articulo_hg/')
def go_articulohg():
    return render_template('articulo_hg.html')

@app.route('/acerca_de/')
def acerca_de():
    return render_template('acerca_de.html')

@app.route('/user_chat/')
def user_chat():
    return render_template('user_chat.html')

@app.route('/barterit/')
def barterit():
    return render_template('barterit.html')

@app.route('/sala_1/')
def sala_1():
    return render_template('sala_1.html')

@app.route('/sala1_2/')
def sala1_2():
    return render_template('sala1_2.html')

@app.route('/sala1_3/')
def sala1_3():
    return render_template('sala1_3.html')

@app.route('/chat_box/')
def chat_box():
    return render_template('chat_box.html')

@app.route('/entrega_1/')
def entrega_1():
    return render_template('entrega_1.html')

@app.route('/mensaje_1/')
def mensaje_1():
    return render_template('mensaje_1.html')

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast = True)


if __name__ == '__main__':
    app.run(port=3000, debug=True)