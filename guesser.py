import yaml
from rich.console import Console
from collections import defaultdict, Counter
from numpy import log2







class Guesser:
    '''
        INSTRUCTIONS: This function should return your next guess. 
        Currently it picks a random word from wordlist and returns that.
        You will need to parse the output from Wordle:
        - If your guess contains that character in a different position, Wordle will return a '-' in that position.
        - If your guess does not contain that character at all, Wordle will return a '+' in that position.
        - If you guesses the character placement correctly, Wordle will return the character. 

        You CANNOT just get the word from the Wordle class, obviously :)
    '''
    def __init__(self, manual):
        self.word_list = yaml.load(open('wordlist.yaml'), Loader=yaml.FullLoader)
        
        self._manual = manual
        self.console = Console()
        
        
        self._tried = []
        self.max_e = {}
        self.initial= 'salet'
        self.pattern_dict = {}
        self.correct_letters = {0:'',1:'',2:'',3:'',4:''}
        self.possible_words = self.word_list
        self.old_res = ''

        
        
    def restart_game(self):
        self.word_list = yaml.load(open('wordlist.yaml'), Loader=yaml.FullLoader)
        self._tried = []
        self.correct_letters = {0:'',1:'',2:'',3:'',4:''}
        self.possible_words = self.word_list

        
        
    def get_matches(self, word, guess):
        counts = Counter(word)
        results = []
        for i, letter in enumerate(guess):
            if guess[i] == word[i]:
                results+=guess[i]
                counts[guess[i]]-=1
            else:
                results+='+'
        for i, letter in enumerate(guess):
            if guess[i] != word[i] and guess[i] in word:
                if counts[guess[i]]>0:
                    counts[guess[i]]-=1
                    results[i]='-'
    
        return ''.join(results)
    
    
    def max_ent(self, words):
        ent_per_word = defaultdict(float)
        num_words = len(self.possible_words)
        for guess in words:
            count_per_pattern = Counter([self.get_matches(word,guess) for word in self.possible_words]) 
            ent_per_word[guess] = sum([count_per_pattern[key]/num_words * log2(num_words/count_per_pattern[key]) for key in count_per_pattern])
        return max(ent_per_word,key = ent_per_word.get)
    
    
    

        

    
    def update_possible(self, guess, result):
        self.possible_words = [word  for word in self.possible_words if self.get_matches(word, guess) == result]
        
        for i in range(5):
            if result[i].isalpha():
                self.possible_words = [word for word in self.possible_words if word[i] in word]
                self.correct_letters[i] = result[i]
                
            elif result[i] == '+':
                for word in self.possible_words:

                    if guess.count(guess[i]) == 1 and guess[i] in word:
                        self.possible_words.remove(word)
                        
                    elif guess.count(guess[i]) > 1 and guess[i] == word[i]:
                        self.possible_words.remove(word)  
                        
            elif result[i] == '-':
                for word in self.possible_words:
                    if guess[i] == word[i]:
                        self.possible_words.remove(word)
        
        return self.possible_words
                        



    def get_guess(self, result):
        '''
        This function must return your guess as a string. 
        '''
        self.result = result
        
        if self._manual=='manual':
            return self.console.input('Your guess:\n')
        
        
        
        else:
            '''
            CHANGE CODE HERE
            '''
            if len(self._tried) == 0:

                    
                self.guess = self.initial
                self._tried.append(self.guess)
                self.console.print(self.guess)
                return self.guess
            
            
            if len(self._tried) == 1:
                
                self.update_possible(self.initial, result)
                
                if len(self.word_list) == 1:
                    return self.word_list[0]
                
                if result in self.max_e:
                    self.possible_words = self.pattern_dict[result]
                    guess = self.max_e[result]
                    
                else:
                    self.pattern_dict[result] = self.update_possible(self.initial, result)
                    guess = self.max_ent(self.word_list)
                    
                
                
                self.max_e[result] = guess
                
                
                self._tried.append(guess)
                self.console.print(guess)
                return guess 
            
            
            elif len(self._tried) <= 4:
                last_guess = self._tried[-1]
                self.update_possible(last_guess, result)
             

    
                if result.count('+') in [1,2] and result.count('-') == 0 and len(self.possible_words) > 2:
                    indices = [i for i, char in enumerate(result) if char == '+']

                    guess = ''
                    
                    for word in self.possible_words:
                        for index in indices:
                            if len(guess) < 5 and word[index] not in guess:
                                guess += word[index]
                                
                    self.guess = guess.ljust(5, 'b')
                    self._tried.append(self.guess)
                    self.console.print(self.guess)

                    return self.guess
                
                elif result.count('-') == 0 and len(self.possible_words) > 2 and len(self.possible_words) < 10 and sum(1 for value in self.correct_letters.items() if value == '') <= 2:        
                    indices = [i for i, value in self.correct_letters.items() if value == '']

                    guess = ''
                    
                    for word in self.possible_words:
                        for index in indices:
                            if len(guess) < 5 and word[index] not in guess:
                                guess += word[index]
                                
                    self.guess = guess.ljust(5, 'b')
                    self._tried.append(self.guess)
                    self.console.print(self.guess)

                    return self.guess
                
                else:

                    guess = self.max_ent(self.possible_words)
                    self._tried.append(guess)
                    self.console.print(guess)
                
                    return guess

            else:
                last_guess = self._tried[-1]
                self.update_possible(last_guess, result)
                guess = self.max_ent(self.possible_words)
                self._tried.append(guess)
                self.console.print(guess)
            
                return guess
                
       