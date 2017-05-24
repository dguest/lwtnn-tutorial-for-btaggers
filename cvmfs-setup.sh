export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
alias setupATLAS='source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh'

setupATLAS -q
localSetupROOT -q
lsetup "lcgenv -p LCG_88Py3 x86_64-slc6-gcc49-opt Python"
lsetup "lcgenv -p LCG_88Py3 x86_64-slc6-gcc49-opt pip"
lsetup "lcgenv -p LCG_88Py3 x86_64-slc6-gcc49-opt h5py"
lsetup "lcgenv -p LCG_88Py3 x86_64-slc6-gcc49-opt Boost"
lsetup "lcgenv -p LCG_88Py3 x86_64-slc6-gcc49-opt eigen"
