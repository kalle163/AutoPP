from Classes.Visualisationfile import *
listofproperties=["rgb","hsv","grey","circularity","area","convexity","inertiaratio"]
line= "  <rgb min=255,255,255 max=255,255,255/>"
objectactive=True
if line.find("#")<0 and line.find("<")>=0 and line.find(">")>=0:
    if objectactive and not line=="</BloobObjects>":
        line=line.replace(">","")
        line=line.replace("<","")
        line=line.replace("/","")
        splits=line.split()
        if splits[0] in listofproperties:
            for i in range(1,len(splits)):
                subsplit=splits[i].split("=")
                print(subsplit[0]+splits[0],subsplit[1])
                
        else:
            print("No "+splits[0]+" Property defined for BlobObjects. Property musst be "+str(listofproperties))

MyPanelApp().run()

