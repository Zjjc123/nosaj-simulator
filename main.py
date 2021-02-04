from prompt_toolkit.validation import Validator, ValidationError
from PyInquirer import prompt, print_json

class IntValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

questions = [
    {
        'type': 'input',
        'name': 'interations',
        'message': 'Number of iterations to run for?',
        'validate': IntValidator,
    },
    {
        'type': 'input',
        'name': 'timestep',
        'message': 'Length of timestep?',
        'validate': FloatValidator,
    },
    {
        'type': 'confirm',
        'name': 'ss',
        'message': 'Screenshot?',
    },
    {
        'type': 'confirm',
        'name': 'init',
        'message': 'Use a preset condition?',
    }
]

ic_question = [
    {
        'type': 'list',
        'name': 'ic',
        'message': 'Preset Initial Condition?',
        'choices': [
            {
                'key': 'two',
                'name': 'Simple Two Body',
                'value': 1
            },
            {
                'key': 'sem',
                'name': 'Sun Earth Moon',
                'value': 2
            },
            {
                'key': 'solar',
                'name': 'Solar System',
                'value': 3
            }
        ],
    }
]

rand_question = [
    {
        'type': 'input',
        'name': 'rand',
        'message': 'How many particles?',
    }
]

args = prompt(questions)

if (args['init'] == True):
    args['ic'] = prompt(ic_question)['ic']
else:
    args['nrand'] = prompt(rand_question)['rand']

print(args)