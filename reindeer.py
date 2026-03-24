from random import random
from threading import Thread
from time import sleep
from shared_data import SharedData


class Reindeer(Thread):
    def __init__(self, sh_data: SharedData, reindeer_id: int) -> None:
        super().__init__()
        self.sh_data = sh_data
        self.reindeer_id = reindeer_id

    def run(self) -> None:
        sleep(random())
        print(f"Reindeer {self.reindeer_id} is back from the tropics.\n", end="")
        self.sh_data.mutex.acquire()
        self.sh_data.reindeer_back_count += 1
        if self.sh_data.reindeer_back_count == self.sh_data.NUM_REINDEER:
            self.sh_data.santa_must_wake_sem.release()
        self.sh_data.mutex.release()
        self.sh_data.sleigh_is_ready_sem.acquire()  # espera el aviso de Santa
        print(f"Reindeer {self.reindeer_id} has been hitched.\n", end="")
