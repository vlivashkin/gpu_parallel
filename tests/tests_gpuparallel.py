import multiprocessing as mp
import unittest
from functools import partial

from gpuparallel import GPUParallel


def test_init__init(worker_id=None, gpu_id=None):
    global result
    result = worker_id


def test_init__perform(worker_id=None, gpu_id=None):
    global result
    mp.get_logger().info(f'Perform {result}')
    return result


def test_results__perform(idx, worker_id=None, gpu_id=None):
    mp.get_logger().info(f'Perform {idx}')
    return idx


def test_multicall__perform(idx, worker_id=None, gpu_id=None):
    mp.get_logger().info(f'Perform {idx}')
    return idx


class TestGPUParallel(unittest.TestCase):
    def test_init(self):
        print('Run Test: test_init')

        results = GPUParallel(n_gpu=2, init_fn=test_init__init)(test_init__perform for _ in range(10))
        self.assertEqual(set(results), {0, 1})

    def test_results(self):
        print('Run Test: test_results')

        true_seq = list(range(10))
        results = GPUParallel(n_gpu=2)(partial(test_results__perform, idx) for idx in true_seq)
        self.assertEqual(sorted(results), true_seq)

    def test_multicall(self):
        print('Run Test: test_multicall')

        true_seq1, true_seq2 = list(range(10)), list(range(10, 20))
        gp = GPUParallel(n_gpu=2)
        results = gp(partial(test_multicall__perform, idx) for idx in true_seq1)
        self.assertEqual(sorted(results), true_seq1)
        results = gp(partial(test_multicall__perform, idx) for idx in true_seq2)
        self.assertEqual(sorted(results), true_seq2)


if __name__ == '__main__':
    unittest.main()
