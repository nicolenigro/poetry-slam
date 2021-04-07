# Poetry Slam

## Description

## How to Set Up and Run the Code

## Challenges

## Scholarly Papers That Inspired My Approach
* [About Tanka](https://www.tandfonline.com/doi/full/10.1080/19342039.2016.1120610)
	* From this article, I learned more about the form of a tanka. It follows a 5-7-5-7-7 syllable pattern, with the first three parts (5-7-5) called the kami-no-ku and the final two parts (7-7) called the shimo-no-ku, which tend to make a pair. To honor the process of tanka poets, I wrote write_kaminoku() and write_shimonoku() functions.
* [Automatic generation of poetry: an overview](https://www.researchgate.net/profile/Hugo-Goncalo-Oliveira/publication/228610670_Automatic_generation_of_poetry_an_overview/links/00b7d517eea41271af000000/Automatic-generation-of-poetry-an-overview.pdf)
	* This article provides an overview of different systems for generating poetry. I was particularly inspired by Levy's POEVOLVE in which "the real process of human poetry writing is taken as a reference from which to draw the intuitions that drive the system" (3). From Levy's model I decided to implement evaluator modules for analyzing and selecting the highest ranked poems for each generation as wall as conceptual and syntactical knowledge bases. 
* [A Survey on Intelligent Poetry Generation: Languages, Features, Techniques, Reutilisation and Evaluation](https://www.aclweb.org/anthology/W17-3502/)
* [Fixed Verse Generation using Neural Word Embeddings](https://core.ac.uk/download/pdf/79584968.pdf)
	* I was inspired by the classification process mentioned in this paper. I decided to tokenize sentences from my inspiring set into bigrams (2-word ngrams) with a create_ngrams() function. I also tag each word with POS-tags in my tag_words() function.
* [Towards A Computational Model of Poetry Generation](https://era.ed.ac.uk/bitstream/handle/1842/3460/0015.pdf?sequence=1&isAllowed=y)

## Sources
* https://poets.org/glossary/tanka
* https://pypi.org/project/syllapy/
* https://tankajournal.com/what-is-tanka/
* https://towardsdatascience.com/how-to-efficiently-remove-punctuations-from-a-string-899ad4a059fb
* https://towardsdatascience.com/text2emotion-python-package-to-detect-emotions-from-textual-data-b2e7b7ce1153
* https://www.kite.com/python/docs/nltk.pos_tag