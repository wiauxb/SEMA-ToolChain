import argparse
import sys

from src import SemaMutator


class ArgumentParserMutator:
    
    def __init__(self, tool_mutator):
        self.parser = argparse.ArgumentParser(description="Mutation module arguments")
        #self.parser._optionals.title = "SCDG module arguments"
        
        self.group = self.parser.add_argument_group('Traces Parameters')

        self.group.add_argument(
            "binary",
            help="Path to the Binary to mutate",
            default="/src"
        )

        #TODO handle multiple trace
        self.group.add_argument(
            "--trace",
            help="Add a trace (usage: <name of trace> <symbolic arg> <args>)"
        )

        self.group.add_argument(
            "--binaries_mutated",
            help="Path to the mutated binaries",
            default="output/runs/"
        )
    
        self.tool_mutator = tool_mutator

    def update_tool(self,args):
        self.tool_mutator.binary = args.binary
        self.tool_mutator.traces = args.trace
        self.tool_mutator.output = args.binaries_mutated + "/"

    def parse_arguments(self, allow_unk = False, args_list=None):
        args = None
        if not allow_unk:
            args = self.parser.parse_args(args_list)
        else:
            args, unknown = self.parser.parse_known_args(args_list)

        return args
    

def main():
    toolm = SemaMutator(
        print_sm_step=True,
        print_syscall=True,
        debug_error=True,
        debug_string=True,
        print_on=True,
        is_from_web=False
    )
    args_parser = ArgumentParserMutator(toolm)
    args = args_parser.parse_arguments()
    args_parser.update_tool(args)
    # toolm.start_scdg(args, is_fl=False,csv_file=None)


if __name__ == "__main__":
    
    main()
            