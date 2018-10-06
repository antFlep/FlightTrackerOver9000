def get_parameter(par_name):
    """
    Extracts parameter values from our config file

    :param par_name: name of the parameter whose value we want to know
    :return: value of that parameter
    """
    config_file = open('./config.txt', 'r')
    lines = config_file.readlines()
    for line in lines:
        line = line.rstrip('\n\r')
        if line.startswith(par_name):
            return line.split('=')[1]
