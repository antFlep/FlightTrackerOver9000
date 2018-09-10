def get_parameter(value):
    config_file = open('./config.txt', 'r')
    lines = config_file.readlines()
    for line in lines:
        line = line.rstrip('\n\r')
        if line.startswith(value):
            return line.split('=')[1]


if __name__ == '__main__':
    print(get_parameter('ip'))