# Esto es para ejecutar mi solución al problema de Santa Claus.


from random import shuffle
from shared_data import SharedData
from santa import Santa
from elf import Elf
from reindeer import Reindeer


if __name__ == "__main__":
    sh_data = SharedData()

    santa = Santa(sh_data)
    reindeer = [Reindeer(sh_data, i)
                for i in range(sh_data.NUM_REINDEER)]  # cada reno tiene un identificador
    elves = [Elf(sh_data, i)
             for i in range(sh_data.NUM_ELVES)]  # cada elfo tiene un identificador

    # para conseguir una puesta en marcha distinta en cada ejecución
    all_threads = reindeer + elves + [santa]
    shuffle(all_threads)
    for t in all_threads:
        t.start()

    # los join no son necesarios (tampoco molestarían)
