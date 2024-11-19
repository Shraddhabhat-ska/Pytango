#!/bin/bash

echo "running FrontEnd device server"
python3.10 FE/fe_server.py inst1 &


echo "Running Servo Device Server"
python3.10 servo/servo_server.py inst1 &

echo "Running Dish Device Server"
python3.10 Dish/dish_server.py inst1 &

echo "Running Subarray Device Server"
python3.10 Subarray/subarray_server.py inst1 &


echo "Running Central controller Device Server"
python3.10 Central_controller/central_server.py inst1

echo "All Server Started"
echo "To stop the server End the process manually in System monitor"
