import os, jpype
from jpype import java

if not jpype.isJVMStarted():
	_jvmArgs = ["-ea"] # enable assertions
	#_jvmArgs.append("-Djava.class.path="+os.environ["CLASSPATH"])
	_jvmArgs.append("-Djava.class.path=C:\\Program Files\\Weka-3-6\\weka.jar;"+os.environ["CLASSPATH"])
	jpype.startJVM("C:\\Program Files\\Java\\jdk1.6.0_26\\jre\\bin\\server\\jvm.dll", *_jvmArgs)

weka = jpype.JPackage("weka")

JPypeObjectInputStream = jpype.JClass("JPypeObjectInputStream")

class WekaClassifier(object):
	def __init__(self, modelFilename, datasetFilename):
		self.dataset = weka.core.Instances(
			java.io.FileReader(datasetFilename))
		self.dataset.setClassIndex(self.dataset.numAttributes() - 1)

		self.instance = weka.core.Instance(self.dataset.numAttributes())
		self.instance.setDataset(self.dataset)

		ois = JPypeObjectInputStream(
			java.io.FileInputStream(modelFilename))
		self.model = ois.readObject()

	def classify(self, record):
		for i, v in enumerate(record):
			if v is None:
				self.instance.setMissing(i)
			else:
				self.instance.setValue(i, float(v))
		return self.dataset.classAttribute().value(
			int(self.model.classifyInstance(self.instance)))
			
	def rank(self, record):
		for i, v in enumerate(record):
			if v is None:
				self.instance.setMissing(i)
			else:
				self.instance.setValue(i, float(v))
		return self.model.distributionForInstance(self.instance)

#jpype.shutdownJVM() is not called ATM
