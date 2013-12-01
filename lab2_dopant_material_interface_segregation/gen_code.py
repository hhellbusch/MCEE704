#!/usr/bin/python

# import modules used here -- sys is a very standard one
import sys

# Gather our code in a main() function
def main():
	impurities = ["boron","phosphorus","arsenic"]
	temperatures = ["900","1000","1100"]

	#gen code for segregation
	for impurity in impurities:
		for temp in temperatures:
			seg_code = "go athena \n"
			seg_code = seg_code + "line x loc=0.00 spac=0.001 \n"
			seg_code = seg_code + "line x loc=1.00 spac=0.001 \n"
			seg_code = seg_code + "line y loc=0.00 spac=0.001 \n"
			seg_code = seg_code + "line y loc=1.00 spac=0.001 \n"
			seg_code = seg_code + "extract name =\"-" + impurity + " SEGREAGATION @ " + temp + " C =\"\n"
			
			impurityconc = "3e19"
			if impurity == "boron" and temp == "900":
				impurityconc = "1.39e17"
			if impurity == "boron" and temp == "1000":
				impurityconc = "2.81e17"
			if impurity == "boron" and temp == "1100":
				impurityconc = "5.15e17"

			seg_code = seg_code + "init silicon c."+ impurity +"="+impurityconc+" orientation=100 space.mult=1.0 \n"
			seg_code = seg_code + "deposit oxide thick=1.00 c."+ impurity +"=1.0e18 dy=0.01\n"

			seg_code = seg_code + "extract name=\"pre surfconc for si\" surf.conc impurity=\"Net Doping\" material=\"Silicon\" mat.occno=1 x.val=1\n"
			seg_code = seg_code + "extract name=\"pre surfconc for sio2\" surf.conc impurity=\"Net Doping\" material=\"SiO~2\" mat.occno=1 x.val=1\n"

			seg_code = seg_code + "diffus time=60 temp=" + temp + " nitro\n"

			seg_code = seg_code + "tonyplot\n"
			seg_code = seg_code + "struct outfile=./structures/seg_trans_coef_"+impurity+"_"+temp+".str\n"
			seg_code = seg_code + "extract name=\"post surfconc for si\" surf.conc impurity=\"Net Doping\" material=\"Silicon\" mat.occno=1 x.val=1\n"
			seg_code = seg_code + "extract name=\"post surfconc for sio2\" surf.conc impurity=\"Net Doping\" material=\"SiO~2\" mat.occno=1 x.val=1\n"
			seg_code = seg_code + "quit"
			fo = open("./segregation/segregation_" + impurity + "_" + temp + ".in", "wb")
			fo.write(seg_code)
			fo.close()

	#gen code for transport
	for impurity in impurities:
		for temp in temperatures:

			trans_code = "go athena\n"

			trans_code = trans_code + "line x loc=0.00 spac=0.001\n"
			trans_code = trans_code + "line x loc=1.00 spac=0.001\n"
			trans_code = trans_code + "line y loc=0.00 spac=0.0001\n"
			trans_code = trans_code + "line y loc=0.05 spac=0.0001\n"
			trans_code = trans_code + "extract name =\"=h sim " + impurity + " @ " + temp + " C ====\"\n"
			trans_code = trans_code + "init silicon orientation=100 space.mult=1.0\n"

			trans_code = trans_code + "deposit oxide thick=0.05 c."+impurity+"=1.0e20 dy=0.0001\n"

			trans_code = trans_code + "extract name=\"pre surfconc for si\" surf.conc impurity=\"Net Doping\" material=\"Silicon\" mat.occno=1 x.val=1\n"
			trans_code = trans_code + "extract name=\"pre surfconc for sio2\" surf.conc impurity=\"Net Doping\" material=\"SiO~2\" mat.occno=1 x.val=1\n"
			trans_code = trans_code + "diffus time=0.1/60 temp="+temp+" nitro\n"
			trans_code = trans_code + "tonyplot\n"

			trans_code = trans_code + "extract name=\"post surfconc for si\" surf.conc impurity=\"Net Doping\" material=\"Silicon\" mat.occno=1 x.val=1\n"
			trans_code = trans_code + "extract name=\"post surfconc for sio2\" surf.conc impurity=\"Net Doping\" material=\"SiO~2\" mat.occno=1 x.val=1\n"
			trans_code = trans_code + "extract name=\"dose\" area from curve(depth,impurity=\""+impurity+"\" material=\"Silicon\" mat.occno=1 x.val=0.1)/10000\n"
			trans_code = trans_code + "struct outfile=./structures/interface_trans_coef_"+impurity+"_"+temp+".str\n"
			trans_code = trans_code + "quit"

			fo = open("./interface_trans/trans_" + impurity + "_" + temp + ".in", "wb")
			fo.write(trans_code)
			fo.close()




# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
