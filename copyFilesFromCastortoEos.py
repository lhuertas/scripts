#! /usr/bin/env python

import sys
import optparse
from subprocess import Popen,PIPE
#from listFilesInCastor import listFilesInCastor
from CopyWatch import CopyWatch
#from ForwardAnalysis.Scripts.CopyWatch import CopyWatch


def listFilesInCastor(castor_dir,type,prefix):
    p1 = Popen(['nsls',castor_dir],stdout=PIPE)
    p2 = Popen(['grep',type],stdin=p1.stdout,stdout=PIPE)
    files = [item[:-1] for item in p2.stdout]
    p2.stdout.close()
    return files



def copyFilesFromCastortoEos(castor_dir,eos_dir,type,veto,prefix,suffix,enable):
    from subprocess import call
    files = listFilesInCastor(castor_dir,type,prefix)
    if suffix: files = [item + suffix for item in files]

    cpcmd = 'xrdcp'
    copy_prefix_castor = 'root://castorcms/'
    copy_prefix_eos = 'root://eoscms.cern.ch/'

    print "Copying from %s%s to %s%s" % (copy_prefix_castor,castor_dir,copy_prefix_eos,eos_dir) 
    copyList = []
    for item in files:
        #cmd = ['rfcp',item,output_dir] 
        cmd = 'nice xrdcp %s%s%s %s%s%s' % (copy_prefix_castor,castor_dir,item,copy_prefix_eos,eos_dir,item) 
        #print "..." + item
        print "..." + cmd
        if enable:
	    #retcode = call(cmd)
	    #if retcode != 0: raise RuntimeError,'Error in copying file %s to directory %s' % (item,output_dir)
            copyList.append( CopyWatch(cmd) )
            copyList[-1].start()

    for item in copyList: item.join() 


if __name__ == '__main__':
    parser = optparse.OptionParser(usage="usage: %prog [options]")
    parser.add_option("-o","--out", dest="out", metavar="OUT", help="output directory")
    parser.add_option("-d","--dir", dest="dir", metavar="DIR", help="copy files from DIR")
    parser.add_option("-t","--type", dest="type", default="root", metavar="TYPE", help="select only files with substring TYPE (Default: 'root')")
    parser.add_option("-v","--veto", dest="veto", default="", metavar="VETO", help="select only files without substring VETO")
    parser.add_option("-p","--prefix", dest="prefix", default="", metavar="PREFIX", help="prepend PREFIX to file path")
    parser.add_option("-s","--suffix", dest="suffix", default="", metavar="SUFFIX", help="append SUFFIX to file path") 
    parser.add_option("--no_exec", dest="enable", action="store_false", default=True, help="files will not be copied")

    (input, args) = parser.parse_args()

    if not input.dir: parser.error('must set input directory')
    if not input.out: parser.error('must set output directory')

    copyFilesFromCastortoEos(castor_dir  = input.dir,
                             eos_dir  = input.out,
                             type        = input.type,
                             veto        = input.veto,
                             prefix      = input.prefix,
                             suffix      = input.suffix,
                             enable      = input.enable)

    print "========================="
    print "----> Transfer completed."
    print "========================="

    sys.exit(0)
