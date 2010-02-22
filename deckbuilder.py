#!/usr/bin/env python

import xml.dom.minidom
import zipfile
import sys
import os

class DeckBuilder:
    
    def compile_directory(self, deckdir, outfile):
        jpegs = self.list_jpegs(deckdir)
        dom = xml.dom.minidom.Document()
        
        deck = dom.createElement("deck")
        dom.appendChild(deck)
        
        title = dom.createElement("title")
        title.appendChild(dom.createTextNode(deckdir))
        deck.appendChild(title)
        
        for j in jpegs:
            slide = dom.createElement("slide")
            layer = dom.createElement("layer")
            layer.appendChild(dom.createTextNode(j))
            slide.appendChild(layer)
            slide.setAttribute("name", j)
            deck.appendChild(slide)
            
        df = os.path.join(deckdir, "deck.xml")
        f = open(df, "w")
        dom.writexml(f)
        f.close()
        
        files = ["deck.xml"] + jpegs
        
        zf = zipfile.ZipFile(outfile, "w")
        for f in files:
            zf.write(os.path.join(deckdir, f), f)
        zf.close()
        
        print "Finished building %s" % outfile
        
        
    
    def list_jpegs(self, deckdir):
        files = os.listdir(deckdir)
        jpegs = []
        for f in files:
            if f[-4:] == ".jpg" or f[-4:] == ".png" or f[-4:] == ".svg":
                jpegs.append(f)
        jpegs.sort()
        if(len(jpegs) < 1):
            print "Sorry, I couldn't find any images from which to build a deck"
            sys.exit(1)
        print "Going to construct a deck from the following image files:"
        for i in range(len(jpegs)):
            print "  [%02d] %s" % (i+1, jpegs[i])
        return jpegs
        
        
        
    
if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print "To create a CPXO deck from a folder of JPEG images, type:"
        print "python deckbuilder.py <folder>"
        sys.exit(1)
    
    deckdir = sys.argv[1]
    if not os.path.isdir(deckdir):
        print "Cannot find directory %s" % deckdir
        sys.exit(1)
        
    db = DeckBuilder()
    db.compile_directory(deckdir, deckdir + ".cpxo")