from qiskit.circuit.library import TwoLocal
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms import VQE
from qiskit.primitives import StatevectorEstimator

def run_vqe_jch(hamiltonian, maxiter: int = 300):
    """
    Runs a Variational Quantum Eigensolver (VQE) and tracks convergence.
    """
    estimator = StatevectorEstimator()
    ansatz = TwoLocal(
        num_qubits=hamiltonian.num_qubits, 
        rotation_blocks='ry', 
        entanglement_blocks='cz', 
        reps=2 
    )
    optimizer = COBYLA(maxiter=maxiter)
    
    # List to store the energy at each iteration
    energy_history = []
    
    # The callback function that VQE calls at every step
    def store_intermediate_result(eval_count, parameters, mean, std):
        energy_history.append(mean)
        
    vqe = VQE(
        estimator=estimator, 
        ansatz=ansatz, 
        optimizer=optimizer,
        callback=store_intermediate_result  # Pass the callback here
    )
    
    result = vqe.compute_minimum_eigenvalue(hamiltonian)
    
    # We now return BOTH the final result and the history array
    return result, energy_history