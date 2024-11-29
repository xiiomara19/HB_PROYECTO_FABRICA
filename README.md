# HB PROYECTO

## Descripción

Este proyecto tiene como objetivo maximizar el número de máquinas operativas en una fábrica con 20 puestos de trabajo, garantizando que la asignación de trabajadores sea óptima incluso en caso de ausencias. La redistribución se basa en las prioridades de las máquinas, el nivel de conocimiento y las capacidades de los trabajadores.

---

## PEAS (Performance Measure, Environment, Actions, Sensors)

### Performance Measure (Métrica de Rendimiento)
- **Objetivo principal**: Maximizar el número de máquinas operativas.
- **Objetivo secundario**: Asignar trabajadores con el mayor nivel de conocimiento (3 o 4) a los puestos prioritarios.

### Environment (Entorno)
- Fábrica con 20 puestos de trabajo.
- Turnos de trabajadores con posibles ausencias.
- Información disponible:
  - Prioridades de las máquinas.
  - Nivel de conocimiento de los trabajadores.
  - Composición de equipos de trabajo.

### Actions (Acciones)
1. **Asignar trabajadores**: 
   - Según experiencia, conocimiento y prioridad del puesto.
2. **Redistribuir en caso de ausencias**: 
   - Priorizando las máquinas críticas.
3. **Asignar refuerzos**:
   - Trabajadores excedentes se asignarán a máquinas prioritarias (excepto CA4, CA5 y tractor).

### Sensors (Sensores)
- Datos de asistencia y ausencias de trabajadores (entrada manual o sistema automatizado).
- Prioridades de las máquinas (archivo de Excel).
- Matriz de polivalencia de los trabajadores (archivo de Excel).
- Prioridades individuales de los trabajadores para las máquinas (archivo de Excel).

---

## Contexto del Problema

En la fábrica, los 20 puestos de trabajo requieren supervisión y/o ayuda humana. Cada puesto tiene requisitos específicos en términos de experiencia y cantidad de trabajadores. El desafío surge cuando faltan uno o más trabajadores en un turno, lo que requiere una redistribución óptima para mantener la máxima cantidad de máquinas operativas.

---

## Datos

### Datos de Entrada (INPUT)
- **Turno y ausencias**: 
  - Identificación del equipo que trabaja y de los trabajadores ausentes (introducido manualmente).
- **Prioridades de las máquinas**: 
  - Archivo de Excel con valores del 1 (máxima prioridad) al 6 (mínima prioridad).
- **Prioridades y conocimientos de los trabajadores**:
  - Matriz en Excel con valores de prioridad (0, 1, 2) y niveles de conocimiento (1-4).

### Datos de Salida (OUTPUT)
- **Distribución de trabajadores**: 
  - Archivo XML con la asignación de trabajadores por puesto.

---

## Algoritmo de Solución

### Estrategia Inicial
- Asignar trabajadores de nivel 3 y 4 a los puestos principales de máquinas críticas.
- Cobertura inicial de las máquinas más prioritarias.

### Uso de Hill-Climbing
- **Descripción de vecinos**:
  - Redistribución de trabajadores para cubrir puestos críticos.
  - Intercambio de trabajadores para mejorar la asignación.
  - Inclusión de trabajadores adicionales en máquinas prioritarias.
- **Función de evaluación**:
  - Maximizar el número de máquinas operativas.
  - Priorizar máquinas críticas.
  - Asignar trabajadores con mayor conocimiento a puestos clave.

---

## Tareas y Cronograma

### Sprint 1 (Deadline: 29/11)
1. Análisis y preparación de datos:
   - Recopilación de matrices de polivalencia y prioridades.
   - Estandarización de datos.
2. Definición de heurísticas y objetivos:
   - Establecer métrica de rendimiento.
   - Priorizar máquinas críticas.
3. Desarrollo inicial:
   - Implementación de asignación inicial y salida en formato XML.
4. Pruebas iniciales:
   - Validación con escenarios de turnos completos.

### Sprint 2 (Deadline: 14/01)
1. Refinamiento:
   - Establecer criterios para asignar trabajadores excedentes.
   - Simulación de escenarios con ausencias y excedentes.
2. Optimización:
   - Implementar mejoras en la asignación.
3. Documentación:
   - Redactar manual de usuario y documentación técnica.
   - Informe de resultados y entrega del proyecto.


