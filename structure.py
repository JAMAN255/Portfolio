from calculations import Calculations, IndexCalculations
from data_actions import Data
class Structure:
    def __init__(self):
        self.menu = {
            '1': 'Import data',
            '2': 'export data',
            '3': 'Calculate Mean',
            '4': 'Calculate Median',
            '5': 'Calculate Mode',
            '6': 'Calculate Ageing Index',
            '7': 'Calculate Sauvy Index',
            '8': 'Calculate EC Weight Index',
            '9': 'Calculate Dependency Index',
            '10': 'Calculate Shadow Index',
            '11': 'Exit'}
    def display_menu(self):
        print("Menu:")
        for key, value in self.menu.items():
            print(f"{key}. {value}")
        choice = input("Enter your choice: ")
        return choice
    
    
    def menu_choice(self, choice):
        choice = self.display_menu()
        match choice:
            case '1':
                Data.import_data()
            case '2':
                Data.export_data()
            case '3':
                Calculations.mean()
            case '4':
                Calculations.median()
            case '5':
                Calculations.mode()
                pass
            case '6':
                IndexCalculations.ageing_idx()
            case '7':
                IndexCalculations.sauvy_idx()
            case '8':
                IndexCalculations.ec_weight_idx()
                pass
            case '9':
                IndexCalculations.dependency_idx()
            case '10':
                IndexCalculations.shadow_idx()
            case '11':
                print("Exiting the program.")
            case _:
                print("Invalid choice. Please try again.")

