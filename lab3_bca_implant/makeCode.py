#!/usr/bin/python

# import modules used here -- sys is a very standard one
import sys

# Gather our code in a main() function
def main():
	
	mesh = ""
	mesh = mesh + "go athena\n"
	mesh = mesh + "line x loc=0.00 spac=0.01\n"
	mesh = mesh + "line x loc=2.00 spac=0.01\n"
	mesh = mesh + "line y loc=0.00 spac=0.01\n"
	mesh = mesh + "line y loc=0.50 spac=0.02\n"
	mesh = mesh + "line y loc=1.00 spac=0.05\n"
	mesh = mesh + "line y loc=4.00 spac=0.1\n"
	mesh = mesh + "init silicon c.boron=3e16 orientation=100 space.mult=1.0\n"
	mesh = mesh + "method fermi\n"

	#implant boron dose=6e12 energy=55 tilt=7 rotation=45 crystal
	energies = ["75","150","300"]
	methods = ["", "monte"]
	oxideThickness = "0.65"
	dose = "2e15"
	tilt = "7"
	rotation = "45"
	for energy in energies:
		for method in methods:
			code = mesh
			code = code + "deposit oxide thick="+oxideThickness+" divisions=20\n"
			code = code + "implant boron dose="+dose+" energy="+energy+" tilt="+tilt+" rotation="+rotation+" crystal "+method+""
			if method=="monte": 
				code = code + " n.ion=100000"
			code = code + "\n"
			outfileName = "implant_"+method+"_"+energy
			code = code + "struct outfile=./structures/"+outfileName+".str\n"
			code = code + "extract name=\"sims\" curve(depth,impurity=\"Boron\" material=\"All\" x.val=.5) outfile=\"./srp_profiles/"+outfileName+".dat\"\n"
			code = code + "quit\n"
			fo = open("./masking_oxide/"+outfileName+".in", "wb")
			fo.write(code)
			fo.close()

	#create screen oxide sims
	oxideThickness = "0.05"
	energies = ["35","100"]
	methods = ["", "monte"]
	dose = "4e15"
	for energy in energies:
		for method in methods:
			code = mesh
			code = code + "deposit oxide thick="+oxideThickness+" divisions=10\n"
			code = code + "implant boron dose="+dose+" energy="+energy+" tilt="+tilt+" rotation="+rotation+" crystal "+method+""
			if method=="monte": 
				code = code + " n.ion=100000"
			code = code + "\n"
			outfileName = "implant_"+method+"_"+energy
			code = code + "struct outfile=./structures/"+outfileName+".str\n"
			code = code + "extract name=\"sims\" curve(depth,impurity=\"Boron\" material=\"All\" x.val=.5) outfile=\"./srp_profiles/"+outfileName+".dat\"\n"
			code = code + "quit\n"
			fo = open("./screen_oxide/"+outfileName+".in", "wb")
			fo.write(code)
			fo.close()
	

	#making channeling things
	oxideThickness = "0.025"
	oxideToggle = ["","#"]
	energies = ["50"]
	doses = ["4e15", "1e13"]
	method = "monte"
	dose = "4e15"
	tilts = ["7", "0"]
	rotations = ["45", "0"]
	for energy in energies:
		for dose in doses:
			for toggle in oxideToggle:
				for tilt in tilts:
					for rotation in rotations:
						code = mesh
						code = code + toggle + "deposit oxide thick="+oxideThickness+" divisions=10\n"
						code = code + "implant phosphor dose="+dose+" energy="+energy+" tilt="+tilt+" rotation="+rotation+" crystal "+method+""
						if method=="monte": 
							code = code + " n.ion=100000 smooth=0.4"
						code = code + "\n"
						outfileName = "implant_"+method+"_"+energy+"_"+tilt+"_"+rotation+"_"+dose
						if toggle=="":
							outfileName = outfileName + "_with_oxide"
						code = code + "struct outfile=./structures/"+outfileName+".str\n"
						code = code + "extract name=\"sims\" curve(depth,impurity=\"Phosphorus\" material=\"All\" x.val=.5) outfile=\"./srp_profiles/"+outfileName+".dat\"\n"
						code = code + "quit\n"
						fo = open("./ion_channeling/"+outfileName+".in", "wb")
						fo.write(code)
						fo.close()



# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
