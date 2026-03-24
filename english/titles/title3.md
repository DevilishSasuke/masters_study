# Пересказ

**1. Introduction (The Why)** Hello. Today, I want to discuss a major problem with modern GPS navigation systems. While apps like Google Maps show traffic, they cannot detect sudden changes on the road, such as a new pothole, a missing sewer cover, or a collapsed bridge. Sadly, this lack of real-time information causes serious accidents. My presentation is about a new system that uses Artificial Intelligence to find road hazards in real-time to keep drivers safe.

**2. Methods (The How)** To solve this, the researchers collected about 5,000 pictures of different road conditions: potholes, wet surfaces, drain holes, sewer covers, and unpaved roads. They trained a fast AI "eye" called YOLOv8 to instantly recognize these problems. Instead of just testing the AI on a computer, they built a real web application. A user can turn on their phone or car camera, and the app will instantly scan the road, find the danger, and put a warning pin on a digital map with exact GPS coordinates.

**3. Results (The What)** The new AI proved to be incredibly fast and smart. It takes only 11.4 milliseconds to process one image, making it perfect for live video streams. It was also very accurate. For example, it correctly identified unpaved roads 95% of the time and sewer covers 82% of the time, which is much better than older AI models.

**4. Conclusion (The So What)** In conclusion, this project shows how we can make our everyday navigation apps much smarter. If this live hazard scanner is added to our phones or cars, it will instantly warn drivers about sudden dangers. It also saves the location of every pothole in a database, which helps city workers quickly find and fix damaged roads.

### 5 Comprehension Questions (Вопросы и ожидаемые ответы)

**1. What is the main problem with modern navigation apps like Google Maps?**

- **EN:** They rely on old maps and cannot detect sudden, real-time road hazards like missing sewer covers or new potholes.

- **RU:** Они полагаются на старые карты и не могут обнаруживать внезапные дорожные опасности в реальном времени, например, открытые люки или новые ямы.

**2. What kinds of road anomalies did the AI learn to recognize?**

- **EN:** The AI learned to find potholes, wet surfaces, drain holes, sewer covers, and unpaved roads.

- **RU:** ИИ научился находить выбоины (ямы), мокрые поверхности, водостоки, канализационные люки и грунтовые (немощеные) дороги.

**3. How does the web application help drivers in real life?**

- **EN:** The app uses a live camera to find dangers and puts a warning pin on a digital map using exact GPS coordinates.

- **RU:** Приложение использует камеру в реальном времени для поиска опасностей и ставит предупреждающую метку на цифровой карте, используя точные GPS-координаты.

**4. Was the new AI fast enough to be used in a moving car?**

- **EN:** Yes, it is extremely fast. It takes only about 11 milliseconds to analyze one picture, which is perfect for live video.

- **RU:** Да, он невероятно быстрый. На анализ одной картинки уходит всего около 11 миллисекунд, что идеально для живого видео.

**5. How can this technology be useful for city maintenance workers?**

- **EN:** The system saves the exact location and type of every road hazard in a database, so workers know exactly where to go to fix the road.

- **RU:** Система сохраняет точное местоположение и тип каждой дорожной опасности в базе данных, поэтому рабочие точно знают, куда ехать, чтобы починить дорогу.

# Перевод

## Аннотация

Существующие навигационные системы не способны предоставлять информацию о состоянии дорожного покрытия в режиме реального времени, что создает серьезные угрозы безопасности. В рамках данного исследования разработана надежная система, использующая модель YOLOv8 для обнаружения аномалий дорожного покрытия, включая выбоины, мокрые участки, канализационные люки, водосточные отверстия и грунтовые дороги. YOLOv8 демонстрирует явные преимущества по сравнению со своими предшественниками, такие как повышенная точность, сокращенное время вывода (18 мс на изображение, 56 кадров в секунду) и механизм обнаружения без якорей, который упрощает обучение и повышает точность обнаружения. В рамках исследования эта модель интегрирована в веб-приложение Flask, что позволяет осуществлять обнаружение и визуализацию на карте в режиме реального времени. Эта интеграция в сочетании с постоянным хранением обнаруженных аномалий вместе с их GPS-координатами представляет собой новый подход к повышению безопасности дорожного движения и прозрачности. Оценки показали среднюю точность (mAP) 0,879 при пересечении над объединением (IoU) 0,5 и 0,604 при IoU 0,95, что подтверждает превосходную производительность и эффективность YOLOv8.

## Введение

Безопасность дорожного движения по-прежнему остается серьезной глобальной проблемой, поскольку навигационные системы зачастую не способны в режиме реального времени обнаруживать аномалии на дорогах, такие как выбоины, трещины и неровности. 24 ноября 2024 года трагический инцидент в штате Уттар-Прадеш, Индия, подчеркнул острую необходимость в улучшении возможностей навигационных систем по обнаружению таких аномалий. Трое мужчин погибли после того, как следовали указаниям GPS, которые привели их на недостроенный мост, в результате чего их автомобиль упал в реку Рамганга. Навигационная система не учла тот факт, что мост находился в стадии строительства и обрушился в 2022 году из-за наводнения, а отсутствие надлежащих предупреждающих знаков или ограждений еще больше усугубило риск. Этот инцидент не является единичным случаем. В сентябре 2022 года мужчина в Северной Каролине, США, погиб после того, как его GPS направил его к обрушившемуся мосту, который был выведен из эксплуатации еще в 2013 году, при этом навигационная система не предоставила никаких предупреждений или обновлений . Аналогичным образом, в 2019 году почти 100 водителей в Колорадо оказались в затруднительном положении после того, как, следуя указаниям GPS, выехали на непроходимую грунтовую дорогу, что подчеркнуло ограниченность существующих навигационных технологий в обнаружении опасностей на дорогах в режиме реального времени.
