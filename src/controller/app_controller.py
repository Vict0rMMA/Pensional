import sys
import psycopg2
from contextlib import contextmanager
from src.model.User import Usuario
import secret_config

sys.path.append("C:/Users/ASUS/testCalculadora/Calculadora_Pensional-3")


class ControladorUsuarios:
    def __init__(self):
        self.database = secret_config.PGDATABASE
        self.user = secret_config.PGUSER
        self.password = secret_config.PGPASSWORD
        self.host = secret_config.PGHOST
        self.port = secret_config.PGPORT

    @contextmanager
    def obtener_cursor(self):
        """
        Crea un cursor de base de datos y garantiza su cierre adecuado.
        """
        connection = psycopg2.connect(database=self.database,
                                      user=self.user,
                                      password=self.password,
                                      host=self.host,
                                      port=self.port)
        cursor = connection.cursor()
        try:
            yield cursor
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()

    def crear_tablas(self):
        """
        Crea las tablas 'usuarios' y 'resultados_calculos' en la base de datos si no existen.
        """
        with self.obtener_cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    sexo TEXT NOT NULL,                              
                    edad INTEGER NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resultados_calculos (
                    id SERIAL PRIMARY KEY,
                    id_usuario INTEGER REFERENCES usuarios(id),
                    nombre_usuario TEXT NOT NULL,
                    tipo_calculo TEXT NOT NULL,
                    resultado NUMERIC NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

    def insertar_usuario(self, usuario):
        """
        Inserta un nuevo usuario en la tabla 'usuarios'.

        :param usuario: Objeto de tipo Usuario.
        """
        with self.obtener_cursor() as cursor:
            cursor.execute("""
                INSERT INTO usuarios (nombre, apellido, sexo, edad)
                VALUES (%s, %s, %s, %s)
            """, (usuario.nombre, usuario.apellido, usuario.sexo, usuario.edad))

    def insertar_resultado_calculo(self, id_usuario, tipo_calculo, resultado):
        """
        Inserta un nuevo resultado de cálculo en la tabla 'resultados_calculos'.

        :param id_usuario: ID del usuario asociado.
        :param tipo_calculo: Tipo de cálculo realizado.
        :param resultado: Resultado del cálculo.
        """
        usuario = self.obtener_usuario_por_id(id_usuario)
        nombre_usuario = f"{usuario.nombre} {usuario.apellido}"

        with self.obtener_cursor() as cursor:
            cursor.execute("""
                INSERT INTO resultados_calculos (id_usuario, nombre_usuario, tipo_calculo, resultado)
                VALUES (%s, %s, %s, %s)
            """, (id_usuario, nombre_usuario, tipo_calculo, resultado))

    def obtener_resultados_calculo(self, id_usuario):
        """
        Obtiene los resultados de cálculo de un usuario específico.

        :param id_usuario: ID del usuario.
        :return: Lista de resultados de cálculo.
        """
        usuario = self.obtener_usuario_por_id(id_usuario)
        with self.obtener_cursor() as cursor:
            cursor.execute("""
                SELECT nombre_usuario, tipo_calculo, resultado, fecha
                FROM resultados_calculos
                WHERE id_usuario = %s
            """, (id_usuario,))
            return cursor.fetchall()

    def eliminar_todos_usuarios(self):
        """
        Elimina todos los usuarios y sus resultados de cálculo asociados.
        """
        with self.obtener_cursor() as cursor:
            cursor.execute("DELETE FROM resultados_calculos WHERE id_usuario IN (SELECT id FROM usuarios)")
            cursor.execute("DELETE FROM usuarios")

    def obtener_usuarios(self):
        """
        Obtiene todos los usuarios de la tabla 'usuarios'.

        :return: Lista de objetos Usuario.
        """
        with self.obtener_cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios")
            usuarios = [Usuario(row[1], row[2], row[3], row[4], row[0]) for row in cursor.fetchall()]
            return usuarios

    def obtener_historial_calculos(self):
        """
        Obtiene el historial de todos los cálculos realizados.

        :return: Lista de tuplas con los resultados de cálculo.
        """
        with self.obtener_cursor() as cursor:
            cursor.execute("SELECT * FROM resultados_calculos")
            return cursor.fetchall()

    def obtener_usuario_por_id(self, id_usuario):
        """
        Obtiene un usuario específico por su ID.

        :param id_usuario: ID del usuario.
        :return: Objeto Usuario si existe.
        :raises ValueError: Si el usuario no existe.
        """
        with self.obtener_cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
            row = cursor.fetchone()
            if row:
                return Usuario(row[1], row[2], row[3], row[4], row[0])
            else:
                raise ValueError("El usuario con el ID especificado no existe.")

    def modificar_usuario(self, id_usuario, nombre, apellido, sexo, edad):
        """
        Modifica los datos de un usuario específico.

        :param id_usuario: ID del usuario.
        :param nombre: Nuevo nombre del usuario.
        :param apellido: Nuevo apellido del usuario.
        :param sexo: Nuevo sexo del usuario.
        :param edad: Nueva edad del usuario.
        :raises ValueError: Si el usuario no existe o si los datos no son válidos.
        """
        from src.view.console.consola_controlador import validate_nombre, validate_apellido, validate_sexo, \
            validate_edad

        usuario_existente = self.obtener_usuario_por_id(id_usuario)

        try:
            validate_nombre(nombre)
            validate_apellido(apellido)
            validate_sexo(sexo)
            validate_edad(edad)
        except ValueError as e:
            raise ValueError(f"Error al modificar usuario: {e}")

        with self.obtener_cursor() as cursor:
            cursor.execute("""
                UPDATE usuarios
                SET nombre = %s, apellido = %s, sexo = %s, edad = %s
                WHERE id = %s
            """, (nombre, apellido, sexo, edad, id_usuario))

    def eliminar_usuario(self, id_usuario):
        """
        Elimina un usuario específico y sus resultados de cálculo asociados.

        :param id_usuario: ID del usuario.
        :raises ValueError: Si el usuario no existe.
        """
        with self.obtener_cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id = %s", (id_usuario,))
            existe_usuario = cursor.fetchone()[0] > 0

            if existe_usuario:
                cursor.execute("DELETE FROM resultados_calculos WHERE id_usuario = %s", (id_usuario,))
                cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
            else:
                raise ValueError("El usuario con el ID especificado no existe.")

