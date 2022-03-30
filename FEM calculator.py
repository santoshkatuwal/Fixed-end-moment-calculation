
#FEM calculator of Beam
#Unit syste: KN,m,rad
from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
import os
import win32ui
Orient=QtWidgets.QInputDialog.getText( None, 'Member Orientation', 'Enter H for horizontal V for vertical:')
orient=Orient[0]
if orient=="h" or orient=="H" or orient=="V" or orient=="v":
    Len=QtWidgets.QInputDialog.getText( None, 'Member Length', 'Enter member length in m:')
    l=float(Len[0])
    NP=QtWidgets.QInputDialog.getText( None, 'No. of point loads', 'Enter total numbers of point loads in the element:')
    np=int(NP[0])
    FRD=0
    BACK=0
    R_A=0
    R_B=0
    for i in range(0,np):
        P=QtWidgets.QInputDialog.getText( None, 'Load Entry', 'Data Entry for <<<P'+str(i+1)+'>>>\nEnter Load (P), Left distance(a), Right distance(b)\ne.g.: 10,2,3\nNote: Positive P for downward and right load')
        p=P[0]
        p=p.split(",")
        
        #FEM CALCULATION
        frd=-float(p[0])*float(p[1])*(float(p[2]))**2/(float(p[1])+float(p[2]))**2
        back=float(p[0])*float(p[1])**2*(float(p[2]))/(float(p[1])+float(p[2]))**2
        FRD=FRD+frd
        BACK=BACK+back
        
        #REACTION CALCULATION
        r_A=float(p[0])*float(p[2])/(float(p[1])+float(p[2]))
        r_B=float(p[0])*float(p[1])/(float(p[1])+float(p[2]))
        R_A=R_A+r_A
        R_B=R_B+r_B
    UDL=QtWidgets.QInputDialog.getText( None, 'UDL', 'Is UDL applied on the element ?\nType "yes" if applied.')
    if UDL[0]=="yes" or UDL[0]=="y":
        UDL_val=QtWidgets.QInputDialog.getText( None, 'UDL', 'Enter UDL value in kN/m\n(Only valid for full length UDL)\n**Note: Positive sign for downward and right loads.')
        #FEM Calculation
        frd=-(float(UDL_val[0])*l**2)/12
        back=-frd
        FRD=FRD+frd
        BACK=BACK+back
        #Reaction Calculation
        r_A=float(UDL_val[0])*l/2
        r_B=float(UDL_val[0])*l/2
        R_A=R_A+r_A
        R_B=R_B+r_B        
        
    elif UDL[0]=="no" or UDL[0]=="n":
        pass
    else:
        pass
        
    offset=l/1000
    max_off=l+offset
    if orient=="H" or orient=="h":
        plt.axis("off")
        plt.plot([0,l],[0,0],color='k')
        plt.text(0,offset/3,"A",fontsize=15)
        plt.text(l/2,+offset/2,"L= "+str(l)+"m",fontsize=10,color='b')
        plt.text(max_off,offset/3,"B",fontsize=15)
        
        #Writing Forward fixed end moment in the plot
        if FRD>0:
            plt.text(0,-offset,"$FEM_{AB}$="+str(round(FRD,3))+" $kNm$ (CW)",fontsize=10)
        elif FRD==0:
            plt.text(0,-offset,"$FEM_{AB}$="+str(round(FRD,3))+" $kNm$",fontsize=10)
        else:
            plt.text(0,-offset,"$FEM_{AB}$="+str(round(FRD,3))+" $kNm$ (ACW)",fontsize=10)        
        
        #Writing backward fixed end moment in plot
        if BACK>0:
            plt.text(0.6*max_off,-offset,"$FEM_{BA}$="+str(round(BACK,3))+" $kNm$ (CW)",fontsize=10)
        elif BACK==0:
            plt.text(0.6*max_off,-offset,"$FEM_{BA}$="+str(round(BACK,3))+" $kNm$",fontsize=10)
        else:
            plt.text(0.6*max_off,-offset,"$FEM_{BA}$="+str(round(BACK,3))+" $kNm$ (ACW)",fontsize=10)
    else:
        plt.axis("off")
        plt.plot([0,0],[0,l],color='k')
        plt.text(-offset,0,"A",fontsize=15)
        plt.text(-offset,l,"B",fontsize=15)
        plt.text(+offset/2,l/2,"L= "+str(l)+"m",fontsize=10,color='b')
        #plt.text(offset,-offset,"$FEM_{AB}$="+str(round(FRD,3))+"$ kNm$",fontsize=12) 
        
        #Writing Forward fixed end moment in the plot
        if FRD>0:
            plt.text(offset/2,0,"$FEM_{AB}$="+str(round(FRD,3))+" $kNm$ (CW)",fontsize=10)
        elif FRD==0:
            plt.text(offset/2,0,"$FEM_{AB}$="+str(round(FRD,3))+" $kNm$",fontsize=10)
        else:
            plt.text(offset/2,0,"$FEM_{AB}$="+str(round(FRD,3))+" $kNm$ (ACW)",fontsize=10)        
        
        #Writing backward fixed end moment in plot
        if BACK>0:
            plt.text(offset/2,max_off,"$FEM_{BA}$="+str(round(BACK,3))+" $kNm$ (CW)",fontsize=10)
        elif BACK==0:
            plt.text(offset/2,max_off,"$FEM_{BA}$="+str(round(BACK,3))+" $kNm$",fontsize=10)
        else:
            plt.text(offset/2,max_off,"$FEM_{BA}$="+str(round(BACK,3))+" $kNm$ (ACW)",fontsize=10)
        
    print("____________________\nFixed end moments:\n____________________")
    print("FEM_AB= "+str(round(FRD,3))+"\nFEM_BA= "+str(round(BACK,3)))
    print("\n____________________\nSupport Reactions:\n____________________\n")
    print("R_A= "+str(round(R_A,3))+"\nR_B= "+str(round(R_B,3)))
else:
    win32ui.MessageBox("Invalid Orientation !!\nEnter H or h for horizontal orientation.\nEnter V or v for vertical orientation.","Quiting....!!!")
    quit()
    
