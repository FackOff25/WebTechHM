VOTED = {0: "up", 1: "down", 2: "no"}

TAGS = ('Perl', 'Python', 'TechnoPark', 'MailRU', 'MySQL', 'Django')

BESTUSERS = ('Emperor', 'Sanguinius', 'Horus Lupercale', 'Alpharius', 'Roboute', 'Lion El\'Jonson', 'Mortarion',
             'Rogal Dorn', 'Angron', 'Lorgar')

USER = {
    'login': "Warmaster",
    'email': "damnImperor@chaos.warp",
    'nickname': "Horus Lupercal",
    'userPfp': "/static/img/warmaster.jpg",
    'isAuth': True
}

QUESTIONS = [
    {
        'id': i,
        'userPfp': "/static/img/racoon.jpg",
        'title': f"Question {i + 1}",
        'text': f"Text of question {i + 1}",
        'tags': [
            f"Tag {j + 1}" for j in range(3)
        ],
        'rating': i * 2 % 17 - 3,
        'voted': VOTED[i % 3]
    } for i in range(20)
]

ANSWERS = [
    {
        'userPfp': "/static/img/racoon.jpg",
        'text': f"answer {i + 1}",
        'rating': 30 - i,
        'correct': False,
        'voted': VOTED[i % 3]
    } for i in range(30)
]
