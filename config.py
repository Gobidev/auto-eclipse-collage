
#Specify images not to use
custom = [63,
          145,
          170,
          229,
          274,
          286,
          301,
          315,
          326,
          350,
          357,
          358,
          377,
          400,
          419,
          420,
          466,
          467,
          491,
          492,
          525]


def generate(index):
    global custom
    
    excluded = []
    
    for element in custom:
        if element < 10:
            excluded.append(index + "00" + str(element) + ".CR2")
        elif element < 100:
            excluded.append(index + "0" + str(element) + ".CR2")
        else:
            excluded.append(index + str(element) + ".CR2")

    return excluded
