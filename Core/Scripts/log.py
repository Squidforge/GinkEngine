import sys
from datetime import date
from datetime import datetime

today = datetime.now()

date_ = today.strftime("%B-%d-%Y")  # Example: January 19, 2025

time_ = today.strftime("%Y-%m-%d : %H-%M-%S")

def log_startup():
    print("Starting GinkEngine...")

    with open(f"../../../Logs/{date_}.log", "a") as file:
        file.write(f"\nGinkengine was started - {time_}")

def log_exit():
    print("Exiting GinkEngine...")

    with open(f"../../../Logs/{date_}.log", "a") as file:
        file.write(f"\nGinkEngine was exited - {time_} \n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        func_name = sys.argv[1]

        if func_name in globals():
            globals()[func_name]() 
        else:
            print(f"Function '{func_name}' not found!")
    else:
        print("No function name provided!")