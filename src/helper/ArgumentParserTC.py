
import argparse
from enum import Enum

try:
    from SemaSCDG.helper.ArgumentParserSCDG import ArgumentParserSCDG
    from SemaClassifier.helper.ArgumentParserClassifier import ArgumentParserClassifier
    from src.SemaMutator.helper.ArgumentParserMutator import ArgumentParserMutator
except:
    from src.SemaSCDG.helper.ArgumentParserSCDG import ArgumentParserSCDG
    from src.SemaClassifier.helper.ArgumentParserClassifier import ArgumentParserClassifier
    from src.SemaMutator.helper.ArgumentParserMutator import ArgumentParserMutator

class ArgumentParserTC:

    def __init__(self,tcw,tcc,tcm):
        self.tool_mutate = tcm
        self.args_parser_mutator = ArgumentParserMutator(tcm)        
        self.tool_scdg = tcw
        self.args_parser_scdg = ArgumentParserSCDG(tcw)
        self.tool_classifier = tcc
        self.args_parser_class = ArgumentParserClassifier(tcc)
        # self.parser = argparse.ArgumentParser(conflict_handler='resolve',
        #                         parents=[self.args_parser_mutator.parser,
        #                                  self.args_parser_scdg.parser,
        #                                  self.args_parser_class.parser])
        self.tools = Enum('tools', ['MUTATOR', 'SCDG', 'CLASSIFIER'])
        self._enabled = []

    def reset(self):
        self._enabled = []

    def enable(self, tool):
        if tool not in self.tools:
            raise  ValueError(f"{tool} is not a valid tool type.")
        if tool not in self._enabled:
            self._enabled.append(tool)

    def disable(self, tool):
        if tool not in self.tools:
            raise  ValueError(f"{tool} is not a valid tool type.")
        if tool in self._enabled:
            self._enabled.remove(tool)
    
    # TODO conflict with --exp_dir and binaries arguments 
    # def parse_arguments(self, allow_unk=False,args_list=None):
    #     args = None
    #     if not allow_unk:
    #         args = self.parser.parse_args(args_list) 
    #     else:
    #         args, unknown = self.parser.parse_known_args(args_list)
    #     return args

    def parse_arguments(self, allow_unk=False,args_list=None):
        args = {}
        for tool in self._enabled:
            if tool == self.tools.MUTATOR:
                args[tool] = self.parse_arguments_with(self.args_parser_mutator.parser, allow_unk, args_list)
            elif tool == self.tools.SCDG:
                args[tool] = self.parse_arguments_with(self.args_parser_scdg.parser, allow_unk, args_list)
            elif tool == self.tools.CLASSIFIER:
                args[tool] = self.parse_arguments_with(self.args_parser_class.parser, allow_unk, args_list)
        return args
    
    def parse_arguments_with(self, parser, allow_unk=False,args_list=None):
        args = None
        if not allow_unk:
            args = parser.parse_args(args_list) 
        else:
            args, unknown = parser.parse_known_args(args_list)
        return args