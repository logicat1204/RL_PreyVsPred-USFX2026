class Prey:
    def __init__(self, name):
        self.name = name
        self.hambre = 100
        self.estado = {"buscar_recurso": 1, "hambre": 2, "buscar_pareja": 3, "pred_cercano": 4}
        self.estado_actual = self.estado["buscar_recurso"]
        
    def __str__(self):
        return self.name + "(" + str(self.hambre) + ")"
    
def mover(self, environment, accion):
    # Obtener posiciones actuales
    preys = environment.PosPreys()
    # Asumiendo que esta presa está en la primera posición, pero idealmente se debería identificar por nombre o índice.
    # Como solo hay una presa, usamos preys[0]
    if not preys:
        return
    pos_actual = preys[0]  # (x, y) tuple

    if accion == "busca_comida":
        recursos = environment.PosRecursos()
        if not recursos:
            # No hay recursos, quizá moverse aleatorio o cambiar estado
            return
        
        # Calcular el recurso más cercano (distancia Manhattan)
        def distancia(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        
        recurso_cercano = min(recursos, key=lambda r: distancia(pos_actual, r))
        # Calcular dirección hacia el recurso
        dx = recurso_cercano[0] - pos_actual[0]
        dy = recurso_cercano[1] - pos_actual[1]
        
        # Movimiento de un paso (prioridad horizontal o vertical)
        if dx != 0:
            paso_x = 1 if dx > 0 else -1
            nueva_pos = (pos_actual[0] + paso_x, pos_actual[1])
        elif dy != 0:
            paso_y = 1 if dy > 0 else -1
            nueva_pos = (pos_actual[0], pos_actual[1] + paso_y)
        else:
            # Ya está en el recurso? Entonces no se mueve, o debería comer
            return
        
        # Verificar si la nueva posición es válida (libre o contiene recurso)
        espacios_libres = environment.FreeSpaces()  # lista de posiciones libres (sin entidades)
        # También permitir moverse a celdas con recursos (para poder comer)
        if nueva_pos in espacios_libres or nueva_pos in recursos:
            # Actualizar posición en el entorno
            # Asumiendo que environment tiene un método para mover la presa
            # Por ejemplo: environment.mover_presa(self, nueva_pos)
            # Como no está definido, podríamos hacer:
            # Reemplazar la posición en la lista de presas (no recomendado)
            # En su lugar, imprimimos o retornamos la nueva posición
            # Lo ideal es que el entorno maneje la actualización.
            # Por ahora, simulamos:
            print(f"Moviendo de {pos_actual} a {nueva_pos}")
            # Aquí llamar al método del entorno si existe
        else:
            # No hay camino directo, posiblemente implementar un BFS o moverse aleatorio
            pass

    elif accion == "busca_pareja":
        # Similar, buscar otra presa (pareja) más cercana
        pass
    elif accion == "huye":
        # Huir del depredador más cercano
        pass



    
    def comer(self, environment, objetivo):
        # Implementar lógica de alimentación para la presa
        pass

    def reproducir(self, environment):
        # Implementar lógica de reproducción para la presa
        pass

    def cambiar_estado(self, environment):
        # Implementar lógica de actuación basada en el estado actual
        if(self.hambre < 50):
            self.estado_actual = self.estado["buscar_recurso"]
        else:
            self.estado_actual = self.estado["buscar_pareja"]

    def actuar(self, environment):
        self.cambiar_estado(environment)
        if self.estado_actual == self.estado["buscar_recurso"]:
            self.mover(environment, "busca_comida")
        elif self.estado_actual == self.estado["buscar_pareja"]:
            self.mover(environment, "busca_pareja")
        elif self.hambre >= 50 and self.estado_actual == self.estado["buscar_pareja"]:
            self.mover(environment, "busca_pareja")
        elif self.estado_actual == self.estado["pred_cercano"]:
            self.mover(environment, "huye")
        

    
Prey1 = Prey("Prey1")
