import numpy as np
from qiskit.quantum_info import SparsePauliOp

def get_jch_pauli_op(wc: float, g: float, J: float) -> SparsePauliOp:
    """
    Constructs a 2-site Jaynes-Cummings-Hubbard Hamiltonian.
    Qubit mapping (4 qubits total):
    - Qubit 0: Site 0 Atom
    - Qubit 1: Site 0 Photon
    - Qubit 2: Site 1 Atom
    - Qubit 3: Site 1 Photon
    """
    # 1. Site Energy: wc * (a'a + 0.5*sz)
    # n = 0.5(I - Z), sz = Z
    h_energy = wc * 0.5 * (SparsePauliOp("IIII") - SparsePauliOp("IZII")) # Site 0 Photon
    h_energy += wc * 0.5 * SparsePauliOp("ZIII")                         # Site 0 Atom
    h_energy += wc * 0.5 * (SparsePauliOp("IIII") - SparsePauliOp("IIIZ")) # Site 1 Photon
    h_energy += wc * 0.5 * SparsePauliOp("IIZI")                         # Site 1 Atom

    # 2. Jaynes-Cummings Interaction: g * (a'sm + asm') -> Maps to 0.5 * g * (XX + YY)
    h_int = 0.5 * g * (SparsePauliOp("XXII") + SparsePauliOp("YYII"))    # Site 0
    h_int += 0.5 * g * (SparsePauliOp("IIXX") + SparsePauliOp("IIYY"))   # Site 1

    # 3. Hopping Interaction: -J * (a0' a1 + a1' a0) -> Maps to -0.5 * J * (IXIX + IYIY)
    h_hop = -0.5 * J * (SparsePauliOp("IXIX") + SparsePauliOp("IYIY"))   # Between Photons

    # Combine and simplify the Pauli strings
    H_total = (h_energy + h_int + h_hop).simplify()
    
    return H_total