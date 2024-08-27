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
- [ ] Выбрать пул карт (Всего 57 карт на 1 и 2 таверне)
    - [ ] Выписать механики ([ссылка на сайт](https://hearthstone.blizzard.com/en-us/battlegrounds?bgCardType=minion&bgGameMode=solos&keyword=battlecry%0A&tier=1%2C2))
    - [ ] Определить, сколько карт с этой механикой
    - [ ] Определить, на какие классы механика повлияет и примерную стоимость разработки
    - [ ] Зафиналить список механик
    - [ ] Зафиналить список механик
    
    
- [ ] Подключить ко-пилот для кодинга

MVP to-do list:
- [ ] Бесплатные рероллы (s0)
- [ ] Триплеты (s1)
- [ ] drawing cards from the pool the same level or lower than your tavern (s1)
- [ ] Механики для карт, которые я добавлю
    - [ ] Интеграция с OpenAI Gym
    - [ ] State representation
    - [ ] Action space
    - [ ] Reward function
    - [ ] Episode structure
    - [ ] Observability

Проблемы:
1. Бесплатные рероллы

Улучшения:
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
