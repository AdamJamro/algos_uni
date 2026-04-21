from randomness_config import *

def falling_into_unit_ball_probability(dimension: int, p_ord = 2, number_of_samples: int = 10) -> float:
    p_norm = lambda _vec: np.linalg.norm(_vec, ord=p_ord, axis=-1)
    sample_vec = random_sample(number_of_samples * dimension).reshape((number_of_samples, dimension))

    probability_unit_ball = (p_norm(sample_vec) <= 1.0).mean()
    return probability_unit_ball


def sample_random_points_norm_on_uniform_square_sidelength2(dimension: int, p_ord = 2, number_of_samples: int = 10) -> np.ndarray:
    p_norm = lambda _vec: np.linalg.norm(_vec, ord=p_ord, axis=-1)
    sample_vec = random_sample(number_of_samples * dimension).reshape((number_of_samples, dimension)) * 2 - 1
    return p_norm(sample_vec)
