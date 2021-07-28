import BayesianNode as BNode
B = BNode.BayesianNode("B", None, None, (0.999, 0.001), None)
E = BNode.BayesianNode("E", None, None, (0.998, 0.002), None)
P = BNode.BayesianNode("P", None, None, (0.95, 0.05), None)
A = BNode.BayesianNode("A", [B, E], None, None, ((0.999, 0.001), (0.71, 0.29), (0.06, 0.94), (0.05, 0.95)))
J = BNode.BayesianNode("J", [P, A], None, None, ((0.99, 0.01), (0.1, 0.9), (0.5, 0.5), (0.05, 0.95)))
M = BNode.BayesianNode("M", [A], None, None, ((0.99, 0.01), (0.3, 0.7)))
E.setChildren([A])
B.setChildren([A])
A.setChildren([J, M])
P.setChildren([J])


# Initialize Lambda and Pi for root nodes A and S
B.setPi(B.getProb())
B.setLam((1, 1))
P.setPi(P.getProb())
P.setLam((1, 1))
E.setPi(E.getProb())
E.setLam((1, 1))

# Initialize Lambda for leaf nodes
J.setLam((1, 1))
M.setLam((0, 1))
M.setPi((0, 1))

unknowns = [A, B, E, J, P]
#print(J.getLam())
print(A.lamYj(J))
print(A.lamYj(M))
print(A.updatePivk(B))
conv = 1
i = 1
i = i+1
while(conv > 10**(-14)):

    conv = 0
    for node in unknowns:
        node.updatePi()
        print(node.__str__() + "pi", node.getPi())
        node.updateLam()
        print(node.__str__() + "lam", node.getLam())
        node.updateProb()
        print(node.__str__() + "prob", node.getProb())
        conv = conv + node.convergence()
    print("convergence", conv)

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