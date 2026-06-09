from typing import Generator

import numpy as np


class PrimeGenerator:
    def __init__(self):
        self.prime_cache = {2, 3}
        self.cached_range = 3

    def __call__(self, n: int) -> Generator[int, None, None]:
        if self.cached_range < n:
            self.fill_sieve(n)

        yield from (prime for prime in self.prime_cache if prime <= n)

    @property
    def cached_primes(self):
        return sorted(self.prime_cache)

    def fill_sieve(self, n: int):
        self.prime_cache.update(range(self.cached_range + 2, n + 1))
        for prime in sorted(self.prime_cache):
            if prime not in self.prime_cache:
                continue
            for j in range(max(self.cached_range + prime - self.cached_range % prime, prime * prime), n + 1, prime):
                self.prime_cache.discard(j)

        self.cached_range = n


def find_prime_factors(n: int, prime_gen=PrimeGenerator()) -> set[int]:
    """finds all unique prime factors of n"""
    factors = set()

    for i in prime_gen(n):
        if i * i > n:
            break
        while n % i == 0:
            factors.add(i)
            n //= i

    if n > 2:
        factors.add(n)

    return factors


def find_generators(p, prime_gen=PrimeGenerator()):
    """
    Outputs all generators of the multiplicative group Z_p*.
    """
    if p == 2:
        return [1]

    phi = p - 1
    factors = find_prime_factors(phi, prime_gen)
    generators = []

    for g in range(2, p):

        is_generator = True

        # lagrange theorem states that if g is a generator, then g^(phi/q) != 1 for every prime factor q of phi
        for q in factors:
            # g^((p-1)/q) mod p
            # phi // q these are sizes of the biggest Z_p* subgroups and
            if pow(g, phi // q, p) == 1:
                is_generator = False
                break

        if is_generator:
            generators.append(g)

    return generators

def test_prime_generator():
    prime_gen = PrimeGenerator()
    test_primes = list(prime_gen(200))
    print(test_primes)
    assert all(all(alleged % i != 0 for i in range(2, int(alleged**0.5) + 1)) for alleged in test_primes)
    print()


if __name__ == "__main__":
    primes_gen = PrimeGenerator()
    primes = list(primes_gen(5))
    p = primes[-1]
    gen_list = find_generators(p, primes_gen)
    print(f"Liczba pierwsza: {p}")
    print(f"Liczba generatorów: {len(gen_list)}")
    print(f"Generatory grupy Z_{p}^*: {gen_list}")

    totient = len(list(i for i in range(1, p - 1) if np.gcd(i, p - 1) == 1))
    assert totient == len(gen_list)
    for generator in gen_list:
        print(f"Testing generator {generator}...")
        assert all(pow(generator, (p - 1) // q, p) != 1 for q in primes_gen(p - 1))
        assert len(set(pow(generator, k, p) for k in range(1, p))) == p - 1


