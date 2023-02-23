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
    datos=list()
    if request.method=='POST':
        paEsp = reg_traductor.espaniol.data
        paIng = reg_traductor.ingles.data
        palabra=reg_traductor.palabra

        btn = request.form.get("btn")
        rbPalabra = request.form.get("rbPalabra")
        
        if btn == 'Guardar':
            f=open('traductor.txt','w')
            paEsp=f.write(paEsp.lower())
            paIng=f.write('\n'+paIng.lower())
            f.close()
            return render_template('traductor.html',form=reg_traductor,paEsp=paEsp, paIng=paIng)
            
        if btn == 'Traducir':
            if rbPalabra == '1':
                f=open('traductor.txt','r')
                palabra=f.readlines()
                palabra1 = ('La palabra en ingles es: '+palabra[1])
                palabra2 = ('La palabra traducida al español es: '+palabra[0])
                f.close()
                return render_template('traductor.html',form=reg_traductor, palabra1=palabra1, palabra2=palabra2)
            elif rbPalabra == '2':
                f=open('traductor.txt','r')
                palabra=f.readlines()
                palabra1 = ('La palabra en español es: '+palabra[0])
                palabra2 = ('La palabra traducida en ingles es: '+palabra[1])
                f.close()
                return render_template('traductor.html',form=reg_traductor, palabra1=palabra1, palabra2=palabra2)
            else:
                print('No ahi una selección')
            return render_template('traductor.html',form=reg_traductor, palabra=palabra)
    return render_template("traductor.html", form=reg_traductor, datos=datos)

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
    # csrf.init_app(app)
    app.run(debug=True,port=3000)