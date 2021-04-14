# Poetry Slam

## Description
In honor of Asian Heritage Month (celebrated during April here at Bowdoin), I wanted my poetry generator to create poems in a form native to Asia and have my poems inspired by an inspiring set of poems by Asian American authors. I chose the tanka, which is a poetry form that originated in Japan in the seventh century. My inspiring set includes poem from Asian American authors I know of (and have read in New Fictions of Asian America with Professor Kong!) like Cathy Park Hong and Ocean Vuong and also up-and-coming poets I found on [Poetry Foundation](https://www.poetryfoundation.org/collections/101589/asian-american-voices-in-poetry).

Tanka poems [do not traditionally have titles](http://www.graceguts.com/essays/why-say-more-the-problem-of-titling-tanka) which is why my tankas are titleless.

Kakai (translates to "poetry meeting") is a real world forum specific to tanka. In kakai, attendees submit poems anonymously, then read and discuss each other's work. To reflect kakai performances, I have the 4 different voices available on my OS and randomly choose one to perform each tanka.

This system is a way for me to pay homage to recent Anti-Asian American violence and the Asian American component of my identity.

## How to Set Up and Run the Code
1. Open the terminal.
2. Change your directory to the folder you want to store this code in.  
```
$ cd Documents/GitHub
```
3. Clone this repository onto your computer with the following line:  
```
$ git clone https://github.com/nicolenigro/poetry-slam.git
```
4. Change your directory to the folder for this project.  
```
$ cd poetry-slam
```
5. Install all the necessary packages with the following commands:
```
$ pip3 install nltk
$ pip3 install syllapy
$ pip3 install text2emotion
$ pip3 install textstat
$ pip3 install num2words
```
6. Type and enter the following line into the terminal to run the program.  
```
$ python3 poetry_generator.py
```

## Challenges
I had a lot of challenges installing packages that I wanted to use and dealing with errors in the terminal. I discovered that even though I have the latest version of Python installed on my computer, Python 2.7 was linked and the default, which creates lots of errors. I troubleshooted errors by googling, looking online for different commands to fix all the problems I was having, and was ultimately able to implement all but 1 package, [torchMoji](https://github.com/huggingface/torchMoji). I ended up reaching out to the developer via email and it turns out it is not compatible with the version of Python I am running (3.9.4). Working through errors in the terminal was really tough and required patience, but I persevered and feel like I am now equipped to deal with all sorts of problems related to installing packages, homebrew, and the terminal.

I also really struggled with finding a way to incorporate grammar rules into my system. I have learned about CFG and parse trees in PPL so I wanted to push myself to draw connections between my CS classes and use some of those linguistic concepts. From my research, I decided the best way to implement this would be creating my own CFG, but I struggled to create the CFG file.

## Scholarly Papers That Inspired My Approach
* [About Tanka](https://www.tandfonline.com/doi/full/10.1080/19342039.2016.1120610)
	* From this article, I learned more about the form of a tanka. It follows a 5-7-5-7-7 syllable pattern, with the first three parts (5-7-5) called the kami-no-ku and the final two parts (7-7) called the shimo-no-ku, which tend to make a pair. To honor the process of tanka poets, I wrote write_kaminoku() and write_shimonoku() functions.
* [Automatic generation of poetry: an overview](https://www.researchgate.net/profile/Hugo-Goncalo-Oliveira/publication/228610670_Automatic_generation_of_poetry_an_overview/links/00b7d517eea41271af000000/Automatic-generation-of-poetry-an-overview.pdf)
	* This article mentioned Manurung's taxonomy for poetry generation systems, and I was inspired to create a form-aware poetry generation system. In form-aware systems, the choice of words follows a pre-defined text form by following metrical rules (properties of grammaticality and poeticness). I implemented the syllapy package to ensure that each line is following the metrical rule of the tanka syllable pattern. I was particularly inspired by Levy's POEVOLVE--a form-aware system--in which "the real process of human poetry writing is taken as a reference from which to draw the intuitions that drive the system" (3). From Levy's model, I decided to implement evaluator modules for analyzing generated tankas as well as conceptual and syntactical knowledge bases. The syntactical knowledge base is the CFG file that I wrote consisting of grammar rules and which POS each word from poems in the inspiring set belong to. The conceptual knowledge base is _______.
* [A Survey on Intelligent Poetry Generation: Languages, Features, Techniques, Reutilisation and Evaluation](https://www.aclweb.org/anthology/W17-3502/)
	* Similar to the above article, this one also referenced Manurung. According to Manurung, besides poeticness, a poetic text "must obey linguistic conventions, prescribed by a given grammar and lexicon (grammaticality); and it must convey a conceptual message, meaningful under some interpretation (meaningfulness)." I incorporated grammaticality through my evaluate_grammar() function which evaluates a poem according to the CFG that I wrote. I incorporated meaningfulness by _________. The evaluation section also gave me some ideas for how I would evaluate the tankas generated by my poem. I was intrigued by evaluating a poem by emotions, understandability, and grammar. However this paper emphasized that it is hard to evaluate systems automatically, which is why I additionally had a live human reaction to/evaluation of my poetry.
* [Fixed Verse Generation using Neural Word Embeddings](https://core.ac.uk/download/pdf/79584968.pdf)
	* I was inspired by the classification process mentioned in this paper. I decided to tokenize sentences from my inspiring set into bigrams (2-word ngrams) with a create_ngrams() function. I also was inspired to tag each word with POS-tags, which I did to categorize words in the knowledge base into different POS categories.

## Sources
* https://docs.huihoo.com/nltk/0.9.5/en/ch07.html
* https://poets.org/glossary/tanka
* https://pypi.org/project/syllapy/
* https://pypi.org/project/textstat/
* https://tankajournal.com/what-is-tanka/
* https://towardsdatascience.com/how-to-efficiently-remove-punctuations-from-a-string-899ad4a059fb
* https://towardsdatascience.com/text2emotion-python-package-to-detect-emotions-from-textual-data-b2e7b7ce1153
* https://web.stanford.edu/~jurafsky/slp3/12.pdf
* https://www.fireblazeaischool.in/blogs/grammar-checking-using-nltk/
* https://www.kite.com/python/docs/nltk.pos_tag
* https://www.nltk.org/book/ch08.html
* https://www.wikihow.com/Write-a-Tanka-Poem