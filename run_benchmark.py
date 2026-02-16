import matplotlib.pyplot as plt
from src.mapping import get_jch_pauli_op
from src.vqe_solver import run_vqe_jch
from qiskit_algorithms import NumPyMinimumEigensolver

def main():
    wc, g, J = 1.0, 0.05, 0.1
    print("\nJCH-VQE Benchmark")
    
    H = get_jch_pauli_op(wc, g, J)
    
    exact_solver = NumPyMinimumEigensolver()
    exact_energy = exact_solver.compute_minimum_eigenvalue(H).eigenvalue.real
    
    print("\nRunning VQE Optimizer")
    # Unpack the two returned values
    vqe_result, energy_history = run_vqe_jch(H, maxiter=300)
    vqe_energy = vqe_result.eigenvalue.real

    print("\n Results ")
    print(f"Exact Energy: {exact_energy:.6f}")
    print(f"VQE Energy:   {vqe_energy:.6f}")
    print(f"Error:        {abs(exact_energy - vqe_energy):.6f}")

    # --- Plotting the Convergence ---
    print("\nGenerating convergence plot...")
    plt.figure(figsize=(8, 5))
    
    # Plot the VQE learning curve
    plt.plot(energy_history, label="VQE Energy", color='#6600CC', linewidth=2)
    
    # Draw a dashed line for the target exact energy
    plt.axhline(y=exact_energy, color='black', linestyle='--', 
                label=f"Exact Energy ({exact_energy:.4f})")
    
    # Graph styling
    plt.title("VQE Convergence for 2-Site JCH Model", fontsize=14, fontweight='bold')
    plt.xlabel("Optimizer Iteration", fontsize=12)
    plt.ylabel("Ground State Energy", fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.tight_layout()
    
    # Save the image
    filename = "vqe_convergence.png"
    plt.savefig(filename, dpi=300)
    print(f"Plot saved successfully as '{filename}'!")

if __name__ == "__main__":
    main()