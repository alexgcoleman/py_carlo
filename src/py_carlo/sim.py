from __future__ import annotations
import random

import pandas as pd

from dataclasses import dataclass


from typing import Callable, Optional, List, Any


@dataclass
class SimResult:
    """Result from a single simulation"""
    sim_id: int
    result: Any

    def as_series(self) -> pd.Series:
        return pd.Series({
            'sim_id': self.sim_id,
            'result': self.result
        })


@dataclass
class RunResult:
    """Result from a batch of simulations"""
    run_id: int
    results: List[SimResult]

    def as_df(self) -> pd.DataFrame:
        df = (
            pd.concat([
                sim.as_series()
                for sim in self.results], axis=1)
            .transpose()
            .assign(run_id=self.run_id)
        )
        return df[['run_id', 'sim_id', 'result']]


@dataclass
class CarloResult:
    """Results from a set of runs - completed 
    monte carlo simulations"""
    num_runs: int
    num_sims: int
    results: List[RunResult]

    def as_df(self) -> pd.DataFrame:

        df = pd.concat([
            result.as_df() for result in self.results
        ])

        return df


class NoResultsError(Exception):
    def __init__(self) -> None:
        super().__init__("No results, please `.run()` first")


class Simulation:
    """Class for running and storing results for the monte carlo simulations."""
    seed: int
    num_sims: int
    num_runs: int
    results: Optional[CarloResult]

    def __init__(self,
                 sim_function: Callable,
                 num_sims: int,
                 num_runs: int = 1,
                 seed: Optional[int] = None) -> None:
        """Initializes an empty simulation, and sets an optional seed"""
        if seed is None:
            seed = 451

        random.seed(seed)
        self.seed = seed
        self.sim_function = sim_function
        self.num_sims = num_sims
        self.num_runs = num_runs

    def _run_sims(self):
        return [SimResult(sim_id, self.sim_function()) for sim_id in range(self.num_sims)]

    def run(self) -> None:
        self.results = CarloResult(
            num_sims=self.num_sims,
            num_runs=self.num_runs,
            results=[RunResult(run_id, self._run_sims())
                     for run_id in range(self.num_runs)]
        )

    def result_stats(self) -> pd.DataFrame:
        if self.results is None:
            raise NoResultsError

        results_df = self.results.as_df()
        stats = results_df.groupby('run_id')['result'].value_counts()
        return stats
