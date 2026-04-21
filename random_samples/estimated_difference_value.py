

def estimated_difference_value(number_of_samples: int, dimensions: int = 2, p_norm: int = 2, repeats: int = 100) -> np.ndarray:
    """use p norm to calculate distance between two points."""

    if number_of_samples % 2 == 1:
        number_of_samples += 1

    samples = generate_samples(number_of_samples * repeats, dimensions, p_norm)
    # samples.reshape(repeats, number_of_samples, dimensions)

    paired = samples.reshape(repeats, number_of_samples // 2, 2, dimensions)
    return np.linalg.norm(paired[:, :, 0] - paired[:, :, 1], ord=p_norm, axis=-1).mean(axis=0)
