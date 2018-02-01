import pickle


class Picanha:

	def __init__(self):
		pass

	def save(self, fileSave, name = "colorConfig"):
		pickle.dump(fileSave, open(str(name)+".p", "wb"))
		print "File saved as " + str(name)

	def load(self, name = "colorConfig"):
		self.fileLoad = pickle.load( open(str(name)+".p", "rb"))
		print " File loaded, "+str(name)
		return self.fileLoad