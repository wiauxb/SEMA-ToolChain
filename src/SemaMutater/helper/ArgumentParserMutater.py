import argparse
import sys


class ArgumentParserMutater:
    
    def __init__(self, tool_mutater):
        self.parser = argparse.ArgumentParser(description="Mutation module arguments")
        #self.parser._optionals.title = "SCDG module arguments"
        
        self.group = self.parser.add_argument_group('Traces Parameters')

        self.group.add_argument(
            "--path",
            help="Path to the Binary to mutate",
            required=True
        )

        self.group.add_argument(
            "--trace",
            help="Add a trace",
            action="append",
            required=True
        )
    
        self.tool_mutater = tool_mutater

    def update_tool(self,args):
        self.tool_mutater.path = args.path
        self.tool_mutater.traces = args.trace

    def parse_arguments(self, allow_unk = False, args_list=None):
        args = None
        if not allow_unk:
            args = self.parser.parse_args(args_list)
        else:
            args, unknown = self.parser.parse_known_args(args_list)

        return args
