from backend.User import cli

run = lambda: cli.CLI().repl() # Create CLI instance and run it

if __name__ == '__main__':
    run()
