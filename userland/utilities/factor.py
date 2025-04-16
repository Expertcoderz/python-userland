import math
from typing import Generator, Iterable, cast

from .. import core


# List of small primes greater than 2; used for lookup.
SMALL_PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


def miller_rabin(n: int) -> bool:
    """
    A deterministic version of the Miller-Rabin primality test.
    """
    d = n - 1
    s = 0

    while d & 1 == 0:
        d >>= 1
        s += 1

    for a in (x % n + 2 for x in range(50)):
        if pow(a, d, n) == 1:
            continue

        for i in range(s):
            if pow(a, 2**i * d, n) == n - 1:
                break
        else:
            return False

    return True


def pollards_rho(n: int, step: int) -> int | None:
    """
    Pollard's rho algorithm for factorization.

    Assumes that n is an odd integer greater than 2.
    """
    x = y = 2
    factor = 1
    while factor == 1:
        x = (x * x + step) % n
        y = ((y * y + step) ** 2 + step) % n
        factor = math.gcd(abs(x - y) % n, n)

    return factor


def factorize(
    n: int, cache: dict[int, int] = {p: p for p in SMALL_PRIMES}
) -> Generator[int]:
    """
    Generates prime factors of the integer n.

    Results may not be in strictly ascending order.
    """
    while n > 1:
        factor: int | None = None

        if n & 1 == 0:
            yield (factor := 2)
        elif factor := cache.get(n):
            yield factor
        else:
            if miller_rabin(n):
                cache[n] = factor = n
                yield factor
            else:
                for i in range(1, n - 1):
                    if (factor := pollards_rho(n, i)) and factor != n:
                        yield from factorize(min(n, factor), cache)
                        break

        if factor == n:
            break

        n //= cast(int, factor)


def format_exponents(factors: Iterable[int]) -> str:
    processed: list[str] = []

    last_factor = 0
    exp = 0

    for factor in factors:
        if exp and last_factor != factor:
            processed.append(f"{last_factor}{"" if exp == 1 else f"^{exp}"}")
            exp = 1
        else:
            exp += 1

        last_factor = factor

    processed.append(f"{last_factor}{"" if exp == 1 else f"^{exp}"}")

    return " ".join(processed)


parser = core.ExtendedOptionParser(
    usage="%prog [OPTION] [NUMBER]...",
    description="Compute and print the prime factors of each positive integer NUMBER.",
)

parser.add_option("-h", "--exponents", action="store_true")


@core.command(parser)
def python_userland_factor(opts, args: list[str]) -> int:
    failed = False

    for arg in args or core.readwords_stdin():
        try:
            num = int(arg)
            if num < 0:
                raise ValueError
        except ValueError:
            failed = True
            core.perror(f"'{arg}' is not a valid positive integer")
            continue

        if num < 2:
            print(f"{num}:")
            continue

        factors = sorted(factorize(num))

        print(
            f"{num}: {format_exponents(factors) if opts.exponents
            else " ".join(map(str, factors))}"
        )

    return int(failed)
