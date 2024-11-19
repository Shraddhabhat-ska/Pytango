from tango.server import run
import Dish_device

if __name__ == "__main__":
    run([Dish_device.DishDevice])
