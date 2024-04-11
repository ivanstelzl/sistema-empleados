from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ivojubese7523'
app.config['MYSQL_DB'] = 'empleados'
mysql = MySQL(app)

@app.route('/')
def index():
        
        cur = mysql.connection.cursor()

        sql = "SELECT * FROM empleados;"
        cur.execute(sql)
        mysql.connection.commit()

        empleados = cur.fetchall()
        print(empleados)

        return render_template('index.html', empleados=empleados)



@app.route('/create')
def create():
        return render_template("create.html")



@app.route('/store', methods=["POST"])
def store():
     nombre = request.form["txtnombre"]
     correo = request.form["txtcorreo"]
     foto = request.files["txtfoto"]

     print(nombre)
     print(correo)
     print(foto)

     cur = mysql.connection.cursor()
     cur.execute('INSERT INTO empleados (nombre, correo, foto) VALUES (%s, %s, %s)', 
                       (nombre, correo, foto.filename))
     mysql.connection.commit()

     return redirect('/')



     
    

if __name__ == '__main__':
    app.run(port=3000, debug = True)


    