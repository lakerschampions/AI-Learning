# Metaheuristics
A metaheuristic is a high-level problem independent algorithmic framework that provides a set of guidelines or strategies to develop heuristic optimization algorithms.

# Metaheuristic Search Method
- Representation of candidate solutions
- Evaluation function
- Initialisation
- Neighbourhood relation

# Escaping from Local Optimal
- Iterate with different solutions, or restart (reinitialise search whenever a local optimum is encountered).  e.g. Iterated Local Search, GRASP.
- Change the search landscape. Change the objective function (E.g., Guided Local Search); Use (mix) different neighbourhoods (E.g., Variable Neighbourhood Search, Hyper-heuristics)
- Use Memory (e.g., tabu search)
- Accept non-improving moves: allow search using candidate solutions with equal or worse evaluation function value than the one in hand.
