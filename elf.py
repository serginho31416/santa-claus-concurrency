# Estoy guardando dos contadores: el de elfos que aún no han terminado su trabajo
# (elves_still_working_count) y el de elfos que aún necesitarán ayuda
# (elves_still_to_ask_for_help_count), que no tienen por qué coincidir
# (cada elfo puede seguir trabajando solo después de recibir toda la ayuda
# que necesite). En mi interpretación del enunciado, los elfos despiertan
# a Santa cuando todos los que aún necesitan alguna ayuda están ya pidiéndola.


from random import random, randint
from threading import Thread
from time import sleep
from shared_data import SharedData


class Elf(Thread):
    def __init__(self, sh_data: SharedData, elf_id: int) -> None:
        super().__init__()
        self.sh_data = sh_data
        self.elf_id = elf_id

    def run(self) -> None:
        number_of_helps = randint(1, 3)
        for _ in range(number_of_helps):
            sleep(random())  # trabaja solo hasta que necesita ayuda
            print(f"Elf {self.elf_id} needs help.\n", end="")
            self.sh_data.elf_turnstile.acquire()
            self.sh_data.mutex.acquire()
            self.sh_data.elves_waiting_for_help_count += 1
            elves_needed = min(self.sh_data.NUM_ELVES_TO_WAKE_SANTA,
                               self.sh_data.elves_still_to_ask_for_help_count)
            if self.sh_data.elves_waiting_for_help_count >= elves_needed:
                self.sh_data.mutex.release()
                self.sh_data.santa_must_wake_sem.release()
            else:
                self.sh_data.mutex.release()
                self.sh_data.elf_turnstile.release()  # otro elfo puede entrar

            self.sh_data.elves_were_helped_sem.acquire()  # espera el aviso de Santa
            print(f"Elf {self.elf_id} has been helped.\n", end="")

            self.sh_data.mutex.acquire()
            self.sh_data.elves_waiting_for_help_count -= 1
            if self.sh_data.elves_waiting_for_help_count == 0:
                self.sh_data.elf_turnstile.release()  # deja que entre el primero de otro grupo
            self.sh_data.mutex.release()

        self.sh_data.mutex.acquire()
        self.sh_data.elves_still_to_ask_for_help_count -= 1
        self.sh_data.mutex.release()

        sleep(random())  # trabaja solo después de la última ayuda que necesita

        self.sh_data.mutex.acquire()
        self.sh_data.elves_still_working_count -= 1
        if self.sh_data.elves_still_working_count == 0:
            self.sh_data.santa_must_wake_sem.release()  # avisan a Santa de que han acabado
        self.sh_data.mutex.release()
        print(f"Elf {self.elf_id} is done.\n", end="")
