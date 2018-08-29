import socket
import ressources.calc as calc
from ressources.controller import Controller
from pigpio import pi

rasp_pi_ip = '192.168.178.29'
rasp_pi = pi(rasp_pi_ip)

# Motor 1 Pins
in1 = 12  # IN1
in2 = 16  # IN2
in3 = 20  # IN3
in4 = 21  # IN4
motor1_pins = [in1, in2, in3, in4]
controller1 = Controller(motor1_pins)

# Test: move motor by 90 degrees
# end_pos = controller1.get_end_pos(90)
# controller1.go_to_goal(end_pos)

# Motor 2 Pins
in2_1 = 18  # IN1
in2_2 = 17  # IN2
in2_3 = 27  # IN3
in2_4 = 22  # IN4
motor2_pins = [in2_1, in2_2, in2_3, in2_4]
controller2 = Controller(motor2_pins)

# 49°29'11.8"N 6°02'04.8"E
our_lat = 49.486617
our_lon = 6.034665

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(rasp_pi_ip)
port = 1337
address = (ip, port)
client.connect(address)

while True:
    msg_data = client.recv(1024)
    msg = msg_data.decode('utf-8')
    split_msg = msg.split(',')
    # print('tracking flight: ' + msg)
    if len(split_msg) > 15 and split_msg[11] != '' and split_msg[14] != '' and split_msg[15] != '' and len(split_msg) < 23:
        plane_alt = int(split_msg[11])
        plane_lat = float(split_msg[14])
        plane_lon = float(split_msg[15])
        print('flight-hex: ' + split_msg[4])
        print('alt: ' + split_msg[11])
        print('lat: ' + split_msg[14])
        print('lon: ' + split_msg[15])

        angle = 360 - calc.calc_angle(our_lat, our_lon, plane_lat, plane_lon)
        end_pos = controller1.get_end_pos(angle)
        controller1.go_to_goal(end_pos)

        our_alt = 0
        plane_alt = calc.feet_to_meter(plane_alt)
        angle = calc.calc_vertical_angle(our_lat, our_lon, our_alt, plane_lat, plane_lon, plane_alt)
        print('Altitude:' + str(plane_alt))
        print('Angle: ' + str(angle))
        end_pos = controller2.get_end_pos(angle)
        controller2.go_to_goal(end_pos)


# # 49°29'11.8"N 6°02'04.8"E
# our_lat = 49.486617
# our_lon = 6.034665
#
# # 49°28'59.0"N 6°05'22.0"E
# # 49.483049, 6.089437
# plane_lat = 49.483049
# plane_lon = 6.089437
#
# # 46°11'46.7"N 6°07'21.1"E
# plane_lat = 46.196295
# plane_lon = 6.122516
#
# print(str(ressources.calc.calc_angle(our_lat, our_lon, plane_lat, plane_lon)))
# print(str(ressources.calc.calc_angle(plane_lat, plane_lon, our_lat, our_lon)))



