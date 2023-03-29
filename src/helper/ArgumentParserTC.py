
import argparse

try:
    from SemaSCDG.helper.ArgumentParserSCDG import ArgumentParserSCDG
    from SemaClassifier.helper.ArgumentParserClassifier import ArgumentParserClassifier
    from SemaMutater.helper.ArgumentParserMutater import ArgumentParserMutater
except:
    from src.SemaSCDG.helper.ArgumentParserSCDG import ArgumentParserSCDG
    from src.SemaClassifier.helper.ArgumentParserClassifier import ArgumentParserClassifier
    from src.SemaMutater.helper.ArgumentParserMutater import ArgumentParserMutater

class ArgumentParserTC:

    def __init__(self,tcw,tcc,tcm):
        self.tool_mutate = tcm
        self.args_parser_mutater = ArgumentParserMutater(tcm)        
        self.tool_scdg = tcw
        self.args_parser_scdg = ArgumentParserSCDG(tcw)
        self.tool_classifier = tcc
        self.args_parser_class = ArgumentParserClassifier(tcc)
        self.parser = argparse.ArgumentParser(conflict_handler='resolve',
                                parents=[self.args_parser_mutater.parser,
                                         self.args_parser_scdg.parser,
                                         self.args_parser_class.parser]) 
    
    # TODO conflict with --exp_dir and binaries arguments 
    def parse_arguments(self, allow_unk=False,args_list=None):
        args = None
        if not allow_unk:
            args = self.parser.parse_args(args_list) 
        else:
            args, unknown = self.parser.parse_known_args(args_list)
        return args