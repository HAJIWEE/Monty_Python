class ToDo:

    comTd = 0

    def __init__(self, description, idx, status):
        self.description = description
        self.done = status
        self.idx = idx

    def chg_idx(self, new):
        self.idx = new

    def completed(self):
        self.done = True
        self.progress('a')

    def undone(self):
        self.done = False
        self.progress('m')

    def value(self):
        d = 'X' if self.done else '-'
        return f'{d}'.center(7, ' ') + '|' + f'{self.idx}'.center(7, ' ') + '| ' + ' '.join(self.description).ljust(28,' ') + '| ' + '-'.center(13, ' ')

    def com(self):
        d = 'X' if self.done else '-'
        return [f'{self.idx}'.center(3, ' '), f'{d}'.center(6, ' '), '-'.center(17, ' '), ' '.join(self.description)]

    def progress(self, prog):
        if prog == 'a':
            ToDo.comTd = ToDo.comTd + 1
        elif ToDo.comTd >= 1:
            ToDo.comTd = ToDo.comTd - 1


class Deadline(ToDo):

    comDL = 0

    def __init__(self, description, idx, date, status):
        super().__init__(description,idx,status)
        self.deadline = date

    def value(self):
        d = 'X' if self.done else '-'
        return f'{d}'.center(7, ' ') + '|' + f'{self.idx}'.center(7, ' ') + '| ' + ' '.join(self.description).ljust(28,' ') + '| ' + ''.join(self.deadline).center(13, ' ')

    def com(self):
        d = 'X' if self.done else '-'
        return [f'{self.idx}'.center(3, ' '), f'{d}'.center(6, ' '), ''.join(self.deadline).center(17, ' '),
                ' '.join(self.description)]

    def progress(self, prog):
        if prog == 'a':
            Deadline.comDL = Deadline.comDL + 1
        elif Deadline.comDL >= 1:
            Deadline.comDL = Deadline.comDL - 1
