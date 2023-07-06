# @Author: Kyle Billings <kbillings>
# @Date:   2021-02-09T22:12:21-05:00
# @Email:  krb0073@mix.wvu.edu
# @Filename: TF_constraint.py
# @Last modified by:   kbillings
# @Last modified time: 2021-02-09T23:03:57-05:00
import loos
import loos.pyloos
import sys
import shutil
sys.path.append('/users/krb0073/EQ_run')
#sys.path.append('/media/bak12/Analysis/RUN_EQ_PYTHON/')
from NAMD_Kyle import *
psf=sys.argv[1]
pdb = sys.argv[2]
param_file=None
box=loos.GCoord(0.,0.,0.)
command=None
end_pdb=None

loos_obj = NAMD_KB(psf,pdb,end_pdb,param_file,box,command)
print(loos_obj.construct_constraints())

# making the constraint pdb
system = loos.createSystem(psf)
loos_obj.write_restraintfile("./",system,'backbone',spring=20)
