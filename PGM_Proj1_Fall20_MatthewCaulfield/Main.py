import BayesianNode as BNode

# Initializing the bayesian nodes and network using Bayesian Node class.
# BayesianNode(Parents, Children, probability, Probability given parents)
A = BNode.BayesianNode("A", None, None, (0.4, 0.6), None)
S = BNode.BayesianNode("S", None, None, (0.2, 0.8), None)
L = BNode.BayesianNode("L", None, None, (0.2, 0.8), None)
T = BNode.BayesianNode("T", [A], None, None, [(0.7, 0.3), (0.2, 0.8)])
B = BNode.BayesianNode("B", [S], None, None, [(0.7, 0.3), (0.3, 0.7)])
E = BNode.BayesianNode("E", [L, T], None, None, ((0.9, 0.1), (0.3, 0.7), (0.4, 0.6), (0.2, 0.8)))
F = BNode.BayesianNode("F", [B, E], None, None, [(0.8, 0.2), (0.2, 0.8), (0.3, 0.7), (0.1, 0.9)])
X = BNode.BayesianNode("X", [E], None, None, ((0.9, 0.1), (0.2, 0.8)))
# Have to set children separately
A.setChildren([T])
T.setChildren([E])
S.setChildren([B])
B.setChildren([F])
L.setChildren([E])
E.setChildren([X])

# Initialize Lambda and Pi for root nodes A, S, L
A.setPi(A.getProb())
A.setLam((1, 1))
S.setPi(S.getProb())
S.setLam((1, 1))
L.setLam((1, 1))
L.setPi(L.getProb())

# Initialize Lambda for leaf nodes
F.setLam((0, 1))
X.setLam((1, 0))
F.setPi((0, 1))
X.setPi((1, 0))

# creat a list of the unknown nodes
unknowns = [B, S, E, L, T, A]

# update the posterior probability of the unknown nodes until the probabilities converge using sum-product.
conv = 1
i = 1
while(conv > 10**(-16)):
    conv = 0
    for node in unknowns:
        node.updatePi()
        #print(node.__str__() + "pi", node.getPi())
        node.updateLam()
        #print(node.__str__() + "lam", node.getLam())
        node.updateProb()
        #print(node.__str__() + "prob", node.getProb())
        conv = conv + node.convergence()
    #print("convergence", conv)
    i = i+1

for node in unknowns:
    print(node.__str__() + "prob", node.getProb())
print("Number of iterations until convergence", i)

#updates the probability of the unknown nodes using max-product
conv = 1
i = 1
while(conv > 10**(-16)):
    conv = 0
    for node in unknowns:
        node.updatePiMaxProd()
        #print(node.__str__() + "pi", node.getPi())
        node.updateLamMaxProd()
        #print(node.__str__() + "lam", node.getLam())
        node.updateProb()
        #print(node.__str__() + "prob", node.getProb())
        conv = conv + node.convergence()
    #print("convergence", conv)
    i = i+1

#configures the nodes
nodeConfigs = []
for node in unknowns:
    nodeProb = node.getProb()
    nodeConfiguration = None
    if nodeProb[0]> nodeProb[1]:
        nodeConfiguration = "0"
    else:
        nodeConfiguration = "1"
    nodeConfigs.append(node.__str__() + "=" + nodeConfiguration)
print(nodeConfigs)
print("Number of iterations until convergence", i)