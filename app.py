from flask import Flask,render_template,request,redirect,url_for,flash
from flask_mysqldb import MySQL

app= Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='db_floreria' 
app.secret_key='mysecretkey'
mysql= MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        Vnombre= request.form['txtNombre']
        Vcantidad= request.form['txtCantidad']
        Vprecio= request.form['txtPrecio']
        CS = mysql.connection.cursor()
        CS.execute('insert into tbflores (Nombre, cantidad, precio) values (%s, %s, %s)',(Vnombre, Vcantidad, Vprecio))
        mysql.connection.commit()

    flash('La flor "'+ Vnombre +'" fue agregada correctamente')
    return redirect(url_for('index'))


@app.route('/Consultar_flor')
def Consultar_flor():
    return render_template('Consultar_flor.html')

@app.route('/Buscar', methods=['GET', 'POST'])
def Buscar():
    if request.method == 'POST':
        Vflor= request.form['txtFlor']
        CC1=mysql.connection.cursor() 
        CC1.execute('SELECT * FROM tbflores WHERE Nombre = %s', (Vflor,)) 
        busFlores=CC1.fetchall()
        return render_template('Consultar_flor.html', listFlores=busFlores)
    flash('Mostrando resultados de la flor "'+ Vflor +'"')
    return redirect(url_for('Consultar_flor'))

@app.route('/Editar/<string:id>')
def editar(id):
    cursorID= mysql.connection.cursor()
    cursorID.execute('SELECT * from tbflores where id=%s', (id,))
    consulID=cursorID.fetchone()
    return render_template('Editar_flor.html', flor=consulID)

@app.route('/Actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        varFruta=request.form['txtNombre']
        varTemporada=request.form['txtCantidad']
        varPrecio=request.form['txtPrecio']
        varStock=request.form['txtAnio']
        curAct = mysql.connection.cursor()
        curAct.execute('UPDATE tbfrutas set fruta = %s, temporada= %s, precio =%s, stock=%s WHERE id=%s',(varFruta, varTemporada, varPrecio, varStock, id))
        mysql.connection.commit()
    flash('La fruta ' + varFruta + ' fue actualizada correctamente ')
    return redirect(url_for('Consuktar_flor'))

if __name__ == '__main__':
    app.run(port=5000,debug=True)