from datetime import datetime, timedelta
import holidays

def calcular_dias_liquidacion(fecha_inicio, fecha_fin, tipo_permiso):
    colombia_holidays = holidays.CO(years=fecha_inicio.year) | holidays.CO(years=fecha_fin.year)
    num_dias = 0
    current_date = fecha_inicio

    while current_date <= fecha_fin:
        if tipo_permiso == "Carga IEE":
            # Excluir domingos y festivos
            if current_date.weekday() != 6 and current_date not in colombia_holidays:
                num_dias += 1
        else:  # Para "VCC" u otros tipos de permiso, contar todos los días
            num_dias += 1
        current_date += timedelta(days=1)

    return num_dias