import pymorphy2
import re

from parse_gram import get_local_gram_table


def translate_gram(tag):
    gram_ = get_local_gram_table()

    compile_tag = dict()

    if tag.POS:
        pos = gram_.get(tag.POS, None)
        compile_tag.setdefault(
            "POS",
            pos and pos.get('desc')
        )

    if tag.animacy:
        animacy = gram_.get(tag.animacy, None)
        compile_tag.setdefault(
            "animacy",
            animacy and animacy.get('desc')
        )

    if tag.aspect:
        aspect = gram_.get(tag.aspect, None)
        compile_tag.setdefault(
            "aspect",
            aspect and aspect.get('desc')
        )

    if tag.case:
        case = gram_.get(tag.case, None)
        compile_tag.setdefault(
            "case",
            case and case.get('desc')
        )

    if tag.gender:
        gender = gram_.get(tag.gender, None)
        compile_tag.setdefault(
            "gender",
            gender and gender.get('desc')
        )

    if tag.involvement:
        involvement = gram_.get(tag.involvement, None)
        compile_tag.setdefault(
            "involvement",
            involvement and involvement.get('desc')
        )

    if tag.mood:
        mood = gram_.get(tag.mood, None)
        compile_tag.setdefault(
            "mood",
            mood and mood.get('desc')
        )

    if tag.number:
        number = gram_.get(tag.number, None)
        compile_tag.setdefault(
            "number",
            number and number.get('desc')
        )

    if tag.person:
        person = gram_.get(tag.person, None)
        compile_tag.setdefault(
            "person",
            person and person.get('desc')
        )

    if tag.tense:
        tense = gram_.get(tag.tense, None)
        compile_tag.setdefault(
            "tense",
            tense and tense.get('desc')
        )

    if tag.transitivity:
        transitivity = gram_.get(tag.transitivity, None)
        compile_tag.setdefault(
            "transitivity",
            transitivity and transitivity.get('desc')
        )

    if tag.voice:
        voice = gram_.get(tag.voice, None)
        compile_tag.setdefault(
            "voice",
            voice and voice.get('desc')
        )

    return compile_tag


def analyze_word(source: str):
    def parse_sentence(raw_sentence: str) -> list:
        return list(set(re.findall(r"[\w\-\\/\\']+", raw_sentence)))

    def parse_pymorphy2(word: str):
        morphy = pymorphy2.MorphAnalyzer()
        return morphy.parse(word)[:5]

    split_sentence = parse_sentence(source)

    return list(map(parse_pymorphy2, split_sentence))


def go_parse(string: str):
    result = analyze_word(string)

    parse_sentence = dict()

    for parts in result:
        word = parse_sentence.setdefault(
            parts[0].word, list()
        )
        for part in parts:
            word.append(
                {
                    'tags': translate_gram(part.tag),
                    'normal_form': part.normal_form,
                }
            )

    return parse_sentence


if __name__ == '__main__':

    sentence = """
    Наша команда занимается внедрений технологий ML в различные процессы
    Национального расчетного депозитария. Мы решаем как внутренние задачи IT,
    так и задачи бизнес-подразделений. В основном задачи связаны с
    обработкой естественного языка (NLP). Технологически наши решения
    представляют из себя Python-микросервисы либо Python-службы. 
    Ограничений по использованию инструментов или фреймворков нет – 
    выбираем наиболее подходящий для конкретной задачи инструмент. 
    Мы пишем unit- и автотесты. Исходные коды хранятся в Gitlab. Практикуем
    code review и merge requests. Настроены процессы CI/CD и мониторинга.
    """

    parse_sentence = go_parse(sentence)

    for word, parts in parse_sentence.items():
        print(word)
        print(parts)
        print('-' * 25 + '\n')
