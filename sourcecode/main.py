# main.py
import glfw
from guis import show_gui
from physics import run
from queue import Queue

def main():
    parameter_queue = Queue()
    
    show_gui(parameter_queue)
    if not parameter_queue.empty():
        params = parameter_queue.get()
        

        run(params)

if __name__ == "__main__":
    main()
