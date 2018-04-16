#
#
# A simple script to offset the gap values in a harmonic file
#
import codecs
from beamline.dcm_enrg import stringToFloatList

def offset_harmonic(harmonic_file,offset):
    fin = codecs.open(harmonic_file,"r","utf-8-sig")
    AA=fin.readlines()
    fin.close()
    for i in range(len(AA)-1):
        #print 'AA',AA[i]
        a,b,c,d = stringToFloatList(AA[i])
        print 'old',a
        a[2]=a[2]+offset
        newstr = "%f %f %f\n"%(a[0],a[1],a[2])
        print "new", newstr
        AA[i]= newstr
    fout = open(harmonic_file,"w")
    fout.writelines(AA)
    fout.close()

