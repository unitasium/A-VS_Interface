from abaqus import *
from customKernel import CommandRegister, RepositorySupport

class Block(CommandRegister):
    def __init__(self, name):
        CommandRegister.__init__(self)

class Model(RepositorySupport):
    def __init__(self, name):
        RepositorySupport.__init__(self)
        self.Repository('blocks', Block)
