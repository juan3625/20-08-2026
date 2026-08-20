# Reservation Testing Lab - Pruebas de Software Módulo II

Este repositorio contiene la implementación y la suite de pruebas unitarias para un sistema de gestión de reservas de asesoría, soporte y demostración, desarrollado en Python con **Pytest**.

## Objetivo del Miniproyecto
Validar y comprobar de forma aislada las reglas de negocio de la lógica del dominio de reservas sin requerir la ejecución de un servidor HTTP (FastAPI/Uvicorn) ni una base de datos real.

## Reglas de Negocio Verificadas
- **RN-01**: El nombre del cliente debe tener al menos 3 caracteres útiles (después del trim).
- **RN-02**: Servicios permitidos: `asesoria`, `soporte`, `demostracion`.
- **RN-03**: Duración permitida única de `30` o `60` minutos.
- **RN-04**: No se permiten reservas en fechas pasadas a la fecha de referencia.
- **RN-05**: Solo se permiten reservas de lunes a viernes.
- **RN-06**: El horario de atención inicia a las `08:00`.
- **RN-07**: La reserva debe finalizar como máximo a las `17:00`.
- **RN-08**: No pueden existir dos reservas en la misma fecha y hora.
- **RN-09**: Toda reserva válida se crea con estado `confirmed`.
- **RN-10**: Código de confirmación generado mediante inyección de dependencias.

## Requisitos Previos
- Python 3.12 o superior.

## Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd pruebas-de-software-fast-api

   python -m pytest -v

python -m venv .venv
.\.venv\Scripts\activate

si ocurre error 
source .venv/Scripts/activate

ejemplo              |
                     |
                     ese c edita
python -m pytest -k reservation -v