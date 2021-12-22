# TODO: сделать классы ошибок


class SideNameError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        result = 'Incorrect name of side (should be R, L, U, D, F, B)'
        if self.message:
            result += f'. {self.message}'

        return result
