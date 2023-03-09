from flask import Flask, render_template
from flask import request
from flask_wtf.csrf import CSRFProtect
from collections import Counter
import forms
import cajasDinamicas
from flask import make_response
from flask import flash
from config import colorConf
import math


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
            f=open('traductor.txt','a')
            paEsp=f.writelines(paEsp.lower()+','+paIng.lower()+'\n')
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

@app.route('/resist', methods=['GET', 'POST'])
def calRes():
    reg_resist = forms.ResistenciasForm(request.form)
    btn = request.form.get("btn")
    colorBanda1 =""
    colorBanda2 =""
    codHexMuilti = ""
    colorTolerancia =""
    valorResistencia =""
    valorMax =""
    valorMin =""
    codHexBanda1 =""
    codHexBanda2 =""
    codHexTolerancia =""
    ban1=""
    ban2=""
    multi=""
    tolerancia=""
    valores_guardados =[]

    if request.method == 'POST' and reg_resist.validate():
        if btn == 'Calcular Valor':
            colorBanda1 = reg_resist.banda1.data
            colorBanda2 = reg_resist.banda2.data
            colorMultiplicador = reg_resist.multiplier.data
            colorTolerancia = reg_resist.tolerancia.data
        
            codHexBanda1 = colorConf.coloresBanda[colorBanda1]
            codHexBanda2 = colorConf.coloresBanda[colorBanda2]
            codHexTolerancia =colorConf.toleranciaColor[colorTolerancia]
            codHexMuilti = colorConf.multiplicador[colorMultiplicador]


            valorResistencia = (int(colorBanda1 + colorBanda2) * 10**int(colorMultiplicador))
            valorNominal = int(colorBanda1 + colorBanda2) * 10**int(colorMultiplicador)

            if colorTolerancia == 'oro':
                valorTolerancia = 0.05
            elif colorTolerancia == 'plata':
                valorTolerancia = 0.1
            else:
                valorTolerancia = colorConf.valorTolerancia[colorTolerancia]

            valorMax = valorNominal * (1 + valorTolerancia)
            valorMin = valorNominal * (1 - valorTolerancia)

            f=open('guardarVaRes.txt','a')
            f.writelines(colorBanda1+','+colorBanda2+','+colorMultiplicador+','+colorTolerancia+'\n')        
            f.close()
            
            
    response = make_response(render_template('resistencia.html', reg_resist=reg_resist, colorBanda1=colorBanda1, colorBanda2=colorBanda2, 
                        miltiColor=codHexMuilti, toleranciaColor=colorTolerancia, 
                        valorResistencia=valorResistencia, maxResistancia=valorMax, minResistancia=valorMin,
                        nomBanda1=codHexBanda1, nomBanda2=codHexBanda2, nomTolerancia=codHexTolerancia))

    response.set_cookie('valorResistencia', str(valorResistencia))
    response.set_cookie('maxResistancia', str(valorMax))
    response.set_cookie('minResistancia', str(valorMin))

    if request.method == 'POST':
        if btn == 'Cargar Valores':
            with open('guardarVaRes.txt', 'r') as archivo:
                valores_guardados =[]
                for line in archivo:
                    ban1, ban2, multi, tolerancia = line.strip().split(',')
                    codHexBanda1 = colorConf.coloresBanda[ban1]
                    codHexBanda2 = colorConf.coloresBanda[ban2]
                    codHexMuilti = colorConf.multiplicador[multi]
                    codHexTolerancia =colorConf.toleranciaColor[tolerancia]
                    
                    valorResistencia = (int(ban1 + ban2) * 10**int(multi))
                    valorNominal = int(ban1 + ban2) * 10**int(multi)

                    if tolerancia == 'oro':
                        valorTolerancia = 0.05
                    elif tolerancia == 'plata':
                        valorTolerancia = 0.1
                    else:
                        valorTolerancia = colorConf.valorTolerancia[tolerancia]

                    valorMax = valorNominal * (1 + valorTolerancia)
                    valorMin = valorNominal * (1 - valorTolerancia)
                    
                    valores_guardados2 =[]
                    valores_guardados2.append(codHexBanda1)
                    valores_guardados2.append(codHexBanda2)
                    valores_guardados2.append(codHexMuilti)
                    valores_guardados2.append(codHexTolerancia)
                    valores_guardados2.append(valorResistencia)
                    valores_guardados2.append(valorMax)
                    valores_guardados2.append(valorMin)
                    valores_guardados.append(valores_guardados2)
                print(valores_guardados)
    response = make_response(render_template('resistencia.html', reg_resist=reg_resist, colorBanda1=ban1, 
                        colorBanda2=ban2, miltiColor=codHexMuilti, toleranciaColor=tolerancia, 
                        valorResistencia=valorResistencia, maxResistancia=valorMax, minResistancia=valorMin,
                        nomBanda1=codHexBanda1, nomBanda2=codHexBanda2, nomTolerancia=codHexTolerancia, valores_guardados=valores_guardados))

    response.set_cookie('valorResistencia', str(valorResistencia))
    response.set_cookie('maxResistancia', str(valorMax))
    response.set_cookie('minResistancia', str(valorMin)) 

    return response

if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug=True,port=3000)