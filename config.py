excluded = []
for n in range(1, 12):
    if n < 10:
        excluded.append("Mond_00" + str(n) + ".CR2")
    else:
        excluded.append("Mond_0" + str(n) + ".CR2")
        
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

for element in custom:
    if element < 10:
        excluded.append("Mond_00" + str(element) + ".CR2")
    elif element < 100:
        excluded.append("Mond_0" + str(element) + ".CR2")
    else:
        excluded.append("Mond_" + str(element) + ".CR2")
