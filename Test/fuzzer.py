# A fuzzer based on https://www.fuzzingbook.org/html/Fuzzer.html

import random
from typing import List, Tuple, Any
import subprocess


class Runner:
    """Base class for testing inputs."""

    # Test outcomes
    PASS = "PASS"
    FAIL = "FAIL"
    UNRESOLVED = "UNRESOLVED"

    def __init__(self) -> None:
        """Initialize"""
        pass

    def run(self, inp: str) -> Any:
        """Run the runner with the given input"""
        return (inp, Runner.UNRESOLVED)


class PrintRunner(Runner):
    """Simple runner, printing the input."""

    def run(self, inp) -> Any:
        """Print the given input"""
        print(inp)
        return (inp, Runner.UNRESOLVED)


class Fuzzer:
    """Base class for fuzzers."""

    def __init__(self) -> None:
        """Constructor"""
        pass

    def fuzz(self) -> str:
        """Return fuzz input"""
        return ""

    def run(self, runner: Runner = Runner()) -> Tuple[subprocess.CompletedProcess, Any]:
        """Run `runner` with fuzz input"""
        return runner.run(self.fuzz())

    def runs(
        self, runner: Runner = PrintRunner(), trials: int = 10
    ) -> List[Tuple[subprocess.CompletedProcess, Any]]:
        """Run `runner` with fuzz input, `trials` times"""
        return [self.run(runner) for i in range(trials)]


class RandomFuzzer(Fuzzer):
    """Produce random inputs."""

    def __init__(
        self,
        min_length: int = 10,
        max_length: int = 100,
        char_start: int = 32,
        char_range: int = 32,
    ) -> None:
        """Produce strings of `min_length` to `max_length` characters
        in the range [`char_start`, `char_start` + `char_range`)"""
        self.min_length = min_length
        self.max_length = max_length
        self.char_start = char_start
        self.char_range = char_range

    def fuzz(self) -> str:
        string_length = random.randrange(self.min_length, self.max_length + 1)
        out = ""
        for i in range(0, string_length):
            out += chr(
                random.randrange(self.char_start, self.char_start + self.char_range)
            )
        return out


if __name__ == "__main__":
    fuzzer = RandomFuzzer(min_length=10, max_length=20, char_start=65, char_range=26)
    print(fuzzer.fuzz())
