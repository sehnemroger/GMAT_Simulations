# Running an incredible amount of simullations in GMAT with it's API.
# Runs the simulations in script files for every combination of the 
# gravitational Harmonics.
#
# Roger M. Sehnem 2021


from load_gmat import * #import gmat API
import pathlib
import time
import multiprocessing
from functools import partial

## Define function to run in parallel
def runScript(mScript,reportStr,orderStr,degreeStr,path2here,comp,nDegree):
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
        # temp script name (for parallel execution only use scripts with singular names)
        scriptName = nReportStr[:-4] + ".script"
        with open(scriptName,"w") as f:
            f.write(script)

        ## Load current script
        gmat.LoadScript(scriptName)

        ## Runs gmat script
        t = gmat.RunScript()

def main():
    ## Mounting the runs
    maxDegree = 8
    minComps = 1
    maxComps = 2

    ## Path to here
    path2here = str(pathlib.Path(__file__).parent.absolute()) # get full path of this script in a string

    ## original strings to be changed in .script file
    degreeStr = "InternalODEModel.GravityField.Earth.Degree = 1;" 
    orderStr = "InternalODEModel.GravityField.Earth.Order = 1;"
    reportStr = "ReportFile1.txt"

    tic = time.time()
    for comp in range(minComps, maxComps + 1): # Actual computer 
        ## Main script
        path2Script = "comp" + str(comp) + "/Order11.script" # This is a relative path
        with open(path2Script,"r") as f:
            mScript = f.read() # Load main script
        iterable = range(2, maxDegree + 1) # this is the iterable that is executed in parallel
        pool = multiprocessing.Pool(8) # number of threads to run in
        func = partial(runScript,mScript,reportStr,orderStr,degreeStr,path2here,comp) # func is a function of just nDegree
        pool.map_async(func, iterable) # divides workload
        pool.close()
        pool.join()

    print(time.time() - tic)

if __name__ == "__main__":
    main()