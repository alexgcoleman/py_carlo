from py_carlo.sim import Simulation
import py_carlo.situ.coin as coin

from functools import partial


def check_for_3_in_5() -> bool:
    return coin.check_for_n_consecutive(
        flips=coin.flip_n_coins(5),
        result='HEADS',
        n=3
    )


def main() -> None:
    sim = Simulation(
        num_sims=100,
        num_runs=5,
        sim_function=check_for_3_in_5
    )

    sim.run()

    stats = sim.result_stats()
    print(stats)

    return


if __name__ == "__main__":
    main()
