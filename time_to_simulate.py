# Running an incredible amount of simullations in GMAT with it's API.
# Runs the simulations in script files for every combination of the 
# gravitational Harmonics.
#
# Roger M. Sehnem 2021


## Mounting the runs
maxDegree = 360
maxOrder = 360
maxComps = 5

time35=23.60842490196228 # time to 35

aux = 0
for comp in range(1, maxComps + 1): # Actual computer 
    for nDegree in range(2, maxDegree + 1): # Degree of the spherical harmonics
        for nOrder in range(0, nDegree + 1): # Order of the spherical harmonics
            aux += 1
print(aux)
print(aux*time35/35) # total time