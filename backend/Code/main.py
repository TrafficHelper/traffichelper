import loader

def run():
    loader.Loader.load()


class Foo:
    def __init__(self, i):
        self.i = i

    def __eq__(self, other):
        return self.i == other.i

    def __hash__(self):
        return self.i, self.i

if __name__ == '__main__':
    # s = {*()}
    # s.add(Foo(0))
    # s.add(Foo(0))
    # print(s)
    run()
