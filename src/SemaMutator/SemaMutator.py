import docker, logging, requests

import subprocess

class SemaMutator:

    args = {}

    binary = ""
    traces = []
    mutant_number = 1
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
        
        
        r = requests.post("http://172.17.0.2:8080/add-project", json={"project":"test",
                                                              "path": self.binary})
        
        r = requests.post("http://172.17.0.2:8080/projects/test/add-trace", json={"trace_name":"tr1",
                                                                "trace_args": self.traces[0],
                                                                "trace_symbolic_args": self.traces[1]})

        r = requests.get(f"http://172.17.0.2:8080/projects/test/mutations/{self.mutant_number}")
        
        print(r)
        print("+"*20)
        print(r.json())

        print("Mutation finished")