from abc import ABC, abstractmethod
from typing import List


class Permission(ABC):

    @abstractmethod
    def is_allowed(self, letter: str) -> bool:
        pass


class Any(Permission):

    def is_allowed(self, letter: str) -> bool:
        return True


class Not(Permission):

    def __init__(self, letter: str) -> None:
        self.letter = letter
        super().__init__()

    def is_allowed(self, letter: str) -> bool:
        return letter != self.letter


class Exactly(Permission):

    def __init__(self, letter: str) -> None:
        self.letter = letter
        super().__init__()

    def is_allowed(self, letter: str) -> bool:
        return letter == self.letter


class Restriction(ABC):

    @abstractmethod
    def conforms(self, word: str) -> bool:
        pass


class Contains(Restriction):

    def __init__(self, letter: str) -> None:
        self.letter = letter

    def conforms(self, word: str) -> bool:
        return self.letter in word


class DoesNotContain(Restriction):

    def __init__(self, letter: str) -> None:
        self.letter = letter

    def conforms(self, word: str) -> bool:
        return self.letter not in word


class WordConfig:
    permissions = [[Any()], [Any()], [Any()], [Any()], [Any()]]
    restrictions = []

    def conforms(self, word: str) -> bool:
        for restriction in self.restrictions:
            if not restriction.conforms(word=word):
                return False

        for i, letter in enumerate(word):
            for permission in self.permissions[i]:
                if not permission.is_allowed(letter=letter):
                    return False

        return True


class Game:
    def __init__(self):
        self.__word_config = WordConfig()
        with open('a.txt') as file:
            self.words = file.readlines()
            self.words = list(map(lambda x: x.strip(), self.words))

    def solve(self, verbose: int):
        initial_count = len(self.words)
        self.words = list(filter(lambda w: self.__word_config.conforms(word=w), self.words))

        if verbose > 1:
            for i, word in enumerate(self.words):
                print(i + 1, word)

        if verbose > 0:
            print(f'Possible words count: {initial_count} -> {len(self.words)}')

    def add_permission(self, index: int, permission: Permission):
        self.__word_config.permissions[index].append(permission)

    def add_restriction(self, restriction: Restriction):
        self.__word_config.restrictions.append(restriction)


def print_help():
    print('What to do?')
    print('[1] Add permission')
    print('[2] Add restriction')
    print('[3] Solve (or just enter)')
    print('[? or h] Show help')

def main():
    game = Game()

    is_gaming = True

    while is_gaming:
        print_help()

        command = input()

        match command:
            case '1':
                print('Adding permission')
                print('Write index and letter. For example:')
                print('5 a, if the fifth letter is `a`')
                print('2 -k, if the second letter is not `k`')
            case '2':
                print('Adding restriction')
                print('Write a letter. For example:')
                print('a, if the word contains `a`')
                print('-k, if the word does not contain `k`')
            case '?' | 'h':
                print_help()
            case _:
                if len(command) == 0:
                    game.solve(verbose=2)
                elif command[0].isdigit():
                    # adding permission
                    permission_index, permission_letters = command.split()

                    if permission_letters.startswith('-'):
                        for letter in permission_letters[1:]:
                            permission = Not(letter=letter)
                            game.add_permission(index=int(permission_index) - 1, permission=permission)
                            restriction = Contains(letter=letter)
                            game.add_restriction(restriction=restriction)
                    else:
                        permission = Exactly(letter=permission_letters[0])
                        game.add_permission(index=int(permission_index) - 1, permission=permission)

                elif command[0].isalpha() or command[0] == '-':
                    # adding restriction

                    if command.startswith('-'):
                        for letter in command[1:]:
                            restriction = DoesNotContain(letter=letter)
                            game.add_restriction(restriction=restriction)
                    else:
                        for letter in command:
                            restriction = Contains(letter=letter)
                            game.add_restriction(restriction=restriction)

                else:
                    game.solve(verbose=2)

if __name__ == '__main__':
    main()