#The recipe gives simple implementation of a Discrete Proportional-Integral-Derivative (PID) controller. PID controller gives output value for error between desired reference input and measurement feedback to minimize error value.
#More information: http://en.wikipedia.org/wiki/PID_controller
#
#cnr437@gmail.com
#
#######	Example	#########
#
#p=PID(3.0,0.4,1.2)
#p.setPoint(5.0)
#while True:
#     pid = p.update(measurement_value)
#
#


class PID:
	"""
	Discrete PID control
	"""

	def __init__(self, P=2.0, I=0.0, D=1.0, Output_max=1.0, Output_min=0.1):

		self.Kp=P
		self.Ki=I
		self.Kd=D
		self.Integrator=0.0
		self.Output_max=Output_max
		self.Output_min=Output_min

		self.set_point=0.0
		self.error=0.0
		self.old_time = 0

	def update(self,current_value, time):
		#"""
		#Calculate PID output value for given reference input and feedback
		#"""

		self.dt = time - self.old_time
		self.old_time=time
		if self.dt<0.000000000000000000001:
			#self.dt=0.0000000000000000000000001
			self.dt=1.0
		self.old_error = self.error
		self.error = self.set_point - current_value
		self.Integrator = self.Integrator + self.error * self.dt
		self.P_value = self.Kp * self.error
		self.I_value = self.Integrator * self.Ki
		self.D_value = ((self.error-self.old_error)/self.dt)*self.Kd
		PID = self.P_value + self.I_value + self.D_value
		if PID > self.Output_max:
			PID = self.Output_max
		elif PID < self.Output_min:
			PID = self.Output_min
			
		
		return round(PID,3)

	def setPoint(self,set_point):
		"""
		Initilize the setpoint of PID
		"""
		self.set_point = set_point
		self.Integrator=0
		self.Derivator=0

	def setIntegrator(self, Integrator):
		self.Integrator = Integrator

	def setKp(self,P):
		self.Kp=P

	def setKi(self,I):
		self.Ki=I

	def setKd(self,D):
		self.Kd=D

	def getPoint(self):
		return self.set_point

	def getError(self):
		return self.error

	def getIntegrator(self):
		return self.Integrator

	def getDerivator(self):
		return self.Derivator




class AviaPID:
	"""
	Discrete PID control
	"""

	def __init__(self, P=2.0, I=0.0, D=1.0, Output_max=1.0, Output_min=0.1):

		self.Kp=P
		self.Ki=I
		self.Kd=D
		self.Integrator=0.0
		self.Derivator=0.0
		self.Output_max=Output_max
		self.Output_min=Output_min

		self.set_point=0.0
		self.error=0.0
		self.old_time = 0

	def update(self,current_value, time):
		#"""
		#Calculate PID output value for given reference input and feedback
		#"""

		self.dt = time - self.old_time
		self.old_time=time
		if self.dt<0.000000000000000000001:
			#self.dt=0.0000000000000000000000001
			self.dt=1.0
		self.old_error = self.error
		self.error = self.set_point - current_value
		self.Integrator = self.Integrator + self.error * self.dt
		self.P_value = self.Kp * self.error
		self.I_value = self.Integrator * self.Ki
		self.D_value = ((self.error-self.old_error)/self.dt)*self.Kd
		PID = self.P_value + self.I_value + self.D_value
		if PID > self.Output_max:
			PID = self.Output_max
		elif PID < self.Output_min:
			PID = self.Output_min
			
		
		return round(PID,3)

	def setPoint(self,set_point):
		"""
		Initilize the setpoint of PID
		"""
		self.set_point = set_point

	def setIntegrator(self, Integrator):
		self.Integrator = Integrator

	def setKp(self,P):
		self.Kp=P

	def setKi(self,I):
		self.Ki=I

	def setKd(self,D):
		self.Kd=D

	def getPoint(self):
		return self.set_point

	def getError(self):
		return self.error

	def getIntegrator(self):
		return self.Integrator

	def getDerivator(self):
		return self.Derivator
