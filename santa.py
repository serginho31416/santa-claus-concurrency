# Hay tres casos en que Santa puede ser despertado,
# y el mismo semáforo `santa_must_wake_sem` se usa para despertarlo en los tres casos.
# Así que, después de ser despertado, Santa debe comprobar qué ha ocurrido.
#
# 1. Hay `NUM_REINDEER` renos esperando (es decir, todos). Esta debe ser la primera condición
#    que se compruebe, para dar prioridad a los renos. Hay que comprobar si los renos
#    ya han sido enganchados, para evitar hacerlo de nuevo. Para eso uso la variable
#    `reindeer_hitched`.
# 2. Todos los elfos han terminado de trabajar. En mi implementación, Santa no conoce
#    de antemano cuántas ayudas necesitarán los elfos, así que espera que los elfos le
#    avisen de que han terminado. En este caso, Santa simplemente deja de trabajar
#    (sale de su bucle).
# 3. Hay elfos pidiendo ayuda. En este caso, Santa debe ayudarlos.
#
# Un detalle: si dos de los casos anteriores ocurren más o menos al mismo tiempo,
# habrá dos `release` para el semáforo `santa_must_wake_sem`. Santa entonces hace
# un `acquire` (despierta una vez), hace lo que deba, y luego hace el otro `acquire`
# (despierta otra vez). Incluso puede ocurrir que el primer `release`
# sea hecho por los elfos y el segundo, casi simultáneo, por los renos, y Santa,
# sin embargo, al despertar la primera vez, debe dar prioridad a los renos.


from time import sleep
from random import random
from threading import Thread
from shared_data import SharedData


class Santa(Thread):
    def __init__(self, sh_data: SharedData) -> None:
        super().__init__()
        self.sh_data = sh_data

    def run(self) -> None:
        reindeer_hitched = False
        while self.sh_data.elves_still_working_count > 0 or not reindeer_hitched:
            self.sh_data.santa_must_wake_sem.acquire()  # Santa duerme
            print("Santa is awake.\n", end="")

            self.sh_data.mutex.acquire()
            if (self.sh_data.reindeer_back_count == self.sh_data.NUM_REINDEER
                    and not reindeer_hitched):  # los renos han despertado a Santa
                self.sh_data.mutex.release()
                print("Santa is preparing the sleigh.\n", end="")
                sleep(random())  # tiempo que tarda Santa en preparar el trineo
                self.sh_data.sleigh_is_ready_sem.release(self.sh_data.NUM_REINDEER)
                # ^ Santa avisa a los renos de que están listos
                reindeer_hitched = True
            elif self.sh_data.elves_still_working_count == 0:
                # los elfos han despertado a Santa para decirle que han acabado todos
                self.sh_data.mutex.release()
            else:   # self.sh_data.elves_waiting_for_help_count >= elves_needed
                # los elfos han despertado a Santa porque necesitan ayuda
                elves_needed = min(self.sh_data.NUM_ELVES_TO_WAKE_SANTA,
                                   self.sh_data.elves_still_to_ask_for_help_count)
                self.sh_data.mutex.release()
                print("Santa is helping the elves.\n", end="")
                sleep(random())  # tiempo que tarda Santa en ayudar a los elfos
                self.sh_data.elves_were_helped_sem.release(elves_needed)
                # ^ Santa avisa a los elfos de que ha terminado de ayudarlos

        print("All toys are made and the sleigh is ready. Time to go.\n", end="")
