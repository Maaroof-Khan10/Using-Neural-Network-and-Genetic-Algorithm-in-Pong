# Libraries
import numpy as np
import random

# Our AI class
class AI(object):

    # Creating a basic neural network - Simple input/output
    def base_net(self, input_layer, output_layer):
        net = []
        net.append(input_layer)
        weights = np.random.rand(input_layer, output_layer).tolist()
        net.append(weights)
        biases = np.random.rand(output_layer).tolist()
        net.append(biases)
        net.append(output_layer)
        return net

    # Activation in case you wanna use it
    def sigmoid(self, x):
        return 1/(1 + np.exp(-x))

    # Running our basic network
    def run_base_net(self, network, data):
        if network[0] == len(data):
            weighed = []
            for i in range(len(data)):
                point = data[i]
                point_weighed = []
                weights = network[1][i]
                for weight in weights:
                    point_weighed.append(point * weight)
                weighed.append(point_weighed)
            results = []
            for i in range(len(weighed[0])):
                biases = network[2]
                result = 0
                for j in range(len(weighed)):
                    result += weighed[j][i]
                result += biases[i]
                # Sigmoid in this case was not working well so I commented it - You can use it or any other activation if you want
                #result = self.sigmoid(result)
                results.append(result)
            return results
        else:
            print(f"Size {network[0]} was required but size {len(data)} was given")

    # Creating a complex network by combining simple networks - Fully connected network
    def create_network(self, input_layer, output_layer, width=1, height=1):
        network = []
        if width == 0 or height == 0:
            network.append(self.base_net(input_layer, output_layer))
            return network
        else:
            network_width = np.random.randint(width)
            if network_width == 0:
                network.append(self.base_net(input_layer, output_layer))
                return network
            else:
                network_height = np.random.randint(1, height)
                network.append(self.base_net(input_layer, network_height))
                for i in range(network_width):
                    old_height = network_height
                    network_height = np.random.randint(1, height)
                    network.append(self.base_net(old_height, network_height))
                network.append(self.base_net(network_height, output_layer))
                return network

    # Running our complex network
    def run_network(self, network, data):
        results = []
        for net in network:
            results = self.run_base_net(net, data)
            data = results
        return results

    # Creating a population of complex networks
    def create_population(self, size, input_layer, output_layer, width=1, height=1):
        population = []
        for i in range(size):
            population.append(self.create_network(input_layer, output_layer, width, height))
        return population

    # Crossing them to get new child - Can customize this function
    def cross_mating(self, pool, size, new):
        new_population = []
        for network in pool:
            new_population.append(network)
        iteration = size - len(pool) - new
        for i in range(iteration):
            parent1 = random.choice(pool)
            parent2 = random.choice(pool)
            room = [parent1, parent2]
            # Change this to your network size
            offspring = self.create_network(5, 3, 0, 0)
            parent1RandomNode = random.choice(parent1)
            parent2RandomNode = random.choice(parent2)
            weights = []
            biases = []
            for weight in parent1RandomNode[1]:
                for weigh in weight:
                    weights.append(weigh)
            for weight in parent2RandomNode[1]:
                for weigh in weight:
                    weights.append(weigh)
            for bias in parent1RandomNode[2]:
                biases.append(bias)
            for bias in parent2RandomNode[2]:
                biases.append(bias)
            offspringRandomNode = random.choice(offspring)
            index_offspringRandomNode = offspring.index(offspringRandomNode)
            weights_to_change = random.choice(offspringRandomNode[1])
            index_weights_to_change = offspringRandomNode[1].index(weights_to_change)
            for i in range(len(weights_to_change)):
                weight = random.choice(weights_to_change)
                random_weight = random.choice(weights)
                index_weight = weights_to_change.index(weight)
                weights_to_change[index_weight] = random_weight
            offspringRandomNode[1][index_weights_to_change] = weights_to_change
            biases_to_change = offspringRandomNode[2]
            for i in range(len(biases_to_change)):
                bias = random.choice(biases_to_change)
                random_bias = random.choice(biases)
                index_bias = biases_to_change.index(bias)
                biases_to_change[index_bias] = random_bias
            offspringRandomNode[2] = biases_to_change
            offspring[index_offspringRandomNode] = offspringRandomNode
            new_population.append(offspring)
        for i in range(new):
            # Can change this
            network = self.create_network(5, 3, 0, 0)
            new_population.append(network)
        return new_population

    # Mutating the babies
    def mutate(self, population, rate):
        for i in range(rate):
            mutation = np.random.random_sample()
            network = random.choice(population)
            index = population.index(network)
            node = random.choice(network)
            index_node = network.index(node)
            to_choose = [1, 2]
            chosen = random.choice(to_choose)
            if chosen == 1:
                weights = random.choice(node[chosen])
                index_weights = node[chosen].index(weights)
                weight = random.choice(weights)
                index_weight = weights.index(weight)
                mutated_weight = weight + mutation
                weights[index_weight] = mutated_weight
                node[chosen][index_weights] = weights
            else:
                bias = random.choice(node[chosen])
                index_bias = node[chosen].index(bias)
                mutated_bias = bias + mutation
                node[chosen][index_bias] = mutated_bias
            network[index_node] = node
            population[index] = network
        return population
