import docker, logging


class SemaMutator:

    args = {}

    binary = ""
    traces = []
    output = ""

    log = logging.getLogger("SemaMutator")

    def print_args(self):
        print("="*20)
        print(self.args)
        print("-"*20)
        print(self.binary)
        print(self.traces)
        print(self.output)
        print("="*20)

    def start_mutation(self):
        client = docker.from_env()
        
        res = client.containers.run("binrec", ["sh", "-c", f"just new-project test {self.binary} && just add-trace test {self.traces} && just recover test"],
                                    environment=["TERM=linux", "TERMINFO=/etc/terminfo"], remove=True)
        for l in res.splitlines():
            SemaMutator.log.info(l)