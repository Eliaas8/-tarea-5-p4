import json
from db import conectar_keydb
from uuid import uuid4

db = conectar_keydb()

def agregar_libro():
    libro_id = str(uuid4())
    libro = {
        "id": libro_id,
        "titulo": input("Título: ").strip(),
        "autor": input("Autor: ").strip(),
        "genero": input("Género: ").strip(),
        "estado": input("Estado (leído/pendiente): ").strip()
    }

    if not all(libro.values()):
        print("Error: Todos los campos son obligatorios")
        return

    db.set(f"libro:{libro_id}", json.dumps(libro))
    print("Libro agregado correctamente")

def listar_libros():
    claves = db.scan_iter("libro:*")
    encontrados = False

    for clave in claves:
        libro = json.loads(db.get(clave))
        print(f"{libro['id']} | {libro['titulo']} | {libro['autor']} | {libro['genero']} | {libro['estado']}")
        encontrados = True

    if not encontrados:
        print("No hay libros registrados")

def buscar_libro():
    criterio = input("Buscar por (titulo/autor/genero): ").strip()
    valor = input("Valor: ").strip().lower()

    resultados = 0
    for clave in db.scan_iter("libro:*"):
        libro = json.loads(db.get(clave))
        if valor in libro.get(criterio, "").lower():
            print(f"{libro['id']} | {libro['titulo']} | {libro['autor']} | {libro['genero']} | {libro['estado']}")
            resultados += 1

    if resultados == 0:
        print("No se encontraron resultados")

def actualizar_libro():
    libro_id = input("ID del libro: ").strip()
    clave = f"libro:{libro_id}"

    if not db.exists(clave):
        print("Libro no encontrado")
        return

    libro = json.loads(db.get(clave))
    campo = input("Campo a actualizar (titulo/autor/genero/estado): ").strip()
    nuevo_valor = input("Nuevo valor: ").strip()

    if campo not in libro:
        print("Campo inválido")
        return

    libro[campo] = nuevo_valor
    db.set(clave, json.dumps(libro))
    print("Libro actualizado correctamente")

def eliminar_libro():
    libro_id = input("ID del libro a eliminar: ").strip()
    eliminado = db.delete(f"libro:{libro_id}")

    if eliminado == 0:
        print("Libro no encontrado")
    else:
        print("Libro eliminado correctamente")

def menu():
    while True:
        print("\n--- Biblioteca con KeyDB ---")
        print("1. Agregar libro")
        print("2. Listar libros")
        print("3. Buscar libro")
        print("4. Actualizar libro")
        print("5. Eliminar libro")
        print("6. Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            agregar_libro()
        elif opcion == "2":
            listar_libros()
        elif opcion == "3":
            buscar_libro()
        elif opcion == "4":
            actualizar_libro()
        elif opcion == "5":
            eliminar_libro()
        elif opcion == "6":
            print("Programa finalizado")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    menu()
