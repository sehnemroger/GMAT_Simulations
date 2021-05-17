# Running an incredible amount of simullations in GMAT with it's API.
# Runs the simulations in script files for every combination of the 
# gravitational Harmonics.
#
# Roger M. Sehnem 2021


from load_gmat import * #import gmat API
import pathlib
import time

## Mounting the runs
maxDegree = 3
maxOrder = 3
maxComps = 5

## Path to here
path2here = str(pathlib.Path(__file__).parent.absolute()) # get full path of this script in a string

## original strings to be changed in .script file
degreeStr = "InternalODEModel.GravityField.Earth.Degree = 1;" 
orderStr = "InternalODEModel.GravityField.Earth.Order = 1;"
reportStr = "ReportFile1.txt"

tic = time.time()
for comp in range(1, maxComps + 1): # Actual computer 
    ## Main script
    path2Script = "comp" + str(comp) + "/Order11.script" # This is a relative path
    with open(path2Script,"r") as f:
        mScript = f.read() # Load main script

    ## Changes to be done on the script
    for nDegree in range(2, maxDegree + 1): # Degree of the spherical harmonics
        for nOrder in range(0, nDegree + 1): # Order of the spherical harmonics
            ## Make necessary changes to the script
            # new changed strings in .script file
            nDegreeStr = "InternalODEModel.GravityField.Earth.Degree = " + str(nDegree) + ";"
            nOrderStr = "InternalODEModel.GravityField.Earth.Order = " + str(nOrder) + ";"
            path2out = "comp" + str(comp) + "/output"
            filename = "ReportFile" + "D" + str(nDegree) + "O" + str(nOrder) + ".txt"
            nReportStr = path2here + "/" + path2out + "/" + filename

            # Make changes
            script = mScript.replace(degreeStr,nDegreeStr).replace(orderStr,nOrderStr).replace(reportStr,nReportStr)

            # save changes in temp script (overwrigth any existing temp.script)
            with open('temp.script',"w") as f:
                f.write(script)

            ## Load current script
            t = gmat.LoadScript('temp.script')
            #print(t) # true if script loads successfully

            ## Uncoment this line to generate scripts that are being run
            #gmat.SaveScript(nReportStr[:-4] + ".script")

            ## Runs gmat script
            t = gmat.RunScript()
            #print(t) # true if script runs successfully
print(time.time() - tic)