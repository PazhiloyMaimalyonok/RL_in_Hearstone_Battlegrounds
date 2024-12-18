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
- [x] Добавить все карты с механикой баффа после призыва
    - [x] Выписать список карт
        - [x] 3/3 элементаль получает 0/1 за каждого элементаля, 1/5 мэрлок получает 1/0 после розыгрыша мэрлока
        - [x] Добавить использование use_flg в Card
        - [x] Сделать работу класса механик более общую, чтобы он бафал не конкретную карту, а скорее у него были бафы и таргеты для этих бафов, которых он потом бафал. Вероятно придется пересмотреть еще реализацию в классе Card
        - [x] 2/3 мурлок который дает всем мурлокам 0/2, 2/4 мурлокодракон получает 1/1 за каждый разыгранный батлкрай
        - [x] мэрлок 3/2 дает дружественному мэрлоку 0/1 кроме разыгранного, 3/2 элементаль дает дружественному элему 2/1 кроме разыгранного 

- [x] Добавить механику ивентов
- [x] Протестировать механику ивентов



- [ ] Сделать интеграцию с PettingZoo
    - [ ] Use PettingZoo to model your multi-agent game environment.
    - [ ] Implement the AEC API methods (reset, step, observe) to handle turn-based logic.
    - [ ] Map each PettingZoo agent to a player in your game.
    - [ ] Integrate with multi-agent RL training frameworks (e.g., RLlib) for actual training.


To-Do after MVP:
- [ ] Добавить автотесты
- [ ] Добавить карты
    - [ ] 2/2 Капля
    - [ ] 3/1 демон
- [ ] Добавить вторую таверну
- [ ] Добавить триплеты

Улучшения:
- unit тесты, логгирование

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
