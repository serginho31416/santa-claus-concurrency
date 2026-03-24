# Un objeto SharedData contiene todos los datos que las hebras necesitan compartir.
# Su único objetivo es hacer más sencilla la compartición.
#
# Esto tiene el inconveniente de que todas las hebras reciben todos los datos,
# aunque no todas necesitan todos. Por ejemplo, los elfos no necesitan
# el contador de renos, pero lo reciben de todos modos. Todo lo que estoy compartiendo
# son datos sencillos, así que lo veo como un inconveniente poco importante.
#
# Usar el mismo mutex para todos los contadores es una elección cuestionable.
# Por ejemplo, esto hace imposible que los renos aumenten su contador
# al mismo tiempo que los elfos aumentan el suyo. Como los trozos de código
# que están bloqueadas por este mutex son muy pequeños y rápidos de ejecutar,
# no creo que sea un problema. Además, en algunos trozos de código accedemos
# a más de un contador, y tener sólo un mutex hace más fácil protegerlos todos.


from dataclasses import dataclass
from threading import Lock, Semaphore


@dataclass
class SharedData:
    NUM_ELVES_TO_WAKE_SANTA = 3
    NUM_REINDEER = 9
    NUM_ELVES = 4
    reindeer_back_count = 0
    elves_waiting_for_help_count = 0
    elves_still_working_count = NUM_ELVES  # cantidad de elfos que están aún trabajando
    elves_still_to_ask_for_help_count = NUM_ELVES  # cantidad de elfos que aún necesitarán ayuda
    mutex = Lock()  # para proteger los contadores anteriores
    santa_must_wake_sem = Semaphore(0)
    sleigh_is_ready_sem = Semaphore(0)  # Santa avisa a los renos de que están listos
    elves_were_helped_sem = Semaphore(0)  # Santa avisa a los elfos de que han sido ayudados
    elf_turnstile = Semaphore(1)


# Esto es equivalente a lo de arriba:
# NUM_ELVES_TO_WAKE_SANTA = 3
# NUM_REINDEER = 9
# NUM_ELVES = 4
#
# class SharedData:
#     def __init__(self) -> None:
#         self.reindeer_back_count = 0
#         etc.
