
from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

ARCHIVO = "estudiantes.json"

def cargar_estudiantes():
    if not os.path.exists(ARCHIVO):
        return []

    with open(ARCHIVO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def guardar_estudiantes(estudiantes):
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(estudiantes, archivo, indent=4, ensure_ascii=False)


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensaje": "API de estudiantes funcionando correctamente"
    })

@app.route("/estudiantes", methods=["POST"])
def agregar_estudiante():
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "No se recibieron datos"}), 400

    estudiantes = cargar_estudiantes()

    nuevo_estudiante = {
        "id": max([e["id"] for e in estudiantes], default=0) + 1,
        "nombre": datos.get("nombre"),
        "matricula": datos.get("matricula"),
        "carrera": datos.get("carrera"),
        "semestre": datos.get("semestre")
    }

    estudiantes.append(nuevo_estudiante)
    guardar_estudiantes(estudiantes)

    return jsonify({
        "mensaje": "Estudiante agregado correctamente",
        "estudiante": nuevo_estudiante
    }), 201
    
@app.route("/estudiantes", methods=["GET"])
def consultar_estudiantes():
    estudiantes = cargar_estudiantes()
    return jsonify(estudiantes), 200


@app.route("/estudiantes/<int:id>", methods=["GET"])
def buscar_estudiante(id):
    estudiantes = cargar_estudiantes()

    for estudiante in estudiantes:
        if estudiante["id"] == id:
            return jsonify(estudiante), 200

    return jsonify({"error": "Estudiante no encontrado"}), 404

@app.route("/estudiantes/<int:id>", methods=["PUT"])
def actualizar_estudiante(id):
    estudiantes = cargar_estudiantes()
    datos = request.get_json()

    for estudiante in estudiantes:
        if estudiante["id"] == id:
            estudiante["nombre"] = datos.get("nombre", estudiante["nombre"])
            estudiante["matricula"] = datos.get("matricula", estudiante["matricula"])
            estudiante["carrera"] = datos.get("carrera", estudiante["carrera"])
            estudiante["semestre"] = datos.get("semestre", estudiante["semestre"])

            guardar_estudiantes(estudiantes)
            return jsonify({"mensaje": "Estudiante actualizado", "estudiante": estudiante}), 200

    return jsonify({"error": "Estudiante no encontrado"}), 404

@app.route("/estudiantes/<int:id>", methods=["DELETE"])
def eliminar_estudiante(id):
    estudiantes = cargar_estudiantes()

    for estudiante in estudiantes:
        if estudiante["id"] == id:
            estudiantes.remove(estudiante)
            guardar_estudiantes(estudiantes)
            return jsonify({"mensaje": "Estudiante eliminado"}), 200

    return jsonify({"error": "Estudiante no encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)