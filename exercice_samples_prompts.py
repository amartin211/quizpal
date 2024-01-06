
############################################################################## EXERCICE EXAMPLE ###################################################################################
############################################################################## EXERCICE EXAMPLE ###################################################################################



data_sufficiency_examples = """\

ANSWER KEY
Here are the answers for the problems in the exam

- Problem 1: 
***A certain bookcase has 2 shelves of books. On the upper shelf, the book with the greatest number of pages has 400 pages. On the lower shelf, the book with the least number of pages has 475 pages. What is the median number of pages for all of the books on the 2 shelves?
      (1) There are 25 books on the upper shelf.
      (2) There are 24 books on the lower shelf.***
      (A) @@@Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.@@@
      (B) @@@Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.@@@
      (C) @@@BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.@@@
      (D) @@@EACH statement ALONE is sufficient.@@@
      (E) @@@Statements (1) and (2) TOGETHER are NOT sufficient.@@@

- Explanation for Problem 1 
(1) The information given says nothing about the number of books on the lower shelf. If there are fewer than 25 books on the lower shelf, then the median number of pages will be the number of pages in one of the books on the upper shelf or the average number of pages in two books on the upper shelf.
Hence, the median will be at most 400 . If there are more than 25 books on the lower shelf, then the median number of pages will be the number of pages in one of the books on the lower shelf or the average number of pages in two books on the lower shelf. Hence, the median will be at least 475 ; NOT sufficient.
(2) An analysis very similar to that used in (1) shows the information given is not sufficient to determine the median; NOT sufficient.
Given both (1) and (2), it follows that there is a total of 49 books. Therefore, the median will be the 25 th book when the books are ordered by number of pages. Since the 25 th book in this ordering is the book on the upper shelf with the greatest number of pages, the median is 400 . Therefore, (1) and (2) together are sufficient.
The correct answer is therefore (C) both statements together are sufficient.

- Problem 2: 
***At what speed was a train traveling on a trip when it had completed half of the total distance of the trip?
    (1) The trip was 460 miles long and took 4 hours to complete.
    (2) The train traveled at an average rate of 115 miles per hour on the trip.***
      (A) @@@Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.@@@
      (B) @@@Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.@@@
      (C) @@@BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.@@@
      (D) @@@EACH statement ALONE is sufficient.@@@
      (E) @@@Statements (1) and (2) TOGETHER are NOT sufficient.@@@

- Explanation for Problem 2:  
Determine the speed of the train when it had completed half the total distance of the trip.
(1) Given that the train traveled 460 miles in 4 hours, the train could have traveled at the constant rate of 115 miles per hour for 4 hours, and thus it could have been traveling 115 miles per hour when it had completed half the total distance of the trip. However, the train could have traveled 150 miles per hour for the first 2 hours (a distance of 300 miles) and 80 miles per hour for the last 2 hours (a distance of 160 miles), and thus it could have been traveling 150 miles per hour when it had completed half the total distance of the trip; NOT sufficient.
(2) Given that the train traveled at an average rate of 115 miles per hour, each of the possibilities given in the explanation for (1) could occur, since 460 miles in 4 hours gives an average speed of $\frac{460}{4}=115$ miles per hour; NOT sufficient.
Assuming (1) and (2), each of the possibilities given in the explanation for (1) could occur. Therefore, (1) and (2) together are not sufficient.
The correct answer is therefore (E); both statements together are still not sufficient.


- Problem 3:
***Material A costs $\$ 3$ per kilogram, and Material B costs $\$ 5$ per kilogram. If 10 kilograms of Material $K$ consists of x kilograms of Material $A$ and $y$ kilograms of Material $B$, is $x>y$ ?
(1) $y>4$
(2) The cost of the 10 kilograms of Material $K$ is less than $\$ 40$.***
    (A) @@@Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.@@@
    (B) @@@Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.@@@
    (C) @@@BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.@@@
    (D) @@@EACH statement ALONE is sufficient.@@@
    (E) @@@Statements (1) and (2) TOGETHER are NOT sufficient.@@@
- Explanation for Problem 3:
Since $x+y=10$, the relation $x>y$ is equivalent to $x>10-x$, or $x>5$.
(1) The given information is consistent with $x=5$ and $y=4.5$, and the given information is also consistent with $x=y=5$. Therefore, it is possible for $x>y$ to be true and it is possible for $x>y$ to be false; NOT sufficient.
(2) Given that $3 x+5 y<40$, or $3 x+5(10-x)<40$, then $3 x-5 x<40-50$. It follows that $-2 x<-10$, or $x>5$; SUFFICIENT.
The correct answer is B; statement 2 alone is sufficient.

- Problem 4:
***For any positive integer $x$, the 2 -height of $x$ is defined to be the greatest nonnegative integer $n$ such that $2^{n}$ is a factor of $x$. If $k$ and $m$ are positive integers, is the 2height of $k$ greater than the 2 -height of $m$ ?
(1) $k>m$
(2) $\frac{k}{m}$ is an even integer.***

- Explanation for Problem 4:
(1) Given that $k>m$, the 2-height of $k$ can be greater than $m$ (choose $k=4$, which has a 2-height of 2, and choose $m=2$, which has a 2 -height of 1 ) and the 2-height of $k$ can fail to be greater than $m$ (choose $k=3$, which has a 2 -height of 0 , and choose $m=2$, which has a 2-height of 1 ); NOT sufficient.
(2) Given that $\frac{k}{m}$ is an even integer, it follows that $\frac{k}{m}=2 n$ for some integer $n$, or $k=2 m n$.
This implies that the 2-height if $k$ is at least one more than the 2-height of $m$; SUFFICIENT.
The correct answer is B; statement 2 alone is sufficient.

- Problem 5:
[4,6,8,10,12,14,16,18,20,22]
List $M$ (not shown) consists of 8 different integers, each of which is in the list shown above. What is the standard deviation of the numbers in list $M$ ?
(1) The average (arithmetic mean) of the numbers in list $M$ is equal to the average of the numbers in the list shown.
(2) List $M$ does NOT contain 22.

- Explanation for Problem 5:
If each of the 8 different numbers in list $M$ is in the set $\{4,6,8,10,12,14,16,18,20,22\}$, then list $M$ can be obtained by removing 2 numbers from the given list. If $s_{M}$ denotes the standard deviation of the numbers in list $M$, determine the value of $s_{M}$.
The average of the numbers in the given list is $\frac{4+6+8+\cdots+22}{10}=13$, which can also be determined by observing that the numbers in the list are symmetric about 13 . If $s$ denotes the standard deviation of the given list, then
\[
\begin{array}{l}
s^{2}=\frac{(4-13)^{2}+(6-13)^{2}+(8-13)^{2}+\cdots+(20-13)^{2}+(22-13)^{2}}{10} \\
\text { and } \\
10 s^{2}=(4-13)^{2}+(6-13)^{2}+(8-13)^{2}+\cdots+(20-13)^{2}+(22-13)^{2} . \\
\end{array}
\]
(1) It is given that the average of the numbers in list $M$ is the same as the average of the numbers in the given list, so the average of the numbers in list $M$ is 13 and, therefore, the sum of the numbers in list $M$ is $8(13)=104$. Since the sum of the numbers in the given list is $10(13)=130$, the sum of the 2 numbers removed from the given list to create list $M$ must be $130-104=26$. Thus, the 2 numbers could be the 2 middle values, 12 and 14 , or the 2 numbers at the extremes, 4 and 22 . If the numbers removed are 12 and 14 , then using the reasoning shown above, $8 s_{M}^{2}=10 s^{2}-(12-13)^{2}-$ $(14-13)^{2}=10 s^{2}-2$. On the other hand, if 4 and 22 are the numbers removed, then $8 s_{M}^{2}=10 s^{2}-(4-13)^{2}-(22-13)^{2}=$ $10 s^{2}-162$. Since $10 s^{2}-2 \neq 10 s^{2}-162,8 s_{M}{ }^{2}$ can vary, and hence $s_{M}$ can vary; NOT sufficient.
(2) It is given that list $M$ does not contain 22. Since no information is given about the other number that is to be removed from the given list to create list $M$, it is not possible to determine the average of the numbers in list $M$. For example, if the other number removed is 20 , then the average is
\[
\frac{4+6+8+\cdots+18}{8}=11 \text { and }
\]
\[
8 s_{M}{ }^{2}=(4-11)^{2}+(6-11)^{2}+(8-11)^{2}+\cdots+(18-11)^{2}=176
\]
But if the other number removed is 12 , then the average is $\frac{4+6+8+10+14+16+18+20}{8}=12$ and
(2)
\[
\begin{array}{l}
\text { But if the other number removed is } 12 \text {, then the } \\
\text { average is } \frac{4+6+8+10+14+16+18+20}{8}=12 \\
\text { and } \\
8 s_{M}^{2}=(4-12)^{2}+\cdots+(10-12)^{2}+(14-12)^{2}+\cdots+(20-12)^{2}=24 .
\end{array}
\]
Because $8 s_{M}^{2}$ varies, so does $s_{M}$; NOT sufficient.
Taking (1) and (2) together, the sum of the 2 numbers removed from the given list to create list $M$ must be 26 and one of those numbers is 22. Therefore, the other number is 4 , and so list $M$ consists of the numbers $6,8,10,12,14,16,18,20$. Since the numbers in list $M$ are known, $s_{M}$ can be determined.
The correct answer is C; both statements together are sufficient."""


problem_solving_examples = """\

ANSWER KEY
Here are the answers for the problems in the exam

- Problem 1: 

***If $\mathrm{m}^{-1}=\frac{1}{3}$, then $\mathrm{m}^{-2}$ is equal to***
(A) @@@-9@@@
(B) @@@-3@@@
(C) @@@$-\frac{1}{9}$@@@
(D) @@@$\frac{1}{9}$@@@
(E) @@@9@@@

- Explanation for Problem 1 
Using rules of exponents, $m^{-2}=m^{-1 \cdot 2}=\left(m^{-1}\right)^{2}$ and since $m^{-1}=-\frac{1}{3}, m^{-2}=\left(-\frac{1}{3}\right)^{2}=\frac{1}{9}$
The correct answer is therefore (D).


- Problem 2: 
***A photography dealer ordered 60 Model $X$ cameras to be sold for $\$ 250$ each, which represents a 20 percent markup over the dealer's initial cost for each camera. Of the cameras ordered, 6 were never sold and were returned to the manufacturer for a refund of 50 percent of the dealer's initial cost. What was the dealer's approximate profit or loss as a percent of the dealer's initial cost for the 60 cameras?***
(A) @@@$7 \%$ loss@@@
(B) @@@$13 \%$ loss@@@
(C) @@@$7 \%$ profit@@@
(D) @@@$13 \%$ profit@@@
(E) @@@$15 \%$ profit@@@

- Explanation for Problem 2:  
Given that $\$ 250$ is $20 \%$ greater than a camera's initial cost, it follows that the initial cost for each camera was $\left(\$ \frac{250}{1.2}\right)$. Therefore, the initial cost for the 60 cameras was $60\left(\$ \frac{250}{1.2}\right)$. The total revenue is the sum of the amount obtained from selling $60-6=54$ cameras for $\$ 250$ each and the $\left(\frac{1}{2}\right)\left(\$ \frac{250}{1.2}\right)$ refund for each of 6 cameras, or $(54)(\$ 250)+(6)\left(\frac{1}{2}\right)\left(\$ \frac{250}{1.2}\right)$. The total profit, as a percent of the total initial cost, is $\left(\frac{(\text { total revenue })-(\text { total initial cost })}{(\text { total initial cost })} \times 100\right) \%=$ $\left(\left(\frac{(\text { total revenue })}{(\text { total initial cost })}-1\right) \times 100\right) \%$. Using the numerical expressions obtained above, $\frac{\text { (total revenue) }}{\text { (total initial cost) }}-1$
$=\frac{(54)(250)+6\left(\frac{1}{2}\right)\left(\frac{250}{1.2}\right)}{(60)\left(\frac{250}{1.2}\right)}-1$
$=\frac{54+3\left(\frac{1}{1.2}\right)}{(60)\left(\frac{1}{1.2}\right)}-1$
by substitution
$=\frac{54(1.2)+3}{60}-1$
by multiplying top and bottom by 1.2 and then canceling 1.2
\[
=\frac{67.8}{60}-1
\]
\[
\begin{array}{l}
=1.13-1 \\
=0.13
\end{array}
\]

Finally, $(0.13 \times 100) \%=13 \%$, which represents a profit since it is positive.
The correct answer is therefore (D).


- Problem 3:
***$\frac{0.99999999}{1.0001}-\frac{0.99999991}{1.0003}=$***
(A) @@@$10^{-8}$@@@
(B) @@@$3\left(10^{-8}\right)$@@@
(C) @@@$3\left(10^{-4}\right)$@@@
(D) @@@$2\left(10^{-4}\right)$@@@
(E) @@@$10^{-4}$@@@

- Explanation for Problem 3:
Calculations with lengthy decimals can be avoided by writing 0.99999999 as $1-10^{-8}$, 0.99999991 as $1-9\left(10^{-8}\right), 1.0001$ as $1+10^{-4}$, and 1.0003 as $1+3\left(10^{-4}\right)$. Doing this gives
$\frac{1-10^{-8}}{1+10^{-4}}-\frac{1-9\left(10^{-8}\right)}{1+3\left(10^{-4}\right)}$
$=\frac{\left[1+10^{-4}\right]\left[1-10^{-4}\right]}{1+10^{-4}}-\frac{1-9\left(10^{-8}\right)}{1+3\left(10^{-4}\right)}$
$=\frac{1-10^{-4}}{1}-\frac{1-9\left(10^{-8}\right)}{1+3\left(10^{-4}\right)}$
$=\frac{\left[1-10^{-4}\right]\left[1+3\left(10^{-4}\right)\right]-\left[1-9\left(10^{-8}\right)\right]}{1+3\left(10^{-4}\right)}$
$=\frac{1+3\left(10^{-4}\right)-10^{-4}-3\left(10^{-8}\right)-1+9\left(10^{-8}\right)}{1+3\left(10^{-4}\right)}$
$=\frac{2\left(10^{-4}\right)+6\left(10^{-8}\right)}{1+3\left(10^{-4}\right)}$
$=\frac{\left[2\left(10^{-4}\right)\right]\left[1+3\left(10^{-4}\right)\right]}{1+3\left(10^{-4}\right)}$
$=2\left(10^{-4}\right)$
The correct answer is therefore (D).

- Problem 4:
***Last Sunday a certain store sold copies of Newspaper A for $\$ 1.00$ each and copies of Newspaper B for $\$ 1.25$ each, and the store sold no other newspapers that day. If $r$ percent of the store's revenue from newspaper sales was from Newspaper $A$ and if $p$ percent of the newspapers that the store sold were copies of Newspaper $A$, which of the following expresses $r$ in terms of $p$ ?***
(A) @@@$\frac{100 p}{125-p}$@@@
(B) @@@$\frac{150 p}{250-p}$@@@
(C) @@@$\frac{300 p}{375-p}$@@@
(D) @@@$\frac{400 p}{500-p}$@@@
(E) @@@$\frac{500 p}{625-p}$@@@

- Explanation for Problem 4:
Let $N$ be the total number of newspapers that the store sold. Then, the number of copies of Newspaper A the store sold was $p \%$ of $N=\left(\frac{p}{100}\right) N$ and the revenue from those copies of Newspaper A, in dollars, was (1.00) $\left(\frac{p}{100}\right) N=\left(\frac{p}{100}\right) N$. The number of copies of Newspaper B the store sold was $(100-p) \%$ of $N=\left(\frac{100-p}{100}\right) N$ and the revenue from those copies of Newspaper $B$, in dollars, was $(1.25)\left(\frac{100-p}{100}\right) N=\left(\frac{5}{4}\right)\left(\frac{100-p}{100}\right) N$.
The store's total revenue from newspaper sales, in dollars, was $\left(\frac{p}{100}\right) N+\left(\frac{5}{4}\right)\left(\frac{100-p}{100}\right) N$, and the fraction of that revenue from the sale of Newspaper A was
\[
\begin{aligned}
\frac{\frac{p}{100} N}{\frac{p}{100} N+\left(\frac{5}{4}\right)\left(\frac{100-p}{100}\right) N} & =\frac{\frac{p}{100}}{\frac{4 p}{400}+\left(\frac{500-5 p}{400}\right)} \\
& =\frac{\frac{p}{100}}{\frac{4 p+500-5 p}{400}} \\
& =\frac{\frac{p}{100}}{\frac{500-p}{400}} \\
& =\left(\frac{p}{100}\right)\left(\frac{400}{500-p}\right) \\
& =\frac{4 p}{500-p}
\end{aligned}
\]
Since $r$ percent of the store's newspaper sales revenue was from Newspaper $A, \frac{r}{100}=\frac{4 p}{500-p}$, and so $r=\frac{400 p}{500-p}$.
The correct answer is therefore (D).

- Problem 5:
***Car $A$ is 20 miles behind $\mathrm{Car} B$, which is traveling in the same direction along the same route as $\mathrm{Car} A$. Car $A$ is traveling at a constant speed of 58 miles per hour and $\mathrm{Car} B$ is traveling at a constant speed of 50 miles per hour. How many hours will it take for $\mathrm{Car} A$ to overtake and drive 8 miles ahead of $\mathrm{Car} B$ ?***
(A) @@@1.5@@@
(B) @@@2.0@@@
(C) @@@2.5@@@
(D) @@@3.0@@@
(E) @@@3.5@@@

- Explanation for Problem 5:
Understand that Car A first has to travel 20 miles to catch up to Car B and then has to travel an additional 8 miles ahead of Car B, for a total of 28 extra miles to travel relative to Car B. It can be stated that Car A is traveling $58-50=8$ miles per hour faster than Car B. Solving the distance $=($ rate $)($ time $)$ formula for time yields $\frac{\text { distance }}{\text { rate }}=$ time
rate
By substitution into this formula, it will take Car A $\frac{28 \text { miles }}{8 \text { miles per hour }}=3.5$ hours to overtake and drive 8 miles ahead of Car B.
The correct answer is therefore (E).


- Problem 6:
***Car $A$ is 20 miles behind $\mathrm{Car} B$, which is traveling in the same direction along the same route as $\mathrm{Car} A$. Car $A$ is traveling at a constant speed of 58 miles per hour and $\mathrm{Car} B$ is traveling at a constant speed of 50 miles per hour. How many hours will it take for $\mathrm{Car} A$ to overtake and drive 8 miles ahead of $\mathrm{Car} B$ ?***
(A) @@@1.5@@@
(B) @@@2.0@@@
(C) @@@2.5@@@
(D) @@@3.0@@@
(E) @@@3.5@@@

- Explanation for Problem 6:
Understand that Car A first has to travel 20 miles to catch up to Car B and then has to travel an additional 8 miles ahead of Car B, for a total of 28 extra miles to travel relative to Car B. It can be stated that Car A is traveling $58-50=8$ miles per hour faster than Car B. Solving the distance $=($ rate $)($ time $)$ formula for time yields $\frac{\text { distance }}{\text { rate }}=$ time
rate
By substitution into this formula, it will take Car A $\frac{28 \text { miles }}{8 \text { miles per hour }}=3.5$ hours to overtake and drive 8 miles ahead of Car B.
The correct answer is therefore (E).

- Problem 7:
***For the past $n$ days, the average (arithmetic mean) daily production at a company was 50 units. If today's production of 90 units raises the average to 55 units per day, what is the value of $n$ ?***
(A) @@@30@@@
(B) @@@18@@@
(C) @@@10@@@
(D) @@@9@@@
(E) @@@7@@@

- Explanation for Problem 7:
Let $x$ be the total production of the past $n$ days. 
Using the formula average $=\frac{\text { sum of values }}{\text { number of values }}$ the information in the problem can be expressed in the following two equations
$50=\frac{x}{n}$
daily average of 50 units over the past $n$ days
$55=\frac{x+90}{n+1}$ increased daily average when including today's 90 units
Solving the first equation for $x$ gives $x=50$. Then substituting $50 n$ for $x$ in the second equation gives the following that can be solved for $n$ :
\[
\begin{aligned}
55 & =\frac{50 n+90}{n+1} \\
55(n+1) & =50 n+90 \\
55 n+55 & =50 n+90 \\
5 n & =35 \\
n & =7
\end{aligned}
\]
multiply both sides by $(n+1)$ distribute the 55 subtract $50 n$ and 55 from both sides divide both sides by 5
The correct answer is therefore (E).

- Problem 8:
***Xavier, Yvonne, and Zelda each try independently to solve a problem. If their individual probabilities for success are $\frac{1}{4}, \frac{1}{2}$, and $\frac{5}{8}$, respectively, what is the probability that Xavier and Yvonne, but not Zelda, will solve the problem?***
(A) @@@$\frac{11}{8}$@@@
(B) @@@$\frac{7}{8}$@@@
(C) @@@$\frac{9}{64}$@@@
(D) @@@$\frac{5}{64}$@@@
(E) @@@$\frac{3}{64}$@@@

- Explanation for Problem 8:
Since the individuals' probabilities are independent, they can be multiplied to figure out the combined probability. The probability of Xavier's success is given as $\frac{1}{4}$, and the probability of Yvonne's success is given as $\frac{1}{2}$. Since the probability of Zelda's success is given as $\frac{5}{8}$, then the probability of her NOT solving the problem is $1-\frac{5}{8}=\frac{3}{8}$.
Thus, the combined probability is $\left(\frac{1}{4}\right)\left(\frac{1}{2}\right)\left(\frac{3}{8}\right)=\frac{3}{64}$.
The correct answer is therefore (E).

- Problem 9:
***List T consists of 30 positive decimals, none of which is an integer, and the sum of the 30 decimals is $S$. The estimated sum of the 30 decimals, $E$, is defined as follows. Each decimal in $T$ whose tenths digit is even is rounded up to the nearest integer, and each decimal in $T$ whose tenths digit is odd is rounded down to the nearest integer; $E$ is the sum of the resulting integers. If $\frac{1}{3}$ of the decimals in Thave a tenths digit that is even, which of the following is a possible value of E-S?
I. -16
II. 6
III. 10***

(A) @@@I only@@@
(B) @@@I and II only@@@
(C) @@@I and III only@@@
(D) @@@II and III only@@@
(E) @@@I, II, and III@@@

- Explanation for Problem 9:
Since $\frac{1}{3}$ of the 30 decimals in $T$ have an even tenths digit, it follows that $\frac{1}{3}(30)=10$ decimals in $T$ have an even tenths digit. Let $T_{E}$ represent the list of these 10 decimals, let $S_{E}$ represent the sum of all 10 decimals in $T_{E}$, and let $E_{E}$ represent the estimated sum of all 10 decimals in $T_{E}$ after rounding. The remaining 20 decimals in $T$ have an odd tenths digit. Let $T_{O}$ represent the list of these 20 remaining decimals, let $S_{O}$ represent the sum of all 20 decimals in $T_{O}$, and let $E_{O}$ represent the estimated sum of all 20 decimals in $T_{0}$ after rounding. Note that $E=E_{E}+E_{O}$ and $S=S_{E}+S_{O}$ and hence $E-S=$ $\left(E_{E}+E_{O}\right)-\left(S_{E}+S_{O}\right)=\left(E_{E}-S_{E}\right)+\left(E_{O}-S_{O}\right)$.
The least values of $E_{E}-S_{E}$ occur at the extreme where each decimal in $T_{E}$ has tenths digit 8. Here, the difference between the rounded integer and the original decimal is greater than 0.1 . (For example, the difference between the integer 15 and 14.899 that has been rounded to 15 is 0.101 .) Hence, $E_{E}-S_{E}>10(0.1)=1$. The greatest values of $E_{E}-S_{E}$ occur at the other extreme, where each decimal in $T_{E}$ has tenths digit 0 . Here, the difference between the rounded integer and the original decimal is less than 1 . (For example, the difference between the integer 15 and 14.001 that
has been rounded to 15 is 0.999 .)
Hence, $E_{E}-S_{E}<10(1)=10$. Thus, $1<E_{E}-S_{E}<10$.
Similarly, the least values of $E_{O}-S_{O}$ occur at the extreme where each decimal in $T_{O}$ has tenths digit 9 . Here, the difference between the rounded integer and the original decimal is greater than -1 . (For example, the difference between the integer 14 and 14.999 that has been rounded to 14 is -0.999.) Hence $E_{O}-S_{O}>20(-1)=-20$.
The greatest values of $E_{O}-S_{O}$ occur at the other extreme where each decimal in $T_{O}$ has tenths digit 1 . Here, the difference between the rounded integer and the original decimal is less than or equal to -0.1 . (For example, the difference between the integer 14 and 14.1 that has been rounded to 14 is -0.1 .)
Hence, $E_{O}-S_{O} \leq 20(-0.1)=-2$.
Thus, $-20<E_{O}-S_{O} \leq-2$.
Adding the inequalities $1<E_{E}-S_{E}<10$ and $-20<$ $E_{O}-S_{O} \leq-2$ gives $-19<\left(E_{E}-S_{E}\right)+\left(E_{O}-S_{O}\right)<8$. Therefore, $-19<\left(E_{E}+E_{O}\right)-\left(S_{E}+S_{O}\right)<8$ and $-19<E-S<8$. Thus, of the values $-16,6$, and 10 for $E-S$, only -16 and 6 are possible.
Note that if $T$ contains 10 repetitions of the decimal 1.8 and 20 repetitions of the decimal 1.9, $S=10(1.8)+20(1.9)=18+38=56$ $E=10(2)+20(1)=40$, and $E-S=40-56=-16$.
Also, if $T$ contains 10 repetitions of the decimal 1.2 and 20 repetitions of the decimal 1.1, $S=10(1.2)+20(1.1)=12+22=34$, $E=10(2)+20(1)=40$, and $E-S=40-34=6$.
The correct answer is therefore (B).

"""

reading_comprehension_sample = """

ANSWER KEY
Here are the answers for the problems in the exam

- Problem 1:
###Jacob Burckhardt's view that Renaissance European women "stood on a footing of perfect equality" with Renaissance men has been repeatedly cited by feminist scholars as a prelude to their presentation of rich historical evidence of women's inequality. In striking contrast to Burckhardt, Joan Kelly in her famous 1977 essay, "Did Women Have a Renaissance?" argued that the Renaissance was a period of economic and social decline for women
relative both to Renaissance men and to medieval women. Recently, however, a significant trend among feminist scholars has entailed a rejection of both Kelly's dark vision of the Renaissance and Burckhardt's rosy one. Many recent works by these
scholars stress the ways in which differences among Renaissance women-especially in terms of social status and religion-work to complicate the kinds of generalizations both Burckhardt and Kelly made on the basis of their observations about
upper-class Italian women.
The trend is also evident, however, in works focusing on those middle- and upper-class European women whose ability to write gives them disproportionate representation in the historical
record. Such women were, simply by virtue of their literacy, members of a tiny minority of the population, so it is risky to take their descriptions of their experiences as typical of "female experience" in any general sense. Tina Krontiris, for example, in
her fascinating study of six Renaissance women writers, does tend at times to conflate "women" and "women writers," assuming that women's gender, irrespective of other social differences, including literacy, allows us to view women as a homogeneous
social group and make that group an object of analysis. Nonetheless, Krontiris makes a significant contribution to the field and is representative of those authors who offer what might be called a cautiously optimistic assessment of Renaissance
women's achievements, although she also stresses the social obstacles Renaissance women faced when they sought to raise their "oppositional voices." Krontiris is concerned to show women intentionally negotiating some power for themselves
(at least in the realm of public discourse) agànst potentially constraining ideologies, but in her sober and thoughtful concluding remarks, she suggests that such verbal opposition to cultural stereotypes was highly circumscribed; women seldom attacked the basic assumptions in the ideologies that oppressed them.###
***The author of the passage discusses Krontris primarly to provide an example of a writer who***
(A) @@@is highly critical of the writings of certain Renaissance women@@@
(B) @@@supports Kelly's view of women's status during the Renaissance@@@
(C) @@@has misinterpreted the works of certain Renaissance women@@@
(D) @@@has rejected the views of both Burckhardt and Kelly@@@
(E) @@@has studied Renaissance women in a wide variety of social and religious contexts@@@


- Explanation for Problem 1:
This question focuses on the author's reason for mentioning Krontiris's work. The passage states that Krontiris, in her discussion of six Renaissance women writers, is an example of icholars who are optimistic about women's achievements but also suggest that these women bared significant obstacles. She is a writer who, in other words, agrees with neither Kelly's negative Views nor Burckhardt's positive approach.
(A) The passage indicates that Krontiris uses the Renaissance women writers' works as historical evidence, not that she offered any criticism of the works themselves.
(B) Krontiris's work, according to the author, is cautiously optimistic about women's achievements during the Renaissance. This contradicts Kelly's view that the status of women declined during this time.
(C) The author suggests that Krontiris may have erred in taking her six subjects as representative of all women during the Renaissance, not that she made any misinterpretations of their actual writing.
(D) Correct. The author uses Krontiris as an example of those feminist scholars who have rejected the overgeneralized approaches of both Kelly and Burckhardt.
(E) The author makes clear that Krontiris's study focuses on literate Renaissance women, who constituted a small minority.
The correct answer is therefore D.


- Problem 2:
###Because the framers of the United States Constitution (written in 1787) believed that protecting property rights relating to inventions would encourage the new nation's economic growth, they gave
Congress - the national legislature - a constitutional mandate to grant patents for inventions. The resulting patent system has served as a model for those in other nations. Recently, however, scholars have questioned whether the American system helped
achieve the framers' goals. These scholars have contended that from 1794 to roughly 1830 , American inventors were unable to enforce property rights because judges were "antipatent" and routinely invalidated patents for arbitrary reasons. This
argument is based partly on examination of court decisions in cases where patent holders ("patentees") brought suit alleging infringement of their patent rights. In the 1820 s, for instance, 75 percent of verdicts were decided against the patentee.
The proportion of verdicts for the patentee began to increase in the 1830s, suggesting to these scholars that judicial attitudes toward patent rights began shifting then.
Not all patent disputes in the early nineteenth century were litigated, however, and litigated cases were not drawn randomly from the population of disputes. Therefore the rate of verdicts in favor of patentees cannot be used by itself to gauge changes in judicial attitudes
or enforceability of patent rights. If early judicial decisions were prejudiced against patentees, one might expect that subsequent courts-allegedly more supportive of patent rights-would reject the former legal precedents. But pre-1830
cases have been cited as frequently as later decisions, and they continue to be cited today, suggesting that the early decisions, many of which clearly declared that patent rights were a just recompense for inventive ingenuity,
provided a lasting foundation for patent law. The proportion of judicial decisions in favor of patentees began to increase during the $1830 \mathrm{~s}$ because of a change in the underlying population of cases brought to trial. This change was partly
due to an 1836 revision to the patent system: an examination procedure, still in use today, was instituted in which each application is scrutinized for its adherence to patent law. Previously, patents were automatically granted upon payment of a $30 fee.
***The passage implies that the scholars mentioned in line 8 would agree with which of the following criticisms of the American patent system before 1830 ?***
(A) @@@Its definition of property rights relating to inventions was too vague to be useful.@@@
(B) @@@Its criteria for the granting of patents were not clear.@@@
(C) @@@It made it excessively difficult for inventors to receive patents.@@@
(D) @@@It led to excessive numbers of patentinfringement suits.@@@
(E) @@@It failed to encourage national economic growth.@@@


- Explanation for Problem 2:
This question asks about a statement implied by the passage. The scholars mentioned in line 8 question whether U.S. patent law achieved its goal. That goal is described in the first sentence of the passage: to encourage America's economic growth. Thus, it is reasonable to conclude that the scholars would criticize the pre- 1830 patent system for failing to encourage economic growth.
A The scholars contend that judges rejected patents for arbitrary reasons, not because the definition of property rights was vague.
B The passage does not indicate that the scholars were critical of the criteria for granting patents.
C The scholars are concerned with inventors' attempts to protect their patents, not the difficulty of acquiring a patent in the first place.
D The passage does not imply that the scholars in question believed that too many patentinfringement suits were brought to court, but rather that too few succeeded.
E Correct. The scholars doubt that patent law helped to achieve its goal, which was to encourage economic growth.
The correct answer is therefore E.


- Problem 3:
###Among the myths taken as fact by the environmental managers of most corporations is the belief that environmental regulations affect all competitors in a given industry uniformly. In reality,
regulatory costs - and therefore compliancefall unevenly, economically disadvantaging some companies and benefiting others. For example, a plant situated near a number of larger noncompliant competitors is less likely to attract
the attention of local regulators than is an isolated plant, and less attention means lower costs.
Additionally, large plants can spread compliance costs such as waste treatment across a larger revenue base; on the other hand, some smaller
plants may not even be subject to certain provisions such as permit or reporting requirements by virtue of their size. Finally, older production technologies often continue to generate toxic wastes that were not regulated when the
technology was first adopted. New regulations have imposed extensive compliance costs on companies still using older industrial coal-fired burners that generate high sulfur dioxide and nitrogen oxide outputs, for example, whereas new
facilities generally avoid processes that would create such waste products. By realizing that they have discretion and that not all industries are affected equally by environmental regulation, environmental managers can help their companies
to achieve a competitive edge by anticipating regulatory pressure and exploring all possibilities for addressing how changing regulations will affect their companies specifically.###
***Which of the following best describes the relationship of the statement about large plants (lines 12-17) to the passage as a whole?***
(A) @@@It presents a hypothesis that is disproved later in the passage.@@@
(B) @@@It highlights an opposition between two ideas mentioned in the passage.@@@
(C) @@@It provides examples to support a claim made earlier in the passage.@@@
(D) @@@It exemplifies a misconception mentioned earlier in the passage.@@@
(E) @@@It draws an analogy between two situations described in the passage.@@@

- Explanation for Problem 3:
This question asks about the role played in the passage by the following statement: Additionally, large plants can spread compliance costs such as waste treatment across a larger revenue base; on the other band, some smaller plants may not even be subject to certain provisions such as permit or reporting requirements by virtue of their size. This statement describes situations in which compliance costs for plants of different sizes may differ, which serve as evidence in support of the passage's main claim: that environmental regulations do not affect all competitors in a given industry uniformly.
A The statement in question is not a hypothesis; rather, it reports factors that are known to affect the varying impact of environmental regulations.
B This is too vague to be a good description of the kind of relationship the question asks about. The highlighted statement does present a contrast - it suggests that larger plants' compliance costs are lower under some circumstances, while smaller plants' compliance costs are lower under other circumstances. But this purports to state two facts rather than mere ideas; they are contrasting facts but not in any meaningful sense opposed, since they can easily coexist.
C Correct. The statement provides examples to support the initial claim made in the passage that regulatory costs fall unevenly on competitors in an industry: large plants can spread compliance costs around, and smaller plants may not even have to pay certain costs.
D This statement helps to dispel, not exemplify, a misconception mentioned earlier in the passage-i.e., the myth that environmental regulations affect all companies in an industry the same way.
E The statement does not suggest that the situation of larger and smaller plants is similar (or analogous) to any other situation mentioned in the passage.
The correct answer is therefore C.
"""



critical_reasoning_example = """

ANSWER KEY
Here are the answers for the problems in the exam

- Problem 1:
###One way to judge the performance of a company is to compare it with other companies. This technique, commonly called "benchmarking," permits the manager of a company to discover better industrial practices and can provide a justification for the adoption of good practices.###
***Any of the following, if true, is a valid reason for benchmarking the performance of a company against companies with which it is not in competition rather than against competitors EXCEPT:***
(A) @@@Comparisons with competitors are most likely to focus on practices that the manager making the comparisons already employs.@@@
(B) @@@Getting "inside" information about the unique practices of competitors is particularly difficult.@@@
(C) @@@Since companies that compete with each other are likely to have comparable levels of efficiency, only benchmarking against noncompetitors is likely to reveal practices that would aid in beating competitors.@@@
(D) @@@Managers are generally more receptive to new ideas that they find outside their own industry.@@@
(E) @@@Much of the success of good companies is due to their adoption of practices that take advantage of the special circumstances of their products or markets.@@@

- Explanation for Problem 1:
Situation: "Benchmarking" is a technique for judging the performance of a company by comparing it with other companies. The goal is to find and adopt better industrial practices.
Reasoning : Which one condition does NOT recommend benchmarking against noncompetitors? Which one condition IS a well-founded reason to benchmark against competitors? First, sort through the given information and the answer choices for the question to gain an understanding of the potential advantages or disadvantages of comparing a company to its competitors or to noncompetitors. What are the reasons in favor of benchmarking against noncompetitors? Information about noncompeting companies is easier to obtain; it can offer new insights; and it may be easier to put into practice. Why then might a manager choose to benchmark against competitors? Competing companies do share special circumstances involving products and markets. If companies are often successful because of practices related to these special circumstances within their industry, then benchmarking against competitors will reveal these practices and so be more fruitful than benchmarking against noncompetitors.

A Since benchmarking against competitors would yield few new practices, it would be better to benchmark against noncompetitors.
B If information about competitors is hard to obtain, benchmarking against noncompetitors is preferable.
C Since benchmarking against noncompetitors would yield practices useful in beating competitors, benchmarking against noncompetitors is preferable.
D If managers are more likely to adopt new practices learned from benchmarking against noncompetitors, then this technique is preferable.
E Correct. This statement properly identifies the rationale that supports a company's benchmarking against its competitors.
The correct answer is therefore E.

- Problem 2:
###With seventeen casinos, Moneyland operates the most casinos in a certain state. Although intent on expanding, it was outmaneuvered by Apex Casinos in negotiations to acquire the Eldorado chain. To complete its acquisition of Eldorado, Apex must sell five casinos to comply with a state law forbidding any owner to operate more than one casino per county. Since Apex will still be left operating twenty casinos in the state, it will then have the most casinos in the state.###
***Which of the following, if true, most seriously undermines the prediction?***
(A) @@@Apex, Eldorado, and Moneyland are the only organizations licensed to operate casinos in the state.@@@
(B) @@@The majority of Eldorado's casinos in the state will need extensive renovations if they are to continue to operate profitably.@@@
(C) @@@Some of the state's counties do not permit casinos.@@@
(D) @@@Moneyland already operates casinos in the majority of the state's counties.@@@
(E) @@@Apex will use funds it obtains from the sale of the five casinos to help fund its acquisition of the Eldorado chain.@@@

- Explanation for Problem 2:
Situation: Moneyland operates seventeen casinos, the most in a certain state, and is intent on expanding. Another operator, Apex Casinos, is acquiring the Eldorado casino chain, but must sell five casinos to comply with a state law forbidding any owner to operate more than one casino per county. After these transactions, Apex will operate twenty casinos in the state.
Reasoning: What observation would cast the most doubt on the prediction that Apex will have the most casinos in the state after the transactions? Apex will operate twenty casinos, whereas Moneyland now operates just seventeen, and no one else operates even that many. It follows that Apex will operate more casinos after its transactions than Moneyland or any other one owner now operates. However, if Moneyland also acquires three or more casinos during the transactions, then Apex will not have the most casinos in the state afterward. Thus, any observation suggesting that Moneyland is about to acquire several casinos would undermine the prediction.
A Correct. Since Apex is acquiring Eldorado, Moneyland and Apex will be the only remaining licensed casino operators in the state. Therefore, Moneyland is the only likely buyer for the five casinos Apex needs to sell. So Moneyland is likely to acquire the five casinos during the sale and end up with twenty-two casinos-more than Apex.
B This does not undermine the prediction. Even if the Eldorado casinos cannot operate profitably for long without extensive renovations, Apex will still have twenty casinos immediately after its transactions.
C This supports rather than undermines the prediction. If fewer counties permit casinos, there will be fewer opportunities for Moneyland or any other operator to acquire more casinos to surpass the twenty Apex will own.
D This supports rather than undermines the prediction. If Moneyland's seventeen casinos are in most of the state's counties already, then there are fewer counties in which Moneyland could acquire additional casinos to surpass the twenty Apex will own.
E This supports rather than undermines the prediction. Apex's use of the funds from selling the five casinos to acquire the Eldorado chain will not help anyone else to acquire more casinos to surpass the twenty Apex will own.
The correct answer is therefore A.

- Problem 3:
***Which of the following most logically completes the argument?***
###The attribution of the choral work Lacrimae to the composer Pescard (1400-1474) has been regarded as tentative, since it was based on a single treatise from the early 1500 s that named Pescard as the composer. Recently, several musical treatises from the late 1500 s have come to light, all of which name Pescard as the composer of Lacrimae. Unfortunately, these newly discovered treatises lend no support to the attribution of Lacrimae to Pescard, since###
(A) @@@the treatise from the early 1500 s misidentifies the composers of some of the musical works it considers@@@
(B) @@@the author of the treatise from the early 1500 s had no very strong evidence on which to base the identification of Pescard as the composer of Lacrimae@@@
(C) @@@there are works that can conclusively be attributed to Pescard that are not even mentioned in the treatise from the early 1500s@@@
(D) @@@the later treatises probably had no source for their attribution other than the earlier treatise@@@
(E) @@@no known treatises from the 1600 s identify Pescard as the composer of Lacrimae@@@


- Explanation for Problem 3:
Situation: A choral work has been tentatively attributed to Pescard based on a single treatise from the early 1500 s. But several treatises from the late 1500 s have recently been discovered, and all of them attribute the work to Pescard.
Reasoning: Which of the answer choices provides the strongest reason for the conclusion? The argument's conclusion is that the newly discovered late-1500 treatises lend no support to the attribution of Lacrimae to Pescard. It is worth noting that prior to the conclusion the passage provides information which suggests that these newly discovered treatises do lend support to the attribution. So the question is: Why don't they? A good reason for thinking they do not is that the newly discovered treatises probably derive solely from the attribution given in the earlier text. Thus the attributions in the later treatises are only as reliable as the attribution in the earlier treatise-and the argument suggests that that reliability has not been conclusively established.
A This makes the treatise from the early 1500 s less reliable, but it does not explain why the newly discoverec treatises are unreliable.
B Like answer choice (A), this is irrelevant. The question is not why the treatise from the early 1500 s fails to lend support to the attribution but why the treatises from the late 1500 s fail to do so.
C This is irrelevant because it does not refer to the newly discovered treatises whose attribution of Lacrimae is at issue.
D Correct. The question is whether these newly discovered treatises lend additional support. Lacrimae has already been tentatively attributed to Pescard based on the text from the early 1500 s. So, if the later treatises base their attribution solely on the earlier treatise, then they provide no additional support beyon that already provided by the earlier treatise.
E This leaves open the possibility that there was no treatise at all in the 1600 s that discussed Pescard or Lacrimae. Also, it fails to provide significant evidence either for or against Pescard's having composed Lacrimae. But even if it did provide such evidence, it would be irrelevant because the issue is why the late-1500 treatises fail to provide significant support for the attribution of Lacrimae to Pescard, not whether Pescard composed the work.
The correct answer is therefore D.
"""


sentence_correction_example = """

ANSWER KEY
Here are the answers for the problems in the exam

- Problem 1:
###Whereas in mammals the tiny tubes that convey nutrients to bone cells are arrayed in parallel lines, in birds the tubes form a random pattern.###
(A) @@@Whereas in mammals the tiny tubes that convey nutrients to bone cells are arrayed in parallel lines, in birds the tubes@@@
(B) @@@Whereas the tiny tubes for the conveying of nutrients to bone cells are arrayed in mammals in parallel lines, birds have tubes that@@@
(C) @@@Unlike mammals, where the tiny tubes for conveying nutrients to bone cells are arrayed in parallel lines, birds' tubes@@@
(D) @@@Unlike mammals, in whom the tiny tubes that convey nutrients to bone cells are arrayed in parallel lines, the tubes in birds@@@
(E) @@@Unlike the tiny tubes that convey nutrients to bone cells, which in mammals are arrayed in parallel lines, in birds the tubes@@@

- Explanation for Problem 1:
Whereas introduces two contrasting situations or events and should be followed by parallel structures. In this sentence, whereas is immediately followed by a clause beginning with the prepositional phrase in mammals; this means that the second part of the sentence must also be a clause that opens with a preposition that functions in the same way-in this case, in birds. This structure clarifies that the things being contrasted are the tubes in mammals and the tubes in birds. Incorrect versions of the sentence grammatically contrast tubes and birds, mammals and tubes, or birds and mammals.
A Correct. Parallel structures make clear that the tubes in mammals are being contrasted with the tubes in birds.
B The faulty parallelism results in a sentence that is confusing and unnecessarily wordy.
C The sentence compares mammals and birds' tubes.
D Because of faulty parallelism, this sentence also compares mammals and tubes in birds.
E This structure is wordy and confusing because of faulty parallelism.
The correct answer is therefore A.


- Problem 2:
###Australian embryologists have found evidence that suggests that the elephant is descended from an aquatic animal, and its trunk originally evolving as a kind of snorkel.###
(A) @@@that suggests that the elephant is descended from an aquatic animal, and its trunk originally evolving@@@
(B) @@@that has suggested the elephant descended from an aquatic animal, its trunk originally evolving@@@
(C) @@@suggesting that the elephant had descended from an aquatic animal with its trunk originally evolved@@@
(D) @@@to suggest that the elephant had descended from an aquatic animal and its trunk originally evolved@@@
(E) @@@to suggest that the elephant is descended from an aquatic animal and that its trunk originally evolved@@@

- Explanation for Problem 2:
The clearest, most economical way of expressing the two things suggested by Australian embryologists' evidence is to format them as relative clauses serving as parallel direct objects of the verb suggest. It is awkward and confusing to string together relative clauses: evidence that suggests that the elephant. ... A clearer way of making this connection is to turn the verb suggests into a participle modifying evidence. The word descended is a predicate adjective following the present-tense verb is and describing the presentday elephant. The verb evolved should be past tense because it describes how the trunk of the elephant originally evolved, not how it is evolving today.
A The string of relative phrases is awkward and confusing; the phrase following the conjunction and is not parallel with the relative clause that the elephant is descended....
B The evidence still suggests these things about the evolution of the elephant and its trunk, so the present-perfect verb tense is inaccurate.
C Had descended is the wrong verb tense; with cannot be followed by an independent clause.
D Had descended is the wrong tense; the phrase following the conjunction and does not parallel the relative clause that precedes the conjunction.
E Correct. The two dependent clauses beginning with that are in parallel form and contain verbs in the correct tenses.
The correct answer is therefore E.

- Problem 3:
###In no other historical sighting did Halley's Comet cause such a worldwide sensation as did its return in 1910-1911.###
(A) @@@did its return in 1910-1911@@@
(B) @@@had its 1910-1911 return@@@
(C) @@@in its return of 1910-1911@@@
(D) @@@its return of 1910-1911 did@@@
(E) @@@its return in 1910-1911@@@

- Explanation for Problem 3:
The single subject of this sentence is Halley's Comet, and its single verb phrase is did cause. The comparison presented by the sentence is between adverbial phrases describing times when the comet was seen. Grammatically, the items being compared are parallel prepositional phrases beginning with the preposition in: in no other sighting and in its return in 1910-1911. This is the clearest, most economical way of presenting the information. The options that introduce a second verb (did or had ) violate the parallelism and introduce a comparison between the comet itself (subject of the verb did cause) and the comet's return (subject of the verb did or had).
A This sentence implies a comparison between the comet and its return.
B This sentence implies a comparison between the comet and its return; had is the wrong auxiliary verb form because it must be followed by caused instead of cause.
C Correct. The parallel prepositional phrases in this sentence correctly compare times when the comet was sighted.
D This sentence implies a comparison between the comet and its return.
E This sentence violates parallelism, implying a comparison between a prepositional phrase and a noun phrase.
The correct answer is therefore C.

"""

############################################################################## STRUCTURING EXAMPLE ###################################################################################
############################################################################## STRUCTURING EXAMPLE ###################################################################################

cleaning_text_examples = """
- Example 1:
    - Input:
    Quantitative Reasoning
    Whiteboard
    Flag for $R$
    Is $r$ to the right of -6 on the number line?
    (1) $r$ is between -4 and -1 on the number line.
    (2) $r$ is between -3 and 1 on the number line.
    Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.
    Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.
    BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.
    EACH statement ALONE is sufficient.
    Statements (1) and (2) TOGETHER are NOT sufficient.
    Help
    ↓ Save for Later
    II Pause Exam
    [3 Expandn\
    - Output:
    (data sufficency, 
    ***Is $r$ to the right of -6 on the number line?***
    (1) $r$ is between -4 and -1 on the number line.
    (2) $r$ is between -3 and 1 on the number line.
    A) @@@Statement (1) ALONE is sufficient, but statement (2) alone is not sufficient.@@@
    B) @@@Statement (2) ALONE is sufficient, but statement (1) alone is not sufficient.@@@
    C) @@@BOTH statements TOGETHER are sufficient, but NEITHER statement ALONE is sufficient.@@@
    D) @@@EACH statement ALONE is sufficient.@@@
    E) @@@Statements (1) and (2) TOGETHER are NOT sufficient.@@@)
- Example 2:
    - Input:
    $\mathrm{X}$ : In order to reduce the amount of plastic in landfills, legislatures should impose a ban on the use of plastics for packaging goods.
    Y: Impossible! Plastic packaging is necessary for public safety. Consumers will lose all of the safety features that plastic offers, chiefly tamperresistant closures and shatterproof bottles.
    Which of the following best describes the weak point in Y's response to X's proposal?
    $Y$ ignores the possibility that packaging goods in materials other than plastic might provide the same safety features that packaging in plastic offers.
    The economic disadvantages of using plastics as a means of packaging goods are not taken into consideration.
    $Y$ attempts to shift the blame for the large amount of plastic in landfills from the users of plastic packaging to the legislators.
    Y does not consider the concern of some manufacturers that safety features spoil package appearances.
    $Y$ wrongly assumes that $X$ defends the interests of the manufacturers rather than the interests of the consumers.
    - Output:
    (critical reasoning,
    ###X: In order to reduce the amount of plastic in landfills, legislatures should impose a ban on the use of plastics for packaging goods.
    Y: Impossible! Plastic packaging is necessary for public safety. Consumers will lose all of the safety features that plastic offers, chiefly tamperresistant closures and shatterproof bottles.###
    ***Which of the following best describes the weak point in Y's response to X's proposal?***
    A) @@@$Y$ ignores the possibility that packaging goods in materials other than plastic might provide the same safety features that packaging in plastic offers.@@@
    B) @@@The economic disadvantages of using plastics as a means of packaging goods are not taken into consideration.@@@
    C) @@@$Y$ attempts to shift the blame for the large amount of plastic in landfills from the users of plastic packaging to the legislators.@@@
    D) @@@Y does not consider the concern of some manufacturers that safety features spoil package appearances.@@@
    E) @@@$Y$ wrongly assumes that $X$ defends the interests of the manufacturers rather than the interests of the consumers.@@@)
- Example 3:
    - Input:
    Verbal Reasoning
    Whiteboard
    Time Remaining: 00:30:02
    D. 11 of 36
    For the farmer who takes care to keep them cool, providing them with high-energy feed, and milking them regularly, Holstein cows are producing an average of 2,275 gallons of milk each per year.
    providing them with high-energy feed, and milking them regularly, Holstein cows are producing
    providing them with high-energy feed, and milked regularly, the Holstein cow produces
    provided with high-energy feed, and milking them regularly, Holstein cows are producing
    provided with high-energy feed, and milked regularly, the Holstein cow produces
    provided with high-energy feed, and milked regularly, Holstein cows will produce
    o Help ¿ Save for Later II Pause Exam :: Expand

    - Output:
    (sentence correction,
    ###For the farmer who takes care to keep them cool, providing them with high-energy feed, and milking them regularly, Holstein cows are producing an average of 2,275 gallons of milk each per year.###
    A) @@@providing them with high-energy feed, and milking them regularly, Holstein cows are producing@@@
    B) @@@providing them with high-energy feed, and milked regularly, the Holstein cow produces@@@
    C) @@@provided with high-energy feed, and milking them regularly, Holstein cows are producing@@@
    D) @@@provided with high-energy feed, and milked regularly, the Holstein cow produces@@@
    E) @@@provided with high-energy feed, and milked regularly, Holstein cows will produce@@@)

- Example 4:
    - Input:
    Quantitative Reasoning
    Whiteboard
    29 of 31    
    Elag for Review
    At the end of the first quarter, the share price of a certain mutual fund was 20 percent higher than it was at the beginning of the year. At the end of the second quarter, the share price was 50 percent higher than it was at the beginning of the year. What was the percent increase in the share price from the end of the first quarter to the end of the second quarter?
    $20 \%$
    $25 \%$
    $30 \%$
    $33 \%$
    $40 \%$
    ¿ Save for Later II Pause Exam :2 Expand 

    - Output:
    (problem solving,
    ***At the end of the first quarter, the share price of a certain mutual fund was 20 percent higher than it was at the beginning of the year. At the end of the second quarter, the share price was 50 percent higher than it was at the beginning of the year. What was the percent increase in the share price from the end of the first quarter to the end of the second quarter?***
    A) @@@$20 \%$@@@
    B) @@@$25 \%$@@@
    C) @@@$30 \%$@@@
    D) @@@$33 \%$@@@
    E) @@@$40 \%$@@@)


- Example 5:
    - Input:
    Verbal Reasoning
    Whiteboard
    Kemaining: 00:08:12 30 of 36
    Elag for Roviow
    Is it possible to decrease inflation without causing a recession and its concomitant increase in unemployment? The orthodox answer is "no." Whether they support the "inertia" theory of inflation (that today's inflation rate is caused by yesterday's inflation, the state of the economic cycle, and external influences such as import prices) or the "rational expectations" theory (that inflation is caused by workers' and employers' expectations, coupled with a lack of credible monetary and fiscal policies), most economists agree that tight monetary and fiscal policies, which cause recessions, are necessary to decelerate inflation. They point out that in the 1980's, many European countries and the United States conquered high (by these countries' standards) inflation, but only by applying tight monetary and fiscal policies that sharply increased unemployment. Nevertheless, some governments' policymakers insist that direct controls on wages and prices, without tight monetary and fiscal policies, can succeed in decreasing inflation. Unfortunately, because this approach fails to deal with the underlying causes of inflation, wage and price controls eventually collapse, the hitherto-repressed inflation resurfaces, and in the meantime, though the policymakers succeed in avoiding a recession, a frozen structure of relative prices imposes distortions that do damage to the economy's prospects for long-term growth.
    The passage suggests that the high inflation in the United States and many European countries in the 1980's differed from inflation elsewhere in which of the following ways?
    It fit the rational expectations theory of inflation but not the inertia theory of inflation.
    It was possible to control without causing a recession.

    It was easier to control in those countries by applying tight monetary and fiscal policies than it would have been elsewhere.
    It was not caused by workers' and employers' expectations.
    It would not necessarily be considered high elsewhere.
    O Help \& Save for Later II Pause Exam :2 Expand
    - Output:
    (reading comprehension,
    ###Is it possible to decrease inflation without causing a recession and its concomitant increase in unemployment? The orthodox answer is "no." Whether they support the "inertia" theory of inflation (that today's inflation rate is caused by yesterday's inflation, the state of the economic cycle, and external influences such as import prices) or the "rational expectations" theory (that inflation is caused by workers' and employers' expectations, coupled with a lack of credible monetary and fiscal policies), most economists agree that tight monetary and fiscal policies, which cause recessions, are necessary to decelerate inflation. They point out that in the 1980's, many European countries and the United States conquered high (by these countries' standards) inflation, but only by applying tight monetary and fiscal policies that sharply increased unemployment. Nevertheless, some governments' policymakers insist that direct controls on wages and prices, without tight monetary and fiscal policies, can succeed in decreasing inflation. Unfortunately, because this approach fails to deal with the underlying causes of inflation, wage and price controls eventually collapse, the hitherto-repressed inflation resurfaces, and in the meantime, though the policymakers succeed in avoiding a recession, a frozen structure of relative prices imposes distortions that do damage to the economy's prospects for long-term growth.###
    ***The passage suggests that the high inflation in the United States and many European countries in the 1980's differed from inflation elsewhere in which of the following ways?***
    A) @@@It fit the rational expectations theory of inflation but not the inertia theory of inflation.@@@
    B) @@@It was possible to control without causing a recession.@@@
    C) @@@It was easier to control in those countries by applying tight monetary and fiscal policies than it would have been elsewhere.@@@
    D) @@@It was not caused by workers' and employers' expectations.@@@
    E) @@@It would not necessarily be considered high elsewhere.@@@
    )

"""

cleaning_response_example = """
- Input 1: 
Situation: Healthy lungs produce a natural antibiotic that kills harmful bacteria on airway surfaces. People with cystic fibrosis, whose lungs produce normal amounts of the antibiotic, are unable to fight off such bacteria. Scientists hypothesize that the high salt concentration in the fluid on airway surfaces in the lungs of people with cystic fibrosis makes the antibiotic ineffective.
Reasoning: What experimental result would most decisively undermine the scientists' hypothesis? The scientists' hypothesis is that the high salt concentration in the fluid on airway surfaces in the lungs of people with cystic fibrosis makes the antibiotic ineffective at killing harmful bacteria. An experimental result that would most decisively undermine this hypothesis would be one that shows that even when the salt concentration is reduced to levels typical of healthy lungs, the lungs of people with cystic fibrosis are still unable to fight off harmful bacteria. This would suggest that the high salt concentration is not the reason for the antibiotic's ineffectiveness.
A This result would not undermine the hypothesis, as it does not address the effectiveness of the antibiotic in high-salt environments.
B This result would not undermine the hypothesis, as it does not address the effectiveness of the antibiotic in high-salt environments.
C This result would not undermine the hypothesis, as it does not address the effectiveness of the antibiotic in high-salt environments.
D Correct. This result would most decisively undermine the scientists' hypothesis. If the lungs of people with cystic fibrosis are unable to fight off harmful bacteria even when the salt concentration is reduced to levels typical of healthy lungs, this suggests that the high salt concentration is not the reason for the antibiotic's ineffectiveness.
E This result would not undermine the hypothesis, as it does not address the effectiveness of the antibiotic in high-salt environments.
The correct answer is therefore D.

- Output 1: 
D

- Input 2:
The percent increase from the end of the first quarter to the end of the second quarter is given by the formula:
Percent Increase = $\frac{Final Value - Initial Value}{Initial Value} \times 100$
Substituting the given values:
Percent Increase = $\frac{1.5P - 1.2P}{1.2P} \times 100$
Solving this gives:
Percent Increase = $\frac{0.3P}{1.2P} \times 100 = 25\%$
So, the percent increase in the share price from the end of the first quarter to the end of the second quarter was 25%.
The correct answer is therefore (B).

- Output 2: 
B

- Input 3:
This question asks about a comparison between inflation in the United States and many European countries in the 1980s and inflation elsewhere. The passage states that these countries conquered high inflation (by their standards) by applying tight monetary and fiscal policies that sharply increased unemployment. This suggests that what was considered high inflation in these countries might not be considered high elsewhere.

A) The passage does not suggest that the inflation in these countries fit one theory but not the other.
B) The passage states that these countries controlled inflation by applying policies that caused a recession, so it does not suggest that it was possible to control without causing a recession.
C) The passage does not compare the ease of controlling inflation in these countries with the ease of controlling it elsewhere.
D) The passage does not suggest that the inflation in these countries was not caused by workers' and employers' expectations.
E) Correct. The passage suggests that what was considered high inflation in the United States and many European countries might not be considered high elsewhere.
The correct answer is therefore E.

- Output 3:
E

- Input 4:
(1) Given that $u = v^2 + 1$, since $v^2$ is always nonnegative for any integer $v$, $u$ must be positive. Therefore, statement (1) is sufficient.
(2) Given that $u = w^4 + 1$, since $w^4$ is always nonnegative for any integer $w$, $u$ must be positive. Therefore, statement (2) is sufficient.
The correct answer is D; each statement alone is sufficient.

- Output 4:
D
"""

combining_text_example = """
- Input 1 : 
Parland's alligator population has been declining in recent years, primarily because of hunting. Alligators prey heavily on a species of freshwater fish that 
is highly valued as food by Parlanders, who had hoped that///on a species of freshwater fish that is highly valued as food by Parlanders, who had hoped that the decline in the alligator 
population would lead to an increase in the numbers of these fish available for human consumption. Yet the population of this fish species has also declined, even though 
the annual number caught for human consumption has not increased.
- Output 1 :
###Parland's alligator population has been declining in recent years, primarily because of hunting. Alligators prey heavily on a species of freshwater 
fish that is highly valued as food by Parlanders, who had hoped that the decline in the alligator population would lead to an increase in the numbers of these fish available 
for human consumption. Yet the population of this fish species has also declined, even though the annual number caught for human consumption has not increased.
Finally, you will output the final text by putting.### 

"""