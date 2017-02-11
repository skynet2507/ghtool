class Base(object):

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError('run() method must be implemented')

    def options(self):
        return self.options

    def arguments(self):
        return self.args

    def kwargs(self):
        return self.kwargs