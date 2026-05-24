# Пересказ

The title of the article I have reviewed is "Evaluating the impact of pre-annotation on annotation speed and potential bias...".
The authors of the article are Todd Lingren and others. It was published in the Journal of the American Medical Informatics Association in 2014.
The research question addressed in the article is whether pre-annotation can increase labeling speed without introducing bias into the data.
The central theme of the article is the efficiency of NLP data annotation. It is dedicated to showing how dictionary-based methods reduce the cost and time of creating "gold standard" corpora.
The research includes experiments on 1,400 clinical trial documents using dictionary-based pre-annotation and ANOVA tests to analyze annotator performance.
The results indicate significant time savings, ranging from 13.85% to 21.5%, with no statistically significant drop in inter-annotator agreement.
In the discussion, the authors highlight that pre-annotation is a feasible and practical way to reduce labor costs in clinical NER tasks without affecting quality.
I found the article to be insightful because it directly relates to my current work of managing a dataset segmentation project for 20 students.

# Перевод

## Аннотация

Цель Представить серию экспериментов: (1) для оценки влияния предварительной аннотации на скорость ручной аннотации объявлений о клинических испытаниях; и (2) для проверки потенциальной предвзятости при использовании предварительной аннотации. 

Методы Для создания золотого стандарта было случайно выбрано 1400 объявлений о клинических испытаниях с веб-сайта clinicaltrials.gov и проведена двойная аннотация по диагнозам, признакам, симптомам, уникальным идентификаторам концепций Unified Medical Language System (UMLS) и кодам SNOMED CT. Для предварительной аннотации текста мы использовали два метода на основе словарей. Мы оценили время аннотирования и потенциальную предвзятость с помощью F-показателей и ANOVA-тестов и применили поправку Бонферрони. 

Результаты Экономия времени составила от 13,85% до 21,5% на каждую сущность. Согласованность между аннотаторами (IAA) составила от 93,4% до 95,5%. Не было статистически значимой разницы в IAA и производительности аннотаторов при предварительной аннотации. 

Выводы В каждой паре экспериментов аннотатор, имевший предварительно аннотированный текст, тратил меньше времени на аннотирование, чем аннотатор, имевший немеченый текст. Экономия времени была статистически значимой. Кроме того, предварительная аннотация не снизила IAA или производительность аннотатора. Предварительная аннотация на основе словаря является реальным и практичным методом снижения затрат на аннотирование распознавания клинических именованных сущностей в разделах о приемлемости объявлений о клинических испытаниях без введения смещения в процесс аннотирования. 

## Введение

Проекты по обработке естественного языка (NLP) требуют ручного аннотирования золотых стандартов корпусов для обучения и тестирования алгоритмов, основанных на машинном обучении, или, в случае методов, основанных на правилах, для тестирования эффективности правил. В свете высокой стоимости ручного аннотирования экспертами, исследователи NLP нуждаются в надежных методах для ускорения процесса аннотирования без искажения сгенерированного золотого стандарта. В нашем учреждении мы работаем над проектом, финансируемым NIH, по автоматизации отбора кандидатов для участия в клинических испытаниях с помощью алгоритмов NLP. Эта работа требует разработки значительного объема аннотированных вручную золотых стандартов. Как таковая, эта аннотация является очень трудоемкой и дорогостоящей. 

В данном исследовании наша цель — представить серию экспериментов: (1) оценить влияние предварительной аннотации на скорость ручной аннотации объявлений о клинических испытаниях (CTA); и (2) проверить потенциальную предвзятость при использовании предварительной аннотации. Мы определяем потенциальную предвзятость как увеличение расхождения между аннотаторами, измеряемое с помощью межаннотаторного согласия (IAA), или уменьшение согласия (называемое в нашем исследовании производительностью аннотатора) между аннотациями аннотатора с предварительно аннотированным текстом и конечным золотым стандартом. Задача аннотирования включала маркировку медицинских именованных сущностей в двух классах: заболевание/расстройство и признак/ симптом. Унифицированная медицинская языковая система (UMLS) Уникальные идентификаторы концепций (CUI) и коды SNOMED-CT также были аннотированы для каждой сущности. Остальная часть статьи построена следующим образом. В разделе «Предпосылки и значимость» мы представляем соответствующую литературу. 

В разделе «Данные и методы» мы описываем данные, экспериментальные методы и аналитические подходы. В разделе «Результаты» мы представляем результаты. В разделе «Обсуждение» мы обсуждаем выводы, ограничения и вопросы для будущих исследований. В заключительном разделе мы приводим наши выводы.

# New version

Good afternoon. I'm a Master's student. Today, I'll present the article "Evaluating the impact of pre-annotation on annotation speed and potential bias".

**The Why (Introduction)** To teach AI to understand medical texts, humans must manually highlight key terms (like names of diseases) to create a "gold standard". However, this manual work is incredibly slow and expensive. The researchers wanted to know: can a simple computer program speed up this process without lowering the final quality?

**The How (Methods)** The researchers tested a method called "pre-annotation" on 1,400 clinical trial documents. Like a spell-checker that underlines mistakes, they used a computer dictionary to quickly pre-highlight known medical words. Then, human experts stepped in. Instead of starting from a blank page, they just reviewed the text — deleting mistakes or adding missing words. The researchers then measured the time saved and the final quality.

**The What (Results)** The results were highly positive. The experts saved between 14% and 21% of their time. More importantly, the human experts didn't get lazy or blindly agree with the computer's mistakes (a problem called "bias"). Their accuracy and agreement with each other stayed extremely high — around 93% to 95%. Quality did not drop at all.

**The So What (Conclusions)** Ultimately, this study proves that simple dictionaries can safely help humans prepare data for AI. Saving 20% of time means saving thousands of hours and dollars, allowing us to build life-saving medical AI systems much faster and cheaper.

---

### 2. Вопросы для проверки понимания (Comprehension Questions)

**1. Why is the traditional way of preparing text for Artificial Intelligence considered a big problem?**

- **EN:** Because manually annotating texts takes a lot of time and is extremely expensive.

- **RU:** Потому что ручная разметка текста людьми занимает очень много времени и стоит слишком дорого.

**2. Can you explain the "pre-annotation" method using the analogy mentioned in the presentation?**

- **EN:** It is like a spell-checker in a text editor — the computer highlights the necessary words in advance, and the human simply checks and corrects them instead of searching from scratch.

- **RU:** Это похоже на проверку орфографии в текстовом редакторе — компьютер заранее подсвечивает нужные слова, а человек просто проверяет и исправляет их, вместо того чтобы искать всё с нуля.

**3. What was the main fear researchers had when giving human experts texts that were already highlighted by a computer?**

- **EN:** They feared "bias" — that people would get lazy, stop reading the text carefully, and blindly agree with the machine's mistakes.

- **RU:** Они боялись «предвзятости» (bias) — что люди станут ленивыми, перестанут вчитываться в текст и будут просто соглашаться с ошибками машины.

**4. Did the new computer-assisted method affect the final quality of the experts' work?**

- **EN:** No, the quality did not suffer. The human experts remained attentive, and the accuracy stayed at a high level.

- **RU:** Нет, качество не пострадало. Люди остались внимательными, и точность сохранилась на высоком уровне.

**5. How can the findings of this study help hospitals and IT companies in real life?**

- **EN:** It will save about 20% of time and money on data preparation, making it faster and cheaper to build useful AI systems for medicine.

- **RU:** Это сэкономит около 20% времени и денег на подготовку данных, что позволит быстрее и дешевле создавать полезные нейросети для медицины.
