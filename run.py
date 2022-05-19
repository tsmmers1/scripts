import rmsd

outputFile = 'aimd' # enter output file name here (ex. 'La-3')

traj = rmsd.Trajectory(ionID='Dy', elements=['O', 'N'], boxSize=10., framesForRMSD=1000, binSize=0.05, startFrame=1, endFrame=1000)
traj.getAtoms('aimd-pos-1.xyz') # input .xyz filename here
traj.getIonNum()
if (traj.ionNum > 1): # get user input if there is more than one of the ion
    traj.getWhichIon()
traj.getRDF()
traj.getDist()
traj.getMaxR()
traj.getCN()
traj.printRDF(outputFile)
#traj.checkWithUser() # comment this out if you don't want to be prompted about max and threshold values, for automated running, no need for "Y"
#traj.getThresholdAtoms()
#traj.getADF()
#traj.printADF(outputFile)
#traj.getIdealGeos()
#traj.getRMSDs()
#traj.printRMSDs(outputFile)
#traj.outputIdealGeometries('') # if there is a subfolder you would like to save to, enter it in the ''
