# Файл с заданиями по проекту

- [x] Найти репозиторий
- [x] Ознакомиться с [базой по классам в питоне](https://devpractice.ru/python-lesson-14-classes-and-objects/)
- [x] Ознакомиться с основными классами: добавить описание, плюсы и минусы, идеи использования дальше. 
    - [x] Ознакомиться с классом Card
    - [x] Ознакомиться с классом Game
    - [x] Ознакомиться с классом Tavern
    - [x] Ознакомиться с классом Fight
- [x] запустить пару игр
- [x] Улучшить классы
    - [x] Улучшить класс Game
    - [x] Улучшить класс Fight
        - [x] Подготовить тестирование для Fight
        - [x] Улучшить класс Fight        
- [x] Обновить описания классов
- [x] Составить To Do лист по изменениям в игре v2
- [x] Выбрать пул карт (Всего 57 карт на 1 и 2 таверне)
    - [x] Выписать механики ([ссылка на сайт](https://hearthstone.blizzard.com/en-us/battlegrounds?bgCardType=minion&bgGameMode=solos&keyword=battlecry%0A&tier=1%2C2))
    - [x] Зафиналить список механик
    - [x] Зафиналить список карт
- [x] Добавить список механик в MVP to-do list ~~и оценить их~~
- [x] Реализовать класс механик
- [x] Переделать инициализацию карт с хардкодинга на чтение excel
- [ ] Добавить все карты с механикой баффа после призыва
    - [x] Выписать список карт
        - [x] 3/3 элементаль получает 0/1 за каждого элементаля, 1/5 мэрлок получает 1/0 после розыгрыша мэрлока
        - [x] Добавить использование use_flg в Card
        - [x] Протестить работу бафов у смавпстрайкера и молтен рока
        - [x] Подумать над реализацией общих батлкраев
            - [x] Сделать работу класса механик более общую, чтобы он бафал не конкретную карту, а скорее у него были бафы и таргеты для этих бафов, которых он потом бафал. Вероятно придется пересмотреть еще реализацию в классе Card
        - [x] 2/3 мурлок который дает всем мурлокам 0/2, 2/4 мурлокодракон получает 1/1 за каждый разыгранный батлкрай
        - [ ] мэрлок 3/2 дает дружественному мэрлоку 0/1 кроме разыгранного, 3/2 элементаль дает дружественному элему 2/1 кроме разыгранного 

- [ ] Добавить все карты с батлкраями
    - [ ] Что делать с батлкраями 1/1 демон который жрет, 3/2 демон который жрет,
- [ ] Добавить механику получения карты при продаже карты
- [ ] Добавить механику сплекрафта
    - [ ] 2/2 нага получает 1/1 за разыгранный спэл (реализовывать только со спелкраффтами?)
    
- [ ] Починить баг с бесплатными рероллами

- [ ] Подключить ко-пилот для кодинга

MVP to-do list:
- [ ] Бесплатные рероллы (s0)
- [ ] Триплеты (s2)
- [ ] drawing cards from the pool the same level or lower than your tavern (s1)
- [ ] Класс механик (s2)
- [ ] Механики для карт, которые я добавлю
    - [ ] Честные
        - [ ] Получает бафф при разыгрывании карты (9 карт)
        - [ ] Меняет таверну при разыгрывании карты (12 карт). Мб эту и верхнюю объединить
        - [ ] Особенности файта
    - [ ] Обычные механики
        - [ ] Таунт
        - [ ] Бабл
        - [ ] Десратл
- [ ] Интеграция с OpenAI Gym
    - [ ] State representation
    - [ ] Action space
    - [ ] Reward function
    - [ ] Episode structure
    - [ ] Observability

Проблемы:
1. Бесплатные рероллы

Улучшения:
- Добавить возможность картам быть нескольких классов. Изменения в Card
- triplets, drawing cards from the pool the same level or lower than your tavern, buffs, pygame visualization

* Идеи для мвп:
    + Из описаний:
        - Как реализовывать триплеты (Card)
        - Как реализовать правильное доставание карт из пула на первой таверне. Надо, чтобы ты не мог достать карты второго уровня (CardsPool, Tavern)
    + Что хотелось бы
        - Триплеты (Card или просто механика в Tavern)
        - Баффы карт (Tavern, Fight -- зависит от пула карт)
        - Интеграция с gym (Вот это пизда)????
    + Интеграция с Gym
        - State representation: Your game should have a clear and concise way to represent its state. This will be used to communicate the game's state to the reinforcement learning agent. A good state - representation should be
        - Action space: Define a clear set of actions that the agent can take. These actions should be:
        - Reward function: Design a reward function that provides feedback to the agent about its actions. The reward function should:
        - Episode structure: Your game should have a clear episode structure, which includes: Reset, Step, Done.
        - Observability: Ensure that the game state is observable by the agent. This means that the agent should have access to all the information it needs to make decisions.
