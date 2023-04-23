import docker, logging, requests

import subprocess

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
        
        # res = client.containers.run("binrec",
        #                             ["sh", "-c", f"just new-project test {self.binary} && just add-trace test {self.traces} && just recover test && mv s2e/projects/test/s2e-out/recovered {self.output}"],
        #                             environment=["TERM=linux", "TERMINFO=/etc/terminfo"],
        #                             volumes=["/app/src:/app/src"],
        #                             remove=True)
        
        r = requests.post("http://172.17.0.2:8080/add-project", json={"project":"test",
                                                              "path":"programs/mult_func"})
        
        print(r)
        print("+"*20)
        print(r.json())

        print("Mutation finished")