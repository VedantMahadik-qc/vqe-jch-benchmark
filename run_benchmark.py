from src.mapping import get_jch_pauli_op
from src.vqe_solver import run_vqe_jch
from qiskit_algorithms import NumPyMinimumEigensolver

def main():
    # 1. Setup the JCH parameters
    wc, g, J = 1.0, 0.05, 0.1
    print(f"\n--- JCH-VQE Benchmark ---")
    print(f"Parameters: wc={wc}, g={g}, J={J}")
    
    print("\nMapping Hamiltonian to Qubits...")
    H = get_jch_pauli_op(wc, g, J)
    print(f"Total Qubits Required: {H.num_qubits}")

    # 2. Get the EXACT ground state energy (Classical Benchmark)
    # This acts as our "ground truth" replacing the need to boot up Julia for this test
    exact_solver = NumPyMinimumEigensolver()
    exact_result = exact_solver.compute_minimum_eigenvalue(H)
    exact_energy = exact_result.eigenvalue.real
    
    # 3. Run the VQE (Quantum Algorithm)
    print("\nRunning VQE Optimizer (this might take a few seconds)...")
    vqe_result = run_vqe_jch(H, maxiter=300)
    vqe_energy = vqe_result.eigenvalue.real

    # 4. Print the final comparison
    print("\nResults ")
    print(f"Exact Ground State Energy: {exact_energy:.6f}")
    print(f"VQE Ground State Energy:   {vqe_energy:.6f}")
    
    # The Delta tells us how accurate our Quantum Algorithm is!
    delta = abs(exact_energy - vqe_energy)
    print(f"Error (Delta):             {delta:.6f}")

if __name__ == "__main__":
    main()