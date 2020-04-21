from numpy import exp, array, random, dot

class NeuralNetwork():
  def __init__(self):
    self.seed_random_number_generator()
    self.create_weight_matrix()

  def seed_random_number_generator(self):
    random.seed(1)

  def create_weight_matrix(self):
    self.weights = 2 * random.random((3, 1)) - 1 # create a 3x1 matrix for weights that have values ranging from -1 to 1 and mean 0

  def sigmoid(self, x): # takes in a weighted sum of the inputs and normalizes them between 0 and 1
    return 1 / (1 + exp(-x))

  def sigmoid_derivative(self, x): # the derivative of the sigmoid function used to calculate the necessary weight adjustments
    return x * (1 - x)

  def train(self, inputs, outputs, iterations): # train the model through trail and error, adjusting the weights each time to get a better result
    for iteration in range(iterations):
      output = self.think(inputs) # pass training set through the neural network
      error = outputs - output # calculate the error rate
      adjustments = error * self.sigmoid_derivative(output) # multiply the error by the input and gradient of the sigmoid function
      self.weights += dot(inputs.T, adjustments) # adjust the weights

  def think(self, inputs): # pass inputs through the neural network to get output
    inputs = inputs.astype(float)
    output = self.sigmoid(dot(inputs, self.weights))
    return output

def init():
  neural_network = NeuralNetwork() # initialize the single neuron neural network
  print("random starting weights: \n{}".format(neural_network.weights))
  inputs = array(get_training_inputs()) # the training set, with 4 examples consisting of 3 input values and 1 output value
  outputs = array(get_training_outputs()).T
  neural_network.train(inputs, outputs, 10000) # train the neural network
  print("weights after training: \n{}".format(neural_network.weights))
  ask_for_input(neural_network)

def get_training_inputs():
  return [[0,0,1],[1,1,1],[1,0,1],[0,1,1]]

def get_training_outputs():
  return [[0,1,1,0]]

def ask_for_input(neural_network):
  A = str(input('Input 1: '))
  B = str(input('Input 2: '))
  C = str(input('Input 3: '))
  print('new input data: {}, {}, {}'.format(A, B, C))
  print("output data: \n{}".format(neural_network.think(array([A, B, C]))))

if __name__ == '__main__':
  init()
