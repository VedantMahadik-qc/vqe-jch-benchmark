from qiskit.circuit.library import TwoLocal
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms import VQE
from qiskit.primitives import StatevectorEstimator

def run_vqe_jch(hamiltonian, maxiter: int = 300):
    """
    Runs a Variational Quantum Eigensolver (VQE) to find the 
    ground state energy of the provided Hamiltonian.
    """
    # 1. Choose the backend primitive (Statevector for exact simulation)
    estimator = StatevectorEstimator()
    
    # 2. Define the hardware-efficient ansatz
    # 'ry' rotations explore the state space, 'cz' creates entanglement
    ansatz = TwoLocal(
        num_qubits=hamiltonian.num_qubits, 
        rotation_blocks='ry', 
        entanglement_blocks='cz', 
        reps=2 # Number of repetition layers
    )
    
    # 3. Define the classical optimizer
    optimizer = COBYLA(maxiter=maxiter)
    
    # 4. Initialize and run VQE
    vqe = VQE(estimator=estimator, ansatz=ansatz, optimizer=optimizer)
    result = vqe.compute_minimum_eigenvalue(hamiltonian)
    
    return result