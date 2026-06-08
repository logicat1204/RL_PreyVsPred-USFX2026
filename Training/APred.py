class Pred:
    def __init__(self, name):
        self.name = name
        self.hambre = 100
        self.estado = {"buscar_presa": 1, "buscar_pareja": 2}
        self.estado_actual = self.estado["buscar_presa"]
    def __str__(self):
        return self.name + "(" + str(self.hambre) + ")"
    
    def mover(self, environment):
        # Implementar lógica de movimiento para el depredador
        pass

    def comer(self, environment):

        # Implementar lógica de alimentación para el depredador
        pass

    def reproducir(self, environment):
        # Implementar lógica de reproducción para el depredador
        pass

Pred1 = Pred("Pred1")
Pred1.estado_actual = Pred1.estado["buscar_presa"]
print(Pred1.estado_actual)