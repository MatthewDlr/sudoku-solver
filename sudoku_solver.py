
from typing import List
from colorama import Fore, Style # to import

class Sudoku : 
    def __init__(self, grid: List[List[str]] ):
        try : self.sudoku_str = self.convert_grid_to_str(grid)
        except : raise ValueError("Your sudoku has not the supported format and cannot be solve. Please look at the data type in 'sudoku_grids.py'.")

    def solve(self) :
        prefilled_cells = self.get_number_of_filled_cell()
        if prefilled_cells < 17 : raise ValueError("Not enough prefilled cell to solve the sudoku")

        sudoku = list(self.sudoku_str)
        original_sudoku = self.sudoku_str       
        index = 0
        iteration = 0 # Just to count the number of calculus the program made
        uncertain_moves = {}
        backtracking = False
        while index >= 0 and index < 81 :
            iteration += 1
            if self.sudoku_str[index].isnumeric() : # The values prefilled from the original sudoku
                print(index, self.sudoku_str[index], "Given number")
            elif index not in uncertain_moves and backtracking : # An edge case that was blocking the algo when backtracking
                print("Pass")
            else : 
                possible_numbers = self.find_possible_numbers(index, "".join(sudoku), original_sudoku)

                if len(possible_numbers) == 0 : 
                    backtracking = True
                elif len(possible_numbers) == 1 : 
                    sudoku[index] = str(possible_numbers[0])
                    print("Perfect solution found")
                    backtracking = False
                else :
                    if index not in uncertain_moves :
                        sudoku[index] = str(possible_numbers[0])
                        uncertain_moves[index] = 0
                        print("Solution is uncertain -> ", sudoku[index])
                        backtracking = False
                    else : 
                        max_length = len(possible_numbers)
                        previous_choice_index = uncertain_moves[index]
                        new_choice_index = previous_choice_index + 1

                        if new_choice_index < max_length :
                            uncertain_moves[index] = new_choice_index
                            sudoku[index] = str(possible_numbers[new_choice_index])
                            print("Taking the next solution -> ", sudoku[index])
                            for i in range(index+1, len(sudoku)):
                                if i in uncertain_moves: del uncertain_moves[i]
                            backtracking = False
                        else : 
                            print("No possibilities left")
                            backtracking = True
                
            if backtracking :
                index -= 1
                print("Backtracking to previous index:", index)
            else : 
                index += 1 

        self.sudoku_str = "".join(sudoku)
        if self.get_number_of_filled_cell() == 81 and index == 81 :
            print("Sudoku solved in", iteration, "iterations ✅ \n")
        else :
            print("The resolution failed or sudoku is unsolvable ❌")

        self.print_sudoku(self.sudoku_str, original_sudoku)

    def get_number_of_filled_cell(self) -> int :
        count = 0
        for char in list(self.sudoku_str) :
            if char.isnumeric(): count += 1
        return count

    # For a given cell, the function return all possible numbers that are not violating sudoku's rules
    def find_possible_numbers(self, index: int, sudoku: str, original_sudoku: str) -> List[int] :
        row_numbers = self.get_used_numbers(Row(index, sudoku, original_sudoku).values)
        column_numbers = self.get_used_numbers(Column(index, sudoku, original_sudoku).values)
        section_numbers = self.get_used_numbers(Section(index, sudoku, original_sudoku).values)
        total_numbers: set[int] = set(row_numbers + column_numbers + section_numbers)
        possible_answers = list(set([1,2,3,4,5,6,7,8,9]) - total_numbers)
        print(index, possible_answers, end=' ')
        return possible_answers
    
    def get_used_numbers(self, input: List[str]) -> List[int] :
        results = []
        for value in input : 
            try:
                value = int(value)
                if value in results : raise ValueError("Found twice the same value in the group: " + str(input))
                else : results.append(value)
            except ValueError: continue
        return results
        
    def convert_grid_to_str(self, grid: List[List[str]] ) -> str :
        sudoku_str: str = ""
        for row in grid :
            for digit in row :
                if digit == "0" or digit.strip() == "" or digit == "." :
                    sudoku_str += "."
                else :
                    sudoku_str += digit

        return sudoku_str
    
    # This function is AI-generated
    def print_sudoku(self, sudoku_str: str, original_sudoku : str):
        if len(sudoku_str) != 81: raise ValueError("The input string must be exactly 81 characters long.")

        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-"*21)
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")  
                if sudoku_str[i*9 + j] == '.':  
                    print(Fore.RED + 'X' + " ", end="")
                elif sudoku_str[i*9 + j] != original_sudoku[i*9 + j]:
                    print(Fore.GREEN + sudoku_str[i*9 + j] + " ", end="")
                else:
                    print(Style.RESET_ALL + sudoku_str[i*9 + j] + " ", end="")
            print(Style.RESET_ALL)


class Row() :
    def __init__(self, index: int, sudoku : str, original_sudoku: str): 
        self.values : List[str] = []
        row_index : int = index // 9
        start_index = row_index * 9
        end_index = start_index + 9
        self.values = list(sudoku[start_index : index]) + list(original_sudoku[index: end_index])

class Column() : 
    def __init__(self, index: int, sudoku : str, original_sudoku: str): 
        self.values : List[str] = []
        original_index = index
        while index > 9 : index-=9

        while index < original_index:
            self.values.append(sudoku[index])
            index += 9

        while index <= 72:
            self.values.append(original_sudoku[index])
            index += 9

# A section represent a square on 9 digits
class Section() : 
    def __init__(self, index: int, sudoku : str, original_sudoku: str): 
        self.values: List[str] = []
        row = (index // 9) // 3 * 3
        col = (index % 9) // 3 * 3
        start_index = row * 9 + col

        for i in range(0, 3):
            for y in range(0, 3):
                current_index = (start_index + y) + 9 * i
                if current_index < index:
                    self.values.append(sudoku[current_index])
                else:
                    self.values.append(original_sudoku[current_index])
    

