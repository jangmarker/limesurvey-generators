from logging import debug
from string import Template


def generate(name, correct, wrong):
    debug(name)
    debug(correct)
    debug(wrong)

    t_max = Template('{max(0, sum($ifs)}')
    t_if_correct = Template('if(${question}_${key} == \'Y\', 1, 0)')
    t_if_wrong = Template('if(${question}_${key} == \'Y\', -1, 0)')

    ifs = []

    def apply_to_template(template, key): return template.substitute(question=name, key=key)

    def insert_into_ifs(if_statement): ifs.append(if_statement)

    def process_list(options, template): [
        insert_into_ifs(apply_to_template(template, option)) for option in options
    ]

    process_list(correct, t_if_correct)
    process_list(wrong, t_if_wrong)

    debug(ifs)
    return t_max.substitute(ifs=', '.join(ifs))
