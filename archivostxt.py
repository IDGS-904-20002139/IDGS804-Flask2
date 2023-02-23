# Esto sireve para leer los datos de un archivo de texto
# f=open('alumnos.txt','r')


# alumnos=f.read()
# print(alumnos)
# f.seek(20)
# alumnos2=f.read()
# print(alumnos2)

# alumnos=f.readlines()
# print(alumnos)
#  print(alumnos[0])
# for item in alumnos:
#     print(item,end='')

# alumnos=f.readline()
# print(alumnos)
# f.close()



# Esto sireve para escribir dato en un archivo de texto y crearlo
# si no sirve, pero remplaza lo que hay en el archivo
# f=open('alumnos2.txt','w')
# f.write('Hola Mundo!!!!')
# f.write('Nuevo Hola Mundo!!!!')
# f.close()

# Esto sireve para escribir dato en un archivo de texto
f=open('alumnos2.txt','a')
f.write('\n'+'Hola Mundo!!!!')
f.write('\n'+'Nuevo Hola Mundo!!!!')
f.close()