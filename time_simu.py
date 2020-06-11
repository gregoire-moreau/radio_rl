from timeit import default_timer as timer
from model_cpp.model_env_cpp import CellEnvironment


def _test_reset(env):
    env.reset(-1)


def _test_no_treat(env):
    env.reset(-1)
    while not env.inTerminalState():
        env.act(0)


def _test_max_treat(env):
    env.reset(-1)
    while not env.inTerminalState():
        env.act([1, 0])

def _test_timeout(env):
    env.reset(-1)
    while not env.inTerminalState():
        env.act(3)

def time_test(fun, env, count):
    start = timer()
    for i in range(count):
        fun(env)
    end = timer()
    return (end-start)/count

if __name__ == '__main__':
    env = CellEnvironment('types', False, 'dose', 'DQN', False, False, False)
    print("Average time to reset:", 1000 * time_test(_test_reset, env, 100), "milliseconds")
    print("Average time without treatment:", 1000 * time_test(_test_no_treat, env, 100), "milliseconds")
    print("Average time in timeout:", 1000 * time_test(_test_timeout, env, 100), "milliseconds")
    env.action_type = 'AC'
    print("Average time with max treatment:", 1000 * time_test(_test_max_treat, env, 100), "milliseconds")
    env.end()
