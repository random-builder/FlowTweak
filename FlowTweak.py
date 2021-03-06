#Name: FlowTweak
#Info: Change Flow % on skin/skirt over a range of layers
#Depend: GCode
#Type: postprocess
#Param: startL(int:0) Layer no. to start
#Param: twLayers(int:3) No. of layers to change
#Param: twSkinFlow(int:80) Change Skin Flow %
#Param: twSkirtFlow(int:100) Change Skirt Flow %
#Param: defFlow(int:100) Default/Normal Flow %

startL = int(startL)
twLayers = int(twLayers)
twSkinFlow = int(twSkinFlow)
twSkirtFlow = int(twSkirtFlow)
defFlow = int(defFlow)

modFlow = False
currentLayer = 0

with open(filename, "r") as f:
	lines = f.readlines()

with open(filename, "w") as f:

	for lIndex in xrange(len(lines)):
		line = lines[lIndex]

		f.write(line)

		if line.startswith(';'):
			if line.startswith(';LAYER:'):
				currentLayer = int(line[7:].strip())

				if currentLayer == 0:
					#f.write("; FlowTweak\n")
					#f.write("; Params startL: %i\n" % (startL))
					#f.write("; Params twLayers: %i\n" % (twLayers))
					#f.write("; Params twSkinFlow: %i\n" % (twSkinFlow))
					#f.write("; Params twSkirtFlow: %i\n" % (twSkirtFlow))
					#f.write("; Params defFlow: %i\n" % (defFlow))

					# start off at default flow rate
					f.write("; FlowTweak - Print Layers %i-%i at Skin:%i%%/Skirt:%i%% -- start at %i%%\n" % ( startL, (startL+twLayers), twSkinFlow, twSkirtFlow, defFlow ))
					f.write("M221 T0 S%f\n" % (defFlow))

			if currentLayer >= startL and currentLayer < ( startL + twLayers ):
				if line.startswith(";TYPE:SKIN"):  #Enable flow tweaks on SKIN type only
					f.write("; FlowTweak - Reduce SKIN flow to %i%%\n" % (twSkinFlow))
					f.write("M221 T0 S%f\n" % (twSkinFlow))
					modFlow = True
				if line.startswith(";TYPE:SKIRT"):  #Enable flow tweaks on SKIRT type only
					f.write("; FlowTweak - Reduce SKIRT flow to %i%%\n" % (twSkirtFlow))
					f.write("M221 T0 S%f\n" % (twSkirtFlow))
					modFlow = True

			if line.startswith(";TYPE:") and not ( line.startswith(";TYPE:SKIN") or line.startswith(";TYPE:SKIRT") ) and modFlow == True:  #Restore default flow for other types
				f.write("; FlowTweak - Reset flow to %i%%\n" % (defFlow))
				f.write("M221 T0 S%f\n" % (defFlow))
				modFlow = False

			if currentLayer == ( startL + twLayers ) and modFlow == True:
				f.write("; FlowTweak - Reset flow to %i%%\n" % (defFlow))
				f.write("M221 T0 S%f\n" % (defFlow))
				modFlow = False

	# reset to default flow at the end
	f.write("; FlowTweak - Reset flow to %i%%\n" % (defFlow))
	f.write("M221 T0 S%f\n" % (defFlow))
