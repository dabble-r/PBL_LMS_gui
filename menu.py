

class Menu:
    def __init__(self, title, options=[]):
        self.title = title
        self.options = options
    
    def __str__(self):
      ret = ''
      for indx, el in enumerate(self.options, start=1):
          ret += f'{indx}: {el} \n'
      return ret
          
    def add_option(self, option_str, func):
        tmp = {}
        try:
          tmp['name'] = option_str
          tmp['action'] = func
          self.options.append(tmp)
        except (ValueError, TypeError):
            print('Enter a valid text option')
            option_str = input('Enter a menu option to add: \n')
        #print(self.options)

    def get_size(self):
        return len(self.options)
    
    def display(self):
        print(self.title)
        print("=" * len(self.title))
        for i, option in enumerate(self.options, start=1):
            print(f"{i}. {option['name']}")

    def select_option(self,choice):
        while True:
            try:
                #choice = int(input("Select a menu option by number: "))
                if 1 <= choice <= len(self.options):
                    return self.options[choice - 1]['action']
                else:
                    print("Invalid choice. Please choose a valid option.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

