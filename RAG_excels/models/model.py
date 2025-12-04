# Archivo principal para inicializar y usar el agente Excel
# Este archivo ahora solo contiene el código de ejemplo para demostrar el uso

from models.agent import ExcelAgent

# Inicializar el agente
agent_instance = ExcelAgent()
agent_instance.initialize("tu_archivo.xlsx")

# Ejemplo de uso
print("=== EXPLORAR ===")
result1 = agent_instance.query("Muéstrame la estructura del Excel")
print(result1["messages"][-1].content)

print("\n=== BUSCAR ===")
result2 = agent_instance.query("¿Qué valor tiene la celda B5 de Ventas?")
print(result2["messages"][-1].content)

print("\n=== EDITAR (el agente pedirá confirmación) ===")
result3 = agent_instance.query("Cambia B5 de Ventas a 2500")
print(result3["messages"][-1].content)
