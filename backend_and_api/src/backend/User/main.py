from backend.Code import loader
from backend.Code.Atomic.gadget import Gadget
from backend.Code.mutation import Mutation
from backend.User import cli


def run():
    cline = cli.CLI()
    cline.repl()

if __name__ == '__main__':
    nt = loader.LOADED_TRAFFIC_NETWORK
    m = Mutation(nt, list(nt.edges)[0],[], [], True)
    res = m.apply(True)
    print(res)
    # run()
