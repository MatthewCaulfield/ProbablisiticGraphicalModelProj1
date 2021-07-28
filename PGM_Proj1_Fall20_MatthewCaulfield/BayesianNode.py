class BayesianNode:
    # BayesianNodes are initialized with their name a list of their parents, a list of their children, the probability
    # of the node, or the probability of the node given its parents. The maximum number of parents and children are two
    # parents is a list of parents whose order matters!
    # children is a list of children nodes whose order matters!
    # prob is the probability of the node in the form of a tuple whose first value is if the node is 0 and
    # second value is if the node is 1
    # parProb is a list of tuples containing the probability of the nodes given its parents. The order of the parents
    # probability is the same as the order of the parents in parents. The order of parProb is always the same for 1 or 2
    # parents and is as follows.
    # ex (P(x|parent1=0, parent2=0),P(x|parent1=0, parent2=1), P(x|parent1=1, parent2=0), P(x|parent1=1, parent2=1))
    # ex (P(x|parent1 = 0), P(x|parent1 =1))
    def __init__(self, name, parentnodes = None, childrennodes = None, probability = None, probparents = None):
        self.name = name
        self.lam = (1, 1)
        self.pi = (1, 1)
        self.previouPi = 1
        self.oldProb = (0, 1)
        if parentnodes is None:
            self.parents = []
            self.pi = probability
        else:
            self.parents = parentnodes
        if childrennodes is None:
            self.children = []
        else:
            self.children = childrennodes
        if probability is None:
            self.prob = ()
        else:
            self.prob = probability
        if probparents is None:
            self.parProb = ()
        else:
            self.parProb = probparents

    #returns the name of the Bayesian Node as a string
    def __str__(self):
        return self.name

    # Sets pi when given a probability
    def setPi(self, probability):
        self.pi = probability

    # Sets lambda when given a Probability
    def setLam(self, probability):
        self.lam = probability

    # returns the Lambda value of the node
    def getLam(self):
        return self.lam

    # returns the Pi value of the node
    def getPi(self):
        return self.pi

    # returns the probability value of the node
    def getProb(self):
        return self.prob

    # returns the children of the node
    def getChildren(self):
        return self.children

    # returns the parents of the node
    def getParents(self):
        return self.parents

    # Sets the probability value of the node given a probability
    def setProb(self, probability):
        self.prob = probability

    # sets the children of the node given a list of child nodes
    def setChildren(self, childrenNodes):
        self.children = childrenNodes

    # sets the parents of the node given a list of parents and a list of parent probability in the correct order
    # outlined at the top of the class
    def setParents(self, parentNodes, parentProb):
        self.parents = parentNodes
        self.parProb = parentProb

    # Updates pi vk from each of its parents using eqn 3.24 from the textbook
    # takes a parent vk and returns pivk
    def updatePivk(self, parent):
        parentPi = parent.getPi()
        parentChildren = parent.getChildren()
        lamC = (1, 1)
        for child in parentChildren:
            if child != self:
                lamyjChild = parent.lamYj(child)
                lamC = (lamC[0]*lamyjChild[0], lamC[1]*lamyjChild[1])
        return (parentPi[0]*lamC[0], parentPi[1]*lamC[1])

    # updates pi using eqn 3.23 from the textbook
    # returns the updated pi of the node
    def updatePi(self):
        parentProb = self.parProb
        parents = self.getParents()
        numParents = len(parents)
        if numParents == 1:
            piVK =self.updatePivk(parents[0])
            piX = (0, 0)
            for prob in parentProb:
                piX = (piX[0]+prob[0], piX[1]+prob[1])
            self.pi = (piVK[0] * piX[0]*piVK[1], piVK[1] * piX[1]*piVK[1])
            return self.pi
        elif numParents == 2:
            piVK = []
            for i in range(0,numParents):
                parent = parents[i]
                piVK = piVK + [self.updatePivk(parent)]
            pi = (0, 0)
            #print(piVK)
            k = 0
            for i in [0, 1]:
                for j in range(0, len(self.parents)):
                    pi = ((pi[0] + parentProb[k][0] * piVK[0][i] * piVK[1][j]), \
                             (pi[1] + parentProb[k][1] * piVK[0][i] * piVK[1][j]))
                    k = k + 1
            self.pi = pi
            return self.pi

        # updates pi using max-product from lecturenotes
        # returns the updated pi of the node
    def updatePiMaxProd(self):
        parentProb = self.parProb
        parents = self.getParents()
        numParents = len(parents)
        if numParents == 1:
            piVK = self.updatePivk(parents[0])
            piX = max(parentProb, key=lambda x:x[1])
            self.pi = (piVK[0] * piX[0] * piVK[1], piVK[1] * piX[1] * piVK[1])
            return self.pi
        elif numParents == 2:
            piVK = []

            for i in range(0, numParents):
                parent = parents[i]
                piVK = piVK + [self.updatePivk(parent)]
            piX = max(parentProb, key=lambda x: x[1])
            k = parentProb.index(piX)
            if k < 2:
                i = k
            else:
                i = k-2
            j = k%2
            pi = (piX[0] * piVK[0][i] * piVK[1][j], piX[1] * piVK[0][i] * piVK[1][j])

            self.pi = pi
            return self.pi


    # updates lamda yj using eqns 3.26 from the textbook
    # takes the child Yj of the node and returns the lamda(Yj) for that child
    def lamYj(self, child):
        lamChild = child.getLam()
        childParents = child.getParents().copy()
        childParents.remove(self)
        childParProb = (0, 0)
        for parent in childParents:
            parPi = parent.getPi()
        for i in range(len(child.parProb)):
            selfInd = child.getParents().index(self)
            if len(child.getParents()) > 1:
                cparProb = child.parProb
                if selfInd == 0:
                    if i < 2:
                        childParProb = (childParProb[0] + lamChild[0] * cparProb[i][0] * parPi[i % 2] + \
                                        lamChild[1] * cparProb[i][1] * parPi[i % 2], childParProb[1])
                    else:
                        childParProb = (childParProb[0], childParProb[1] + lamChild[0] * cparProb[i][0] * \
                                        parPi[i % 2] + lamChild[1] * cparProb[i][1] * parPi[i % 2])
                else:
                    if i % 2 == 0:
                        if i < 2:
                            childParProb = (childParProb[0] + lamChild[0] * cparProb[i][0] * parPi[0] + \
                                            lamChild[1] * cparProb[i][1] * parPi[0], childParProb[1])
                        else:
                            childParProb = (childParProb[0] + lamChild[0] * cparProb[i][0] * parPi[1] + \
                                            lamChild[1] * cparProb[i][1] * parPi[1], childParProb[1])
                    else:
                        if i < 2:
                            childParProb = (childParProb[0], childParProb[1] + lamChild[0] * \
                                            cparProb[i][0] * parPi[0] + lamChild[1] * cparProb[i][1] * parPi[0])
                        else:
                            childParProb = (childParProb[0], childParProb[1] + lamChild[0] * \
                                            cparProb[i][0] * parPi[1] + lamChild[1] * cparProb[i][1] * parPi[1])
            else:
                childParProb = (lamChild[0] * child.parProb[0][0] + \
                                lamChild[1] * child.parProb[0][1], lamChild[0] * \
                                child.parProb[1][0] + lamChild[1] * child.parProb[1][1])
        return childParProb

    # updates lamdyja using max-product from the lectures
    # takes the child Yj of the node and returns the lamda(Yj) for that child
    def lamYjMaxProd(self, child):
        lamChild = child.getLam()
        childParents = child.getParents().copy()
        childParents.remove(self)
        childParProb = (0, 0)
        for parent in childParents:
            parPi = parent.getPi()
        for i in range(len(child.parProb)):
            selfInd = child.getParents().index(self)
            if len(child.getParents()) > 1:
                if selfInd == 0:
                    cparProb = child.parProb
                    cparProb0 = [cparProb[0], cparProb[1]]
                    cparProb1 = [cparProb[2], cparProb[3]]
                    maxcparProb0 = max(cparProb0, key=lambda x: x[1])
                    maxcparProb1 = max(cparProb1, key=lambda x: x[1])
                    childParProb = (childParProb[0] + lamChild[0] * maxcparProb0[0] * parPi[0] + \
                                       lamChild[1] * maxcparProb0[1] * parPi[1],
                                    childParProb[1]+ lamChild[0] * maxcparProb1[0] * parPi[0] + \
                                       lamChild[1] * maxcparProb1[1] * parPi[1])
                else:
                    cparProb = child.parProb
                    cparProb0 = [cparProb[0], cparProb[2]]
                    cparProb1 = [cparProb[1], cparProb[3]]
                    maxcparProb0 = max(cparProb0, key=lambda x: x[1])
                    maxcparProb1 = max(cparProb1, key=lambda x: x[1])
                    childParProb = (childParProb[0] + lamChild[0] * maxcparProb0[0] * parPi[0] + \
                                       lamChild[1] * maxcparProb0[1] * parPi[1],
                                    childParProb[1]+ lamChild[0] * maxcparProb1[0] * parPi[0] + \
                                       lamChild[1] * maxcparProb1[1] * parPi[1])
            else:
                childParProb = (lamChild[0] * child.parProb[0][0] + \
                                lamChild[1] * child.parProb[0][1], lamChild[0] * \
                                child.parProb[1][0] + lamChild[1] * child.parProb[1][1])
        return childParProb

    #updates lamda using eqns 3.25 from the textbook
    def updateLam(self):
        children = self.getChildren()
        lamX = (1, 1)
        for child in children:
            lamChild = self.lamYj(child)
            lamX = (lamX[0]*lamChild[0], lamX[1]*lamChild[1])
        self.lam = lamX

    # updates lamda using eqns 3.25 from the textbook but for the max-product
    def updateLamMaxProd(self):
        children = self.getChildren()
        lamX = (1, 1)
        for child in children:
            lamChild = self.lamYjMaxProd(child)
            lamX = (lamX[0] * lamChild[0], lamX[1] * lamChild[1])
        self.lam = lamX

    #updates the probabilty using alpha*Pi(Xn)*Lambda(Xn)
    def updateProb(self):
        if self.prob == ():
            self.oldProb = (0, 1)
        else:
            self.oldProb = self.prob
        pilam = (self.pi[0]*self.lam[0], self.pi[1]*self.lam[1])
        alpha = 1/(pilam[0]+pilam[1])
        self.prob = (alpha*pilam[0], alpha*pilam[1])

    # returns the distance from the old probability to the new probability
    def convergence(self):
        return abs(self.prob[0] - self.oldProb[0]) + abs(self.prob[1] - self.oldProb[1])
