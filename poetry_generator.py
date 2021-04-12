"""
M6: Poetry Slam
CSCI 3725
Nicole Nigro
4/11/21

Generates and evaluates poems in the tanka form.

Dependencies: glob, os, random, re, string, syllapy, nltk, text2emotion, textstat, num2words

TODO - code: 
* ERRORS
    * how to handle problems with writing (i.e. word not in vowels, not in syllapy dictionary)
    * change the while loops??
    * word cases in evaluate_grammar: 'you’re', cop's, "won\'t", "couldn’t"
* 4Ps - PROCESS: What contextual information might inspire your computational poet? How might it move from inspiration to planning to creation?
    * have the first 2 line address the experience of the poet (what they saw, heard, felt, tasted, smelled etc.)
    * have the third line (turn/pivot) change the tone of the poem, relating to 2 lines above and below
    * have final 2 lines express a profound transcendental meaning that prompts reflection
        * make a connection that is just enough distinct that the reader is familiar with
        * try as a human first
        * Beale
    * Conceptual knowledge base
        * must convey a conceptual message, meaningful under some interpretation (meaningfulness)
* EVALUATION
    * make meaning out of grammar score
* display poem on the screen
    * implement Deepmoji: https://medium.com/@b.terryjack/nlp-pre-trained-sentiment-analysis-1eb52a9d742c
* incorporate more creativity theory from class into algorithms and documentation

TODO - not code:
* README
    * Title: Tanka Artful Generator for Knowledgable Artifacts (TAGKA);  System for Novel Tanka Generating Tanka Artifacts (TANGTA)
    * Description
    * Challenges
    * Scholarly paper and their inspo 
* VIDEO
    * video file of your system generating, evaluating, and performing a new poetry piece live.
    * Bonus points will be awarded if you have an audience reacting to what your system generates live.
        * If you do this, it should be clear what the system says, and what the follow-up reaction by the audience is.

TANKA INFO
Third line is a turn/pivotal image, which marks the transition from the examination of an image to the examination of the personal response.
In its purest form, tanka poems are most commonly written as expressions of gratitude, love, or self-reflection. Suitors would send
a tanka to a woman the day after a date, and she would reply in kind. These were short messages (like secret letters) expressing love,
desire, meaning, or gratitude. These poems often culminated in a transcendental message. Because tanka poems are meant to be given to
someone, they are written from the viewpoint of the poet. That does not mean they must be written in the first person, but the poet is
ever-present, always writing to express personal feelings about the subject. Like any constrained poem, lines should not begin with
articles (e.g., “a” or “the”) because articles reduce poetic compression and weaken the poetic impact of the form. In terms of content,
the kami-no-ku and shimo-no-ku tend to make a pair. Tanka is more likely to have transitions in narrative or mood. Traditionally, tanka has
addressed a limited number of themes, from seasons to love to travel to death, but contemporary tanka has tackled a much wider range of topics
within the age-old form.
"""

import nltk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import glob, os, random, re, string, syllapy
import text2emotion as te
import textstat
import num2words

class Tanka():
    def __init__(self):
        """
        Initializes a Tanka object with 5 lines (since it's a 5 line poem with a 5-7-5-7-7 syllable pattern),
        a last_words tuple, a bigrams dictionary, an all_words list, an emotions dictionary, a grammar_score,
        an understandability score, and an understandability category.
        Args: 
            None
        Return:
            None
        """
        self.line_1 = ""
        self.line_2 = ""
        self.line_3 = ""
        self.line_4 = ""
        self.line_5 = ""
        self.last_words = ()
        self.bigrams = dict()
        self.all_words = []
        self.emotions = dict()
        self.grammar_score = 0
        self.understandability_score = 0
        self.understandability_category = ""
        
    def read_files(self, input_dir):
        """
        Read in the files from the inspiring set.
        Arg:
            input_dir (str): name of directory the inspiring set of poems are in
        Return:
            None
        """
        for filename in glob.glob(input_dir):
            with open(os.path.join(filename), encoding='utf-8') as f:
                poem_words = []
                for word in f.read().split():
                    prep_word = word.lower().replace("&", "and").replace("--", "")
                    
                    #removes punctuation (except ' and -)
                    exclude = string.punctuation.replace("'", "").replace("-", "")
                    table = str.maketrans('', '', exclude)
                    cleaned_word = prep_word.translate(table)

                    #replaces numbers with their words
                    num_free_word = re.sub(r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), cleaned_word) 
                    
                    if num_free_word not in self.all_words:
                        self.all_words.append(num_free_word)

                    poem_words.append(num_free_word)

                self.create_bigrams(poem_words)

    def create_bigrams(self, words):
        """
        Creates 2-word ngrams.
        Arg:
            words (list): list of words in a poem
        Return:
            bigrams (dict): 2-word ngrams and the words that follow after and their frequencies
        """
        for i in range(len(words)-2):
            ngram = (words[i], words[i+1])
            next_word = words[i+2]
            if ngram in self.bigrams and next_word in self.bigrams[ngram]:
                self.bigrams[ngram][next_word] += 1
            elif ngram in self.bigrams:
                self.bigrams[ngram][next_word] = 1
            else:
                self.bigrams[ngram] = dict()
                self.bigrams[ngram][next_word] = 1
        return self.bigrams
            
    def syllables(self, word):
        """
        Counts the number of syllables in a word using the syllapy package.
        Arg:
            word (str): the word
        Return:
            word_syllables (int): the number of syllables in the word
        """
        word_syllables = syllapy.count(word)
        return word_syllables
    
    def get_next_word(self, word_pair):
        """
        Gets the next word based on the frequencies of the words following the current pair of words.
        Arg:
            word_pair (tuple): the current pair of words
        Return:
            next_word (str): the word chosen to follow next in the poem
        """
        if word_pair in self.bigrams:
            word_options = list(self.bigrams[word_pair].keys())
            word_frequencies = [self.bigrams[word_pair][i] for i in word_options]
            next_word = random.choices(population=word_options, weights=word_frequencies, k=1)[0]
        else:
            word_index = random.randint(0, len(self.all_words)-1)
            next_word = self.all_words[word_index]
        return next_word
    
    def write_kaminoku(self, current_pair):
        """
        Writes the first 3 parts of a tanka in 5-7-5 syllable pattern.
        Args:
            current_pair (tuple): the current pair of words used to start writing the kami-no-ku
        Return:
            None
        """
        self.line_1 += current_pair[0] + " " + current_pair[1] + " "
        syllable_count = self.syllables(str(current_pair))

        while self.syllables(self.line_1) != 5:
            if self.syllables(self.line_1) < 5:
                next_word = self.get_next_word(current_pair)
                self.line_1 += next_word + " "
                current_pair = (current_pair[1], next_word)
            else: 
                self.line_1 = ' '.join(self.line_1.split(' ')[:-1]) + " "
        
        print("line 1 done: " + self.line_1)
        
        while self.syllables(self.line_2) != 7:
            if self.syllables(self.line_2) < 7:
                next_word = self.get_next_word(current_pair)
                self.line_2 += next_word + " "
                current_pair = (current_pair[1], next_word)
            else: 
                self.line_2 = ' '.join(self.line_2.split(' ')[:-1]) + " " 
        
        print("line 2 done: " + self.line_2)

        while self.syllables(self.line_3) != 5:
            if self.syllables(self.line_3) < 5:
                next_word = self.get_next_word(current_pair)
                self.line_3 += next_word + " "
                current_pair = (current_pair[1], next_word)
            else: 
                self.line_3 = ' '.join(self.line_3.split(' ')[:-1]) + " "
        
        print("line 3 done: " + self.line_3)
        
        self.last_words = current_pair

    def write_shimonoku(self):
        """
        Writes the last 2 parts of a tanka in 7-7 syllable pattern.
        Args:
            None
        Return:
            None
        """
        current_pair = self.last_words

        while self.syllables(self.line_4) != 7:
            if self.syllables(self.line_4) < 7:
                next_word = self.get_next_word(current_pair)
                self.line_4 += next_word + " "
                current_pair = (current_pair[1], next_word)
            else: 
                self.line_4 = ' '.join(self.line_4.split(' ')[:-1]) + " "
        
        print("line 4 done: " + self.line_4)
        
        while self.syllables(self.line_5) != 7:
            if self.syllables(self.line_5) <= 7:
                next_word = self.get_next_word(current_pair)
                self.line_5 += next_word + " "
                current_pair = (current_pair[1], next_word)
            else: 
                self.line_5 = ' '.join(self.line_5.split(' ')[:-1]) + " "
        
        print("line 5 done")
                
    def write_tanka(self):
        """
        Writes a complete tanka, consisting of the kami-no-ku and shimo-no-ku.
        Args:
            None
        Return:
            poem (str): the 5-line tanka
        """
        ready = False

        while not ready:
            start_index = random.randint(0, len(self.bigrams)-1)
            start_pair = tuple(list(self.bigrams)[start_index])

            #first word of a tanka shouldn't be an article
            if pos_tag(word_tokenize(start_pair[0]))[0][1] != "DT" and self.syllables(str(start_pair)) <= 5:
                self.write_kaminoku(start_pair)
                self.write_shimonoku()
                ready = True

        poem = self.line_1 + self.line_2 + self.line_3 + self.line_4 + self.line_5

        return poem

    def export_poem(self):
        """
        Exports a poem to an output folder.
        Args:
            None
        Return:
            None
        """
        output_path = os.path.join("output", "tanka4.txt")
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(self.line_1 + "\n")
            f.write(self.line_2 + "\n")
            f.write(self.line_3 + "\n")
            f.write(self.line_4 + "\n")
            f.write(self.line_5)
        
    def export_pos_tags(self):
        """
        Export a file with all the words that are of a specified part of speech.
        Args:
            None
        Return:
            None
        """
        output_path = os.path.join("pos_tags", "NN.txt")
        with open(output_path, "w", encoding='utf-8') as f:
            for word in self.all_words:
                if len(pos_tag(word_tokenize(word))) == 0:
                    pass
                elif pos_tag(word_tokenize(word))[0][1] == "NN":
                    f.write("'" + str(pos_tag(word_tokenize(word))[0][0] + "'" + " | "))
                else:
                    pass

    def perform_poem(self, poem):
        """
        Performs a tanka out loud.
        Args:
            poem (str): the tanka to be performed
        Return:
            None
        """
        voices = ["Samantha", "Victoria", "Alex", "Fred"]
        speaker = random.choice(voices)
        os.system("say -v " + speaker + " " + poem)
    
    def evaluate_emotions(self, poem):
        """
        Evaluates the emotions of a poem (happy, angry, surprise, sad, fear) using the text2emotion package.
        Args:
            poem (str): the poem to evaluate
        Return
            emotions (dict): a dictionary with the 5 emotions and the poem's score for each
        """
        self.emotions = te.get_emotion(poem)
        return self.emotions
    
    def evaluate_grammar(self, poem):
        """
        Evaluates the grammar of a poem. Uses code from: https://www.fireblazeaischool.in/blogs/grammar-checking-using-nltk/
        Args:
            poem (str): the poem to evaluate
        Return:
            None
        """
        load_grammar = nltk.data.load('file:grammar.cfg')
        for word in poem.split():
            wrong_syntax = 1
            word_split = word.split()
            print("\n\n"+ word)
            rd_parser = nltk.RecursiveDescentParser(load_grammar)
            for tree_struc in rd_parser.parse(word_split):
                s = tree_struc
                wrong_syntax = 0 
                self.grammar_score += 1
                print("Correct Grammar !!!")
                print(str(s))
            if wrong_syntax == 1:
                print("Wrong Grammar!!!!")

    def evaluate_understandability(self, poem):
        """
        Evalautes the understandability using the textstat package. The flesch_reading_ease() method
        is used to measure the readability of a poem.
        Args:
            poem (str): the poem to evaluate
        Return
            understandability (float): the flesch reading ease score
        """
        self.understandability_score = textstat.flesch_reading_ease(poem)

        #categorize the score into the different Flesch Reading Ease Score categories
        if self.understandability_score >= 90:
            self.understandability_category = "Very Easy"
        elif 80 <= self.understandability_score <= 89:
            self.understandability_category = "Easy"
        elif 70 <= self.understandability_score <= 79:
            self.understandability_category = "Fairly Easy"
        elif 60 <= self.understandability_score <= 69:
            self.understandability_category = "Standard"
        elif 50 <= self.understandability_score <= 59:
            self.understandability_category = "Fairly Difficult"
        elif 30 <= self.understandability_score <= 49:
            self.understandability_category = "Difficult"
        else:
            self.understandability_category = "Very Confusing" # <= 29

        return self.understandability_score

    def export_metrics(self):
        """
        Exports the metrics from evaluation of the tanka: emotions, grammar, understandability.
        Args:
            None
        Return:
            None
        """
        output_path = os.path.join("metrics", "tanka4-metrics.txt")
        with open(output_path, "w", encoding='utf-8') as f:
            f.write("Emotions: " + str(self.emotions) + "\n")
            f.write("Grammar: " + str(self.grammar_score) + "\n")
            f.write("Understandability: " + str(self.understandability_score) + " (" + self.understandability_category + ") \n")
    
def main():
    t = Tanka()
    t.read_files("input/*")
    t.export_pos_tags()
    p = t.write_tanka()
    print(t.line_1)
    print(t.line_2)
    print(t.line_3)
    print(t.line_4)
    print(t.line_5)
    #t.perform_poem(p)
    print(t.syllables(t.line_1))
    print(t.syllables(t.line_2))
    print(t.syllables(t.line_3))
    print(t.syllables(t.line_4))
    print(t.syllables(t.line_5))
    t.export_poem()
    t.evaluate_emotions(p)
    t.evaluate_understandability(p)
    t.evaluate_grammar(p)
    t.export_metrics()

if __name__ == "__main__":
    main()