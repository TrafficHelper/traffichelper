import cli
from Code import loader
from Code.Atomic.gadget import Gadget
from Code.mutation import Mutation

def run():
    cline = cli.CLI()
    cline.repl()

if __name__ == '__main__':
    # nt = loader.LOADED_TRAFFIC_NETWORK
    # m = Mutation(nt, list(nt.edges)[0],[Gadget.STOP_LIGHT], [], False)
    # m.apply()
    run()