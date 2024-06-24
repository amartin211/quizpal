verbal_questions_direction = """\
For verbal section, there are 3 types of questions: \
1 - Reading Comprehension: \
    Direction: The questions in this group are based on the content of a passage\
    After reading the passage, choose the best answer to each question. Answer all questions following the passage on the basis of what is stated or implied in the passage.\ 
    Text is indicated by '###' at the begining and at the end. Questions are indicated by '***' and Option choice are surrounded by '@@@'\
        Question sample:\
            ###Schools expect textbooks to be a valuable source of information for students. My research suggests, however, that textbooks that address the place\ 
            of Native Americans within the history of the United States distort history to suit a particular cultural value system. In some textbooks, for\ 
            example, settlers are pictured as more humane, complex, skillful, and wise than Native Americans. In essence, textbooks stereotype and depreciate\ 
            the numerous Native American cultures while reinforcing the attitude that the European conquest of the New World denotes the superiority of\ 
            European cultures. Although textbooks evaluate Native American architecture, political systems, and homemaking, I contend that they do it from an\ 
            ethnocentric, European perspective without recognizing that other perspectives are possible.\
            One argument against my contention asserts that, by nature, textbooks are culturally biased and that I am simply\ 
            underestimating children's ability to see through these biases. Some researchers even claim that by the time students are\ 
            in high school, they know they cannot take textbooks literally. Yet substantial evidence exists to the contrary.\ 
            Two researchers, for example, have conducted studies that suggest that children's attitudes about particular cultures\ 
            are strongly influenced by the textbooks used in schools. Given this, an ongoing, careful review of how school textbooks depict Native Americans is certainly warranted.###\
            ***Which of the following would most logically be the topic of the paragraph immediately following the passage?***\
            (A) @@@Specific ways to evaluate the biases of United States history textbooks@@@\
            (B) @@@The centrality of the teacher's role in United States history courses@@@\
            (C) @@@Nontraditional methods of teaching United States history@@@\
            (D) @@@The contributions of European immigrants to the development of the United States@@@\
            (E) @@@Ways in which parents influence children's political attitudes@@@ \
            Answer: (A)
2 - Critical Reasoning :
    Direction : For this question, select the best of the answer choices given. Text is indicated by '###' at the begining and at the end. Questions are indicated by '***' and Option choice are surrounded by '@@@'\
        Question sample:\
            ###The cost of producing radios in Country Q is ten percent less than the cost of producing radios in Country Y.\ 
            Even after transportation fees and tariff charges are added, it is still cheaper for a company \
            to import radios from Country Q to Country Y than to produce radios in Country Y.###\
            *** The statements above, if true, best support which of the following assertions?***\
            (A) @@@Labor costs in Country Q are ten percent below those in Country Y.@@@\
            (B) @@@Importing radios from Country Q to Country Y will eliminate ten percent of the manufacturing jobs in Country Y.@@@\
            (C) @@@The tariff on a radio imported from Country Q to Country Y is less than ten percent of the cost of manufacturing the radio in Country Y.@@@\
            (D) @@@The fee for transporting a radio from Country Q to Country Y is more than ten percent of the cost of manufacturing the radio in Country Q.@@@\
            (E) @@@It takes ten percent less time to manufacture a radio in Country Q than it does in Country Y.@@@\
            Answer: (C)\
3 - Sentence Correction :
    Directions : \
        This question presents a sentence, part of which or all of which will also be the first option choice presented. Beneath the sentence you will find five\ 
        ways of phrasing the underlined part. The first of these repeats the original; the other four are different. If you\ 
        think the original is best, choose the first answer; otherwise choose one of the others.\
        This question tests correctness and effectiveness of expression. In choosing your answer, follow the requirements of\ 
        standard written English; that is, pay attention to grammar, choice of words, and sentence construction. Choose the\ 
        answer that produces the most effective sentence; this answer should be clear and exact, without awkwardness, ambiguit, redundancy, or grammatical error.\
        Sentences is indicated by '***' at the begining and at the end. Option choice are surrounded by '@@@'\
        Question sample: \
            *** While larger banks can afford to maintain their own data-processing operations, many smaller regional and community\ 
            banks are finding that the cost associated with upgrading data-processing equipment and with the development and\ 
            maintenance of new products and technical staff are prohibitive.***\
            (A) @@@cost associated with@@@\
            (B) @@@costs associated with@@@\
            (C) @@@costs arising from@@@\
            (D) @@@cost of@@@\
            (E) @@@costs of@@@\
            Answer: (B)\
"""

quantitative_questions_direction = """\
For quantitative section, there are 2 types of questions: \
1 - Problem Solving: \
    You use logic and analytical reasoning to solve quantitative problems. You solve the problem and indicate the best of five answer choices.\
    Directions:\
        Solve the problem and indicate the best of the answer choices given. Questions start and end with '***' and each option choice is surrounded by '@@@'\
        Question sample:\
            ***If $u>t, r>q, s>t$, and $t>r$, which of the following must be true?\
            1. $u>s$\
            2. $s>q$\
            3. $u>r$***\
            (A) @@@I only@@@\
            (B) @@@II only@@@\
            (C) @@@III only@@@\
            (D) @@@I and II@@@\
            (E) @@@II and III@@@\
            Answer: (E)\
2 - Data Sufficiency Question: \
    Measures your ability to analyze a quantitative problem, recognize which data is relevant, and determine at what point there are enough data to solve the problem.\
    You will be given a problem that consists of a question and two statements. Using the data in the statements, plus your knowledge of math and everyday facts, \
    you decide whether you have enough data in the statement to answer the question asked.\
    Directions:\
        This data sufficiency problem consists of a question and two statements, labeled (1) and (2), in which certain data are given. \
        You have to decide whether the data given in the statements are sufficient for answering the question. Using the data given in the statements, \
        plus your knowledge of mathematics and everyday facts (such as the number of days in July or the meaning of the word counterclockwise), you must indicate whether:\
            1) Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient to answer the question asked.\
            2) Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient to answer the question asked.\
            3) BOTH statements (1) and (2) TOGETHER are sufficient to answer the question asked, but NEITHER statement ALONE is sufficient to answer the question asked.\
            4) EACH statement ALONE is sufficient to answer the question asked.\
            5) Statements (1) and (2) TOGETHER are NOT sufficient to answer the question asked, and additional data specific to the problem are needed.\
            Questions start and end with '***' and each option choice is surrounded by '@@@'\
        Question sample:\
            ***If a real estate agent received a commission of 6 percent of the selling price of a certain house, what was the selling price of the house?\ 
            (1) The selling price minus the real estate agent's commission was $84,600.\ 
            (2) The selling price was 250 percent of the original purchase price of $36,000.***\ 
            (A) @@@Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.@@@ \ 
            (B) @@@Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.@@@ \ 
            (C) @@@BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.@@@ \ 
            (D) @@@EACH statement ALONE is sufficient.@@@ \ 
            (E) @@@Statements (1) and (2) TOGETHER are NOT sufficient.@@@\ 
            Answer: (D)
            
"""


data_sufficiency_strategy = """\
These questions require knowledge of the following topics:\
- Arithmetic\
- Elementary algebra\
- Commonly known concepts of geometry\
Data sufficiency questions are designed to measure your ability to analyze a quantitative problem, recognize which given information is relevant,\ 
and determine at what point there is sufficient information to solve a problem. \
In these questions, you are to classify each problem according to the five fixed answer choices, rather than find a solution to the problem.\
Each data sufficiency question consists of a question, often accompanied by some initial information, and two statements, labeled (1) and (2), which contain additional information. \
You must decide whether the information in each statement is sufficient to answer the question or-if neither statement provides enough information - whether the information in the two \
statements together is sufficient. It is also possible that the statements in combination do not give enough information to answer the question.\
Begin by reading the initial information and the question carefully. Next, consider the first statement. \
Does the information provided by the first statement enable you to answer the question? Go on to the second statement. Try to ignore the information given in the first statement when you consider \
whether the second statement provides information that, by itself, allows you to answer the question. Now you should be able to say, for each statement, whether it is sufficient to determine the answer.\
Next, consider the two statements in tandem. Do they, together, enable you to answer the question?\
Look again at your answer choices. Select the one that most accurately reflects whether the statements provide the information required to answer the question.\
Test-Taking Strategies\
You only need to determine whether sufficient information is given to solve it.\
1. Consider each statement separately.\
First, decide whecher each statement alone gives sufficient information to solve the problem. Be sure to disregard the information given in statement (1) when you evaluate the information given in statement (2). \
If either, or both, of the statements give(s) sufficient information to solve the problem, select the answer corresponding to the description of which statement(s) give(s) sufficient information to solve the problem.\
2. Judge the statements in tandem if neither statement is sufficient by îtself. \
It is posible that the two statements together do not provide sufficient information. \
Once you decide, select the answer corresponding to the description of whether the statements together give sufficient information to solve the problem.\
3. Answer the question asked.\
For example, if the question asks, "What is the value of $y$ ?" for an answer statement to be suffient you must be able to find one and only one value for $y$. \
Being able to determine minimum or maximum values for an answer $\left(e_{g . y} y=x+2\right)$ is not sufficient, because such answers constitute a range of values rather than the specific value of $y$.\

"""

output_structure = """ 
Question 544 : 
  question : |
    ###Neuroscientist: Memory evolved to help animals react appropriately to situations they encounter by drawing on the past experience of similar situations. But this does not require that animals perfectly recall every detail of all their experiences. Instead, to function well, memory should generalize from past experiences that are similar to the current one.###
    ***The neuroscientist's statements, if true, most strongly support which of the following conclusions?***
    (A) @@@At least some animals perfectly recall every detail of at least some past experiences.@@@
    (B) @@@Perfectly recalling every detail of all their past experiences could help at least some animals react more appropriately than they otherwise would to new situations they encounter.@@@
    (C) @@@Generalizing from past experiences requires clear memories of most if not all the details of those experiences.@@@
    (D) @@@Recalling every detail of all past experiences would be incompatible with any ability to generalize from those experiences.@@@
    (E) @@@Animals can often react more appropriately than they otherwise would to situations they encounter if they draw on generalizations from past experiences of similar situations.@@@
  Answer: X
            
            """