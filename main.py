import argparse
from renderer import *

parser = argparse.ArgumentParser()

parser.add_argument('--iterations', help='number of iterations to run for', type=int, default=10000)
parser.add_argument('--timestep', help='length of timestep', type=float, default=-1)
parser.add_argument('--trail_length', help='length of trail', type=float, default=40)
parser.add_argument('--skip', help='# timesteps to skip when rendering', type=int, default=100)

parsed = parser.parse_args()

from prompt_toolkit.validation import Validator, ValidationError
from PyInquirer import prompt, print_json

class IntValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter an int',
                cursor_position=len(document.text))  # Move cursor to end

class FloatValidator(Validator):
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a float',
                cursor_position=len(document.text))  # Move cursor to end

questions = [
    {
        'type': 'confirm',
        'name': 'ss',
        'message': 'Screenshot?',
    },
    {
        'type': 'confirm',
        'name': 'plot_energy',
        'message': 'Plot energies?',
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

run_nbody(parsed, args)