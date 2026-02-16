import numpy as np
from src.mapping import get_jch_pauli_op

def test_jch_hamiltonian_is_hermitian():
    """
    Validates that the generated Pauli operator for the JCH model
    is a valid, Hermitian observable.
    """
    # Generate Hamiltonian with arbitrary parameters
    H = get_jch_pauli_op(wc=1.0, g=0.05, J=0.1)
    
    # Convert to matrix form for validation
    matrix = H.to_matrix()
    
    # Check if the matrix is equal to its conjugate transpose
    is_hermitian = np.allclose(matrix, matrix.conj().T)
    
    assert is_hermitian, "The generated JCH Hamiltonian is not Hermitian!"