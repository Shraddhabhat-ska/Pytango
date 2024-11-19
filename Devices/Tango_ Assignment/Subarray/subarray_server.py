import tango
from tango.server import run
from SubArray import SubArray

if __name__ == "__main__":
    run([SubArray])
