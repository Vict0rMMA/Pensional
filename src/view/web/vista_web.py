import sys

from flask import Flask, render_template, request, redirect, url_for

sys.path.append(".")
from src.controller.app_controller import *
from src.model.CodigoPension import CalculadoraPensional

app = Flask(__name__, template_folder='templates')


@app.route("/")
def Home():
    return render_template("index.html")


@app.route("/nuevo")
def nuevo():
    return render_template("new-user.html")


@app.route("/crear-usuario", methods=["POST"])
def crear_usuario():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    sexo = request.form["sexo"]
    edad = int(request.form["edad"])

    usuario = Usuario(nombre, apellido, sexo, edad)
    ControladorUsuarios.insertar_usuario(usuario, usuario)

    return render_template("usuario.html", user=usuario, mensaje="Usuario insertado exitosamente!")


@app.route("/usuario", methods=["GET"])
def buscar_usuario():
    nombre = request.args.get("nombre")
    apellido = request.args.get("apellido")
    sexo = request.args.get("sexo")
    edad = int(request.args.get("edad"))

    usuario = Usuario(nombre, apellido, sexo, edad)
    usuario_encontrado = ControladorUsuarios.obtener_usuarios(usuario)
    return render_template("usuario.html", user=usuario_encontrado)


@app.route("/modificar-usuario", methods=["GET", "POST"])
def modificar_usuario(id_usuario):
    if request.method == "GET":
        usuario = ControladorUsuarios.obtener_usuario_por_id(id_usuario)
        return render_template("modificar-usuario.html", user=usuario)
    else:
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        sexo = request.form["sexo"]
        edad = int(request.form["edad"])

        usuario = Usuario(nombre, apellido, sexo, edad)
        ControladorUsuarios.modificar_usuario(id_usuario, usuario)
        return redirect(url_for("buscar_usuario", usuario=usuario))


@app.route("/eliminar-usuario", methods=["GET", "POST"])
def eliminar_usuario(id_usuario):
    ControladorUsuarios.eliminar_usuario(id_usuario)
    return redirect(url_for("Home"))


@app.route("/realizar-calculo", methods=["GET", "POST"])
def realizar_calculo(id_usuario):
    if request.method == "GET":
        usuario = ControladorUsuarios.obtener_usuario_por_id(id_usuario)
        return render_template("realizar-calculo.html", user=usuario)
    else:
        tipo_calculo = request.form["tipo_calculo"]
        if tipo_calculo == "ahorro_pensional":
            salario = float(request.form["salario"])
            semanas_laboradas = float(request.form["semanas_laboradas"])
            rentabilidad_fondo = float(request.form["rentabilidad_fondo"])
            tasa_administracion = float(request.form["tasa_administracion"])

            ahorro_pensional = CalculadoraPensional().calculo_ahorro_pensional(usuario.edad, salario, semanas_laboradas,
                                                                               rentabilidad_fondo, tasa_administracion)
            ControladorUsuarios.insertar_resultado_calculo(id_usuario, "ahorro_pensional", ahorro_pensional)
            return redirect(url_for("ver_historial_calculos", id_usuario=id_usuario))
        elif tipo_calculo == "calculo_pension":
            ahorro_pensional_esperado = float(request.form["ahorro_pensional_esperado"])
            esperanza_vida = float(request.form["esperanza_vida"])
            estado_civil = request.form["estado_civil"]

            pension = CalculadoraPensional().calculo_pension(usuario.edad, ahorro_pensional_esperado, usuario.sexo,
                                                             estado_civil, esperanza_vida)
            ControladorUsuarios.insertar_resultado_calculo(id_usuario, "calculo_pension", pension)
            return redirect(url_for("ver_historial_calculos", id_usuario=id_usuario))


@app.route("/historial-calculos")
def ver_historial_calculos(id_usuario):
    historial = ControladorUsuarios.obtener_resultados_calculo(id_usuario)
    return render_template("historial-calculos.html", historial=historial)


if __name__ == "__main__":
    app.run(debug=True)
