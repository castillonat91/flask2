from flask import Flask,  request, render_template, redirect, url_for, flash,session
import bcrypt
import mysql.connector

#creamos una instancia de la clase flask

app = Flask(__name__)

#configurar la conexion
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="AGENDA2025"
)
cursor = db.cursor()


def encriptarcontra(contraencrip):

    encriptar = bcrypt.hashpw(contraencrip.encode('utf-8'),bcrypt.gensalt())
    return encriptar

@app.route('/login', methods=['GET','PSOT'])
def login():
    if request.method =='POST':
        username= request.form.get('txtusuario')
        password= request.form.get('txtcontrasena')

        cursor = db.cursor()
        cursor.execute('SELECT usuarioper, contraper FROM Personas where usuarioper = %s', (username,))
        usuarios = cursor.fetchone()

        if usuarios and bcrypt.check_password_hash(usuarios[7],password):
            session['usuario'] = username
            return redirect(url_for('lista'))
        else:
            error='Credenciales invalidas. por favor intentarlo de nuevo'
            return render_template('sesion.html', error=error)
    return render_template('sesion.html')
        
#definir rutas
@app.route('/')
def lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Personas')
    usuario = cursor.fetchall() 
    return render_template('index.html',   personas = usuario)


@app.route('/registrar', methods=['GET','POST'])
def registrar_usuarios():

    if request.method == 'POST':
        NOMBRE = request.form.get('nombrePer')
        APELLIDO = request.form.get('apellidoPer')
        EMAIL = request.form.get('correoPer')
        DIRECCION = request.form.get('direccionPer')
        TELEFONO = request.form.get('telefonoPer')
        USUARIO = request.form.get('usuarioPer')
        CONTRASENA = request.form.get('contrasenaPer')
        contrasenaencriptada = encriptarcontra(CONTRASENA)
        
        #insertar datos a la tlaba personas
        
        cursor.execute("INSERT INTO Personas(nombreper,apellidoper,emailper,dirper,telper,usuarioper,contraper)VALUES(%s,%s,%s,%s,%s,%s,%s)",(NOMBRE,APELLIDO,EMAIL,DIRECCION,TELEFONO,USUARIO,contrasenaencriptada))
        db.commit()
        flash('usuario creado correctament','success')
        return redirect(url_for('registrar_usuarios()'))
    return render_template('registrar.html')

@app.route("/editar/<int:id>", methods=["POST", "GET"])
def editar_usuario(id):
    cursor = db.cursor()
    if request.method == "POST":
        nombreper = request.form.get("nombre")
        apelldioper = request.form.get("apellido")
        emailper = request.form.get("email")
        dirreccionper = request.form.get("direccion")
        telefonoper = request.form.get("telefono")
        usuarioper = request.form.get("usuario")
        contraper = request.form.get("contraseña")
         
        sql = "update Personas set nombreper=%s, apellidoper=%s,emailper=%s,dirreccionper=%s, telefonoper=%s,usuarioper=%s, contraper=%s where idpersona=%s"
        cursor.execute(
            sql,
            (
                nombreper,
                apelldioper,
                emailper,
                dirreccionper,
                telefonoper,
                usuarioper,
                contraper,
                id,
            ),
        )
        db.commit()

        return redirect(url_for("lista"))

    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM personas WHERE idper=%s", (id,))
        data = cursor.fetchall()
        return render_template("editar.html", usuario=data[0])
    
@app.route("/eliminar/<int:id>", methods=["GET"])
def eliminar_usuario(id):
    cursor = db.cursor()
    if request.method == "GET":
       cursor.execute('DELETE FROM personas WHERE idper=%s',(id,))
       db.commit()
       return redirect(url_for("lista"))
  
# para ejecutar la aplicacion
if __name__ == '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True,port=5005)