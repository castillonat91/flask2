from flask import Flask,  request, render_template, redirect, url_for, flash
import mysql.connector

#creamos una instancia de la clase flask

app = Flask(__name__)

#configurar la conexion
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="AGENDA2024"
)
cursor = db.cursor()

#definir rutas
@app.route('/')
def lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM personas')
    personas = cursor.fetchall()
    return render_template('index.html',personas=personas)

@app.route('/registrar', methods=['POST'])
def registrar_usuarios():
    NOMBRE = request.form['nombre'],
    APELLIDO = request.form['apellido'],
    EMAIL = request.form['correo'],
    DIRECCION = request.form['direccion'],
    TELEFONO = request.form['telefono'],
    USUARIO = request.form['usuario'],
    CONTRASEÑA = request.form['contraseña'],
    
    #insertar datos a la tlaba personas
    
    cursor.execute("INSERT INTO personas(nombreper,apellidoper,emailper,dirper,telper,usuarioper,contraper)VALUES(%s,%s,%s,%s,%s,%s,%s)",(NOMBRE,APELLIDO,EMAIL,DIRECCION,TELEFONO,USUARIO,CONTRASEÑA))
    
    db.commit()
    flash('usuario creado correctament','success')
    return redirect(url_for('registrar.html'))

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
         
        sql = "update personas set nombreper=%s, apellidoper=%s,emailper=%s,dirreccionper=%s, telefonoper=%s,usuarioper=%s, contraper=%s where idpersona=%s"
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