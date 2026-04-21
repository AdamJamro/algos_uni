from hilbert_space_utils import np
from hilbert_space_utils.dot_product import dot_product
from hilbert_space_utils.gram_schmidt_algorithm import gram_schmidt_algorithm


def project(vector, subspace_basis):
    """
    Project a vector onto a subspace defined by an orthonormal basis.

    Parameters:
    vector (array-like): The vector to be projected.
    subspace_basis (array-like): An array of orthonormal vectors that form the basis of the subspace.

    Returns:
    numpy.ndarray: The projection of the vector onto the subspace.
    """
    projection = np.zeros_like(vector, dtype=vector.dtype)
    for basis_vector in subspace_basis:
        project_constant = dot_product(vector, basis_vector)
        projection += project_constant * basis_vector
    return projection


if __name__ == "__main__":
    from gram_schmidt_algorithm import gram_schmidt_algorithm
    basis_0 = gram_schmidt_algorithm([np.random.random_sample(3) for _ in range(3)])
    print(basis_0)
    print(basis_0.dtype)
    input_data = [
        (np.array([1, 1, 0], dtype=basis_0.dtype), basis_0),
        (np.array([1, 0, 1], dtype=basis_0.dtype), basis_0),
        (np.array([0, 1, 1], dtype=basis_0.dtype), basis_0),
        (np.array([1, 2, 3], dtype=basis_0.dtype), basis_0)
    ]

    for vec, subspace_basis in input_data:
        print(f"Test {vec=}, {subspace_basis=}")
        projected_vector = project(vec, subspace_basis)
        assert np.allclose(projected_vector, project(projected_vector, subspace_basis))
        assert dot_product(projected_vector, projected_vector - vec) < 10e-10
        print("Projected vector:", projected_vector)
        print()
