#! /usr/bin/env python

import sys
import optparse
from subprocess import Popen,PIPE
#from listFilesInCastor import listFilesInCastor
from CopyWatch import CopyWatch
#from ForwardAnalysis.Scripts.CopyWatch import CopyWatch
lscmd = 'lcg-ls -bD srmv2'


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="usage: %prog [options]")
    parser.add_option("-s","--site", dest="site", metavar="SITE", help="site name")
    parser.add_option("-p","--port", dest="port", type="int", default=8443, metavar="PORT", help="SRM port (Default: 8443)")
    parser.add_option("-t","--type", dest="type", default="root", metavar="TYPE", help="select only files with substring TYPE (Default: 'root')")
    parser.add_option("--srm_str", dest="srmstr", default="/srm/v2/server?SFN=", metavar="SRM", help="SRM string (Default: '/srm/v2/server?SFN=')")
    parser.add_option("-o","--out", dest="out", metavar="OUT", help="output directory")
    parser.add_option("-d","--dir", dest="dir", metavar="DIR", help="copy files from DIR")
    parser.add_option("-v","--veto", dest="veto", default="", metavar="VETO", help="select only files without substring VETO")
    parser.add_option("--no_exec", dest="enable", action="store_false", default=True, help="files will not be copied")

    (input, args) = parser.parse_args()

    if not input.site: parser.error('must set site name')
#    if len(args) != 2: parser.error('exactly two arguments required')



from subprocess import call
srm_string = input.srmstr
storage_name = input.site
storage_port = input.port
storage_path = args[0]
outdir = args[0]
type = input.type
endpoint = 'srm://' + storage_name + ':' + str(storage_port) + srm_string
fullpath = endpoint + storage_path
lscmd = '%s "%s"' % (lscmd,fullpath)
print lscmd
p1 = Popen(lscmd,shell=True,stdout=PIPE)
files = [item.rstrip().split("/")[-1] for item in p1.stdout if item.find(type) != -1]

cpcmd = 'xrdcp'
copy_prefix_eos = 'root://eoscms.cern.ch/'
eos_dir = input.out

print "Copying from %s%s to %s%s" % (cpcmd,fullpath,copy_prefix_eos,eos_dir) 
copyList = []
for item in files:
     #cmd = ['rfcp',item,output_dir] 
     cmd = 'gfal-copy %s%s %s%s%s' % (fullpath,item,copy_prefix_eos,eos_dir,item) 
     #print "..." + item
     print cmd
#     if enable:
	    #retcode = call(cmd)
	    #if retcode != 0: raise RuntimeError,'Error in copying file %s to directory %s' % (item,output_dir)
#*            copyList.append( CopyWatch(cmd) )
#            copyList[-1].start()

for item in copyList: item.join() 


print "========================="
print "----> Transfer completed."
print "========================="

sys.exit(0)
