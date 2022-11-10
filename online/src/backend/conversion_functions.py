

class Convert:

	#Converts an ID number to the index of its category's list
	def id_to_local(self, globalID):
		if globalID < 100:
			category = 1
		elif globalID < 200:
			category = 2
		elif globalID < 300:
			category = 3
		else:
			category = None
		localID = globalID % 100

		return localID, category