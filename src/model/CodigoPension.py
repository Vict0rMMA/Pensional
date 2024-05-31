# Definición de Excepciones Personalizadas

class SalarioNoNumerico(Exception):
    def __init__(self):
        super().__init__("El salario debe ser numérico, ingrese un salario válido.")


class EdadTipoIncorrecto(Exception):
    def __init__(self):
        super().__init__("La edad debe ser un entero, ingrese una edad válida.")


class SemanasLaboradasTipoIncorrecto(Exception):
    def __init__(self):
        super().__init__("Las semanas laboradas deben ser numéricas.")


class TasaAdministracionTipoIncorrecto(Exception):
    def __init__(self):
        super().__init__("La tasa de administración debe ser numérica, ingrese una tasa válida.")


class RentabilidadFondoInvalida(Exception):
    def __init__(self):
        super().__init__("La rentabilidad de fondo debe estar entre 0 y 1.")


class SemanasLaboradasNegativas(Exception):
    def __init__(self):
        super().__init__("Las semanas laboradas tienen que ser positivas.")


class EdadNegativa(Exception):
    def __init__(self):
        super().__init__("La edad ingresada es negativa, ingrese una edad válida.")


class SalarioNegativo(Exception):
    def __init__(self):
        super().__init__("El salario debe ser mayor a 0, ingrese un salario válido.")


class SexoTipoIncorrecto(Exception):
    def __init__(self):
        super().__init__("El sexo debe ser un string, no un número. Debe ser 'masculino' o 'femenino'.")


class EstadoCivilTipoIncorrecto(Exception):
    def __init__(self):
        super().__init__("El estado civil debe ser 'soltero' o 'casado', no un número.")


class SexoNoPermitido(Exception):
    def __init__(self):
        super().__init__("El sexo debe ser 'masculino' o 'femenino'.")


class EstadoCivilNoPermitido(Exception):
    def __init__(self):
        super().__init__("El estado civil debe ser 'casado' o 'soltero'.")


class EsperanzaVidaTipoIncorrecto(Exception):
    def __init__(self):
        super().__init__("La esperanza de vida debe ser numérica.")


class AhorroPensionalTipoIncorrecto(Exception):
    def __init__(self):
        super().__init__("El ahorro pensional esperado debe ser int o float.")


class EdadMayorA90(Exception):
    def __init__(self):
        super().__init__("La edad debe estar entre 1-90, ingrese una edad válida.")


class EdadMayorAEsperanzaDeVida(Exception):
    def __init__(self):
        super().__init__("La edad no puede ser mayor a la esperanza de vida.")


class EsperanzaVidaNegativa(Exception):
    def __init__(self):
        super().__init__("La esperanza de vida debe ser mayor a 0.")


# Definición de la clase CalculadoraPensional

class CalculadoraPensional:
    def __init__(self):
        pass

    def validaciones_ahorro_pensional(self, edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion):
        """
        Valida los argumentos para el cálculo del ahorro pensional.

        :param edad: Edad del trabajador, debe ser un entero positivo.
        :param salario: Salario del trabajador, debe ser un número positivo.
        :param semanas_laboradas: Semanas laboradas por el trabajador, debe ser un número positivo.
        :param rentabilidad_fondo: Rentabilidad del fondo, debe ser un número entre 0 y 1.
        :param tasa_administracion: Tasa de administración, debe ser un número.
        """

        if not isinstance(salario, (int, float)):
            raise SalarioNoNumerico()

        if not isinstance(edad, int):
            raise EdadTipoIncorrecto()

        if not isinstance(semanas_laboradas, (int, float)):
            raise SemanasLaboradasTipoIncorrecto()

        if not isinstance(tasa_administracion, (int, float)):
            raise TasaAdministracionTipoIncorrecto()

        if not (0 < rentabilidad_fondo < 1):
            raise RentabilidadFondoInvalida()

        if semanas_laboradas < 0:
            raise SemanasLaboradasNegativas()

        if edad <= 0:
            raise EdadNegativa()

        if salario <= 0:
            raise SalarioNegativo()

    def validaciones_calculo_pension(self, edad, ahorro_pensional_esperado, sexo, estado_civil, esperanza_vida):
        """
        Valida los argumentos para el cálculo de la pensión.

        :param edad: Edad del trabajador, debe ser un entero positivo.
        :param ahorro_pensional_esperado: Ahorro pensional esperado, debe ser un número positivo.
        :param sexo: Sexo del trabajador, debe ser 'masculino' o 'femenino'.
        :param estado_civil: Estado civil del trabajador, debe ser 'soltero' o 'casado'.
        :param esperanza_vida: Esperanza de vida del trabajador, debe ser un número positivo.
        """

        if not isinstance(sexo, str):
            raise SexoTipoIncorrecto()

        if not isinstance(estado_civil, str):
            raise EstadoCivilTipoIncorrecto()

        if not isinstance(edad, int):
            raise EdadTipoIncorrecto()

        if sexo.lower() not in ['masculino', 'femenino']:
            raise SexoNoPermitido()

        if estado_civil not in ['casado', 'soltero']:
            raise EstadoCivilNoPermitido()

        if not isinstance(esperanza_vida, (int, float)):
            raise EsperanzaVidaTipoIncorrecto()

        if not isinstance(ahorro_pensional_esperado, (int, float)):
            raise AhorroPensionalTipoIncorrecto()

        if edad < 0:
            raise EdadNegativa()

        if edad > 90:
            raise EdadMayorA90()

        if esperanza_vida <= 0:
            raise EsperanzaVidaNegativa()

        if edad >= esperanza_vida:
            raise EdadMayorAEsperanzaDeVida()

    def calculo_ahorro_pensional(self, edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion):
        """
        Calcula el ahorro pensional esperado.

        :param edad: Edad del trabajador.
        :param salario: Salario del trabajador.
        :param semanas_laboradas: Semanas laboradas por el trabajador.
        :param rentabilidad_fondo: Rentabilidad del fondo.
        :param tasa_administracion: Tasa de administración.
        :return: Ahorro pensional esperado.
        """
        self.validaciones_ahorro_pensional(edad, salario, semanas_laboradas, rentabilidad_fondo, tasa_administracion)

        # Cálculo de los aportes mensuales
        aportes_mensuales = salario * 0.12

        # Cálculo del ahorro pensional esperado
        ahorro_pensional_esperado = aportes_mensuales * semanas_laboradas * rentabilidad_fondo * (
                    1 - tasa_administracion)
        return ahorro_pensional_esperado

    def calculo_pension(self, edad, ahorro_pensional_esperado, sexo, estado_civil, esperanza_vida):
        """
        Calcula la pensión esperada.

        :param edad: Edad del trabajador.
        :param ahorro_pensional_esperado: Ahorro pensional esperado.
        :param sexo: Sexo del trabajador.
        :param estado_civil: Estado civil del trabajador.
        :param esperanza_vida: Esperanza de vida del trabajador.
        :return: Pensión esperada.
        """
        self.validaciones_calculo_pension(edad, ahorro_pensional_esperado, sexo, estado_civil, esperanza_vida)

        # Determinación del factor de sexo y estado civil
        factor_sexo = 0
        if sexo == 'masculino':
            if estado_civil == 'soltero':
                factor_sexo = 0.06
            elif estado_civil == 'casado':
                factor_sexo = 0.08
        elif sexo == 'femenino':
            if estado_civil == 'soltero':
                factor_sexo = 0.07
            elif estado_civil == 'casado':
                factor_sexo = 0.09

        # Cálculo de la pensión esperada
        pension_esperada = ahorro_pensional_esperado * (1 + factor_sexo) * (edad / (esperanza_vida - edad))
        return pension_esperada
