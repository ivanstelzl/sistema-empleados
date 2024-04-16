from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flask_mysqldb import MySQL
from datetime import datetime
import os




app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ivojubese7523'
app.config['MYSQL_DB'] = 'empleados'
app.config['SECRET_KEY'] = 'clave'

UPLOADS = os.path.join('uploads')
app.config['UPLOADS'] = UPLOADS
mysql = MySQL(app)




@app.route('/fotodeusuario/<path:foto>')
def uploads(foto):
       return send_from_directory(os.path.join('uploads'), foto)



@app.route('/Empleados')
def index():
        
        cur = mysql.connection.cursor()

        sql = "SELECT * FROM empleados;"
        cur.execute(sql)
        mysql.connection.commit()

        empleados = cur.fetchall()

        return render_template('index.html', empleados=empleados)



@app.route('/Empleados/crearEmpleado', methods=["GET", "POST"])
def alta_empleado():
        if request.method == "GET":
                return render_template("create.html")
        elif request.method == "POST":
        
                nombre = request.form["txtnombre"]
                correo = request.form["txtcorreo"]
                foto = request.files["txtfoto"]

                if nombre == "" or correo =="":
                       flash("El nombre y el correo son obligatorios.")
                       return redirect(url_for("alta_empleado"))

                now = datetime.now()
                tiempo = now.strftime("%Y%H%M%S")

                if foto.filename != "":
                        nuevoNombreFoto = tiempo + "-" + foto.filename
                        foto.save("uploads/" + nuevoNombreFoto)   

                cur = mysql.connection.cursor()
                cur.execute('INSERT INTO empleados (nombre, correo, foto) VALUES (%s, %s, %s)', 
                                (nombre, correo, nuevoNombreFoto))
                
                mysql.connection.commit()

                return redirect('/Empleados')


    
@app.route('/delete/<id>')
def delete(id):
        sql = "DELETE FROM empleados WHERE id=%s"

        cur = mysql.connection.cursor()

        sql = f'SELECT foto FROM empleados WHERE id="{id}"'
        cur.execute(sql)

        nombrefoto = cur.fetchone()[0]

        try:
               os.remove(os.path.join(app.config['UPLOADS'], nombrefoto))
        except:
               pass

        sql = f'DELETE FROM empleados WHERE id="{id}"'

        cur.execute(sql)

        mysql.connection.commit()
        return redirect("/Empleados")


@app.route('/modify/<id>')
def modify(id):
       
        sql = f'SELECT * FROM empleados WHERE id="{id}"'

        cur = mysql.connection.cursor()
        cur.execute(sql)
        empleado = cur.fetchone()
        mysql.connection.commit()
       
        return render_template("edit.html", empleado=empleado)



@app.route('/update', methods=["POST"])
def update():
        nombre = request.form["txtnombre"]
        correo = request.form["txtcorreo"]
        foto = request.files["txtfoto"]
        id = request.form["txtid"]

        cur = mysql.connection.cursor()

        if foto.filename != "":

                now = datetime.now()
                tiempo = now.strftime("%Y%H%M%S")
                nuevoNombreFoto = tiempo + "_" + foto.filename
                foto.save("uploads/" + nuevoNombreFoto)   

                sql = f'SELECT foto FROM empleados WHERE id="{id}"'
                cur = mysql.connection.cursor()
                cur.execute(sql)
                mysql.connection.commit()

                nombrefoto = cur.fetchone()[0]

                borrarEstaFoto = os.path.join(app.config['UPLOADS'], nombrefoto)
                print(borrarEstaFoto)

                try:
                        os.remove(os.path.join(app.config['UPLOADS'], nombrefoto))
                        sql = f'UPDATE empleados SET foto="{nuevoNombreFoto}" WHERE id="{id}";'
                except:
                       pass 

                cur.execute(sql)
                mysql.connection.commit()
        
        sql = f'UPDATE empleados SET nombre="{nombre}", correo="{correo}" WHERE id="{id}"'

        cur.execute(sql)
        mysql.connection.commit()

        return redirect('/Empleados')




if __name__ == '__main__':
    app.run(port=3000, debug = True)