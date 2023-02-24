from flask import Flask, render_template
from flask import request
from flask_wtf.csrf import CSRFProtect
from collections import Counter
import forms
import cajasDinamicas
from flask import make_response
from flask import flash


app=Flask(__name__)
app.config['SECRET_KEY']="esta es una clave encriptada"
csrf=CSRFProtect()

@app.route("/")
def formprueba():
    return render_template("formprueba.html")

@app.route("/Alumnos", methods=['GET','POST'])
def Alumnos():
    reg_alum=forms.UserForm(request.form)
    datos=list()
    if request.method=='POST' and reg_alum.validate():
        datos.append(reg_alum.matricula.data)
        datos.append(reg_alum.nombre.data)
        print(reg_alum.matricula.data)
        print(reg_alum.nombre.data)
    return render_template('Alumnos.html',form=reg_alum,datos=datos)


@app.route("/CajasDi", methods=['GET','POST'])
def CajasDi():
    reg_caja=cajasDinamicas.CajaForm(request.form)
    if request.method=='POST':
        btn = request.form.get("btn")
        if btn == 'Cargar':
            return render_template('cajasDinamicas.html',form=reg_caja)
        if btn == 'Datos':
            numero = request.form.getlist("numeros")
            max_value = None
            for num in numero:
                if (max_value is None or num > max_value):
                    max_value = num

            min_value = None
            for num in numero:
                if (min_value is None or num < min_value):
                    min_value = num

            for i in range(len(numero)):
                numero[i] = int(numero[i])


            prom = 0
            prom = sum(numero) / len(numero)

            counter = Counter(numero)
            resultados = counter.most_common()
            textoResultado = ''
            for r in resultados:
                textoResultado += '<p>El número {0} se repite {1}</p>'.format(r[0], r[1])
            return render_template('cajasDinamicas.html',form=reg_caja, max_value=max_value, min_value=min_value, prom=prom, repetidos = textoResultado)
    return render_template('cajasDinamicas.html', form=reg_caja)

@app.route("/Traductor", methods=['GET','POST'])
def traductor():
    reg_traductor=forms.Traductor(request.form)
    reg_palabra=forms.Palabra(request.form)
    if request.method=='POST' and reg_traductor.validate():
        paEsp = reg_traductor.espaniol.data
        paIng = reg_traductor.ingles.data
        btn = request.form.get("btn")
        
        if btn == 'Guardar':
            f=open('traductor.txt','w')
            paEsp=f.write(paEsp.lower()+','+paIng.lower())
            f.close()
            return render_template('traductor.html',reg_traductor=reg_traductor, reg_palabra=reg_palabra,paEsp=paEsp, paIng=paIng)
    
    if request.method=='POST' and reg_palabra.validate():  
        btn = request.form.get("btn")      
        if btn == 'Traducir':
            rbPalabra = request.form.get("rbPalabra")
            palabra= reg_palabra.palabra.data.lower()
            with open('traductor.txt', 'r') as archivo:
                for line in archivo:
                    esp, ing = line.strip().split(',')
                    if rbPalabra == '1' and ing == palabra:
                        result = esp
                        break
                    elif rbPalabra == '2' and esp == palabra:
                        result = ing
                        break
                else:
                    result = 'No se pudo encontrar la traducción'
        
            return render_template('traductor.html',reg_traductor=reg_traductor, reg_palabra=reg_palabra, palabra=palabra,result=result)
    return render_template("traductor.html", reg_traductor=reg_traductor,reg_palabra= reg_palabra)

@app.route("/cookie", methods=['GET','POST'])
def cookie():
    reg_user=forms.LoginForm(request.form)
    response=make_response(render_template('cookie.html', form=reg_user))

    if request.method == 'POST' and reg_user.validate():
        user=reg_user.username.data
        password=reg_user.password.data
        datos=user+'@'+password
        success_message='Bienvenido {}'.format(user)
        response.set_cookie('datos_usuario',datos)
        flash(success_message)
    return response

if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug=True,port=3000)