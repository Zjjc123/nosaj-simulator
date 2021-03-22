import argparse
from renderer2d import *

## setup command line arguments
parser = argparse.ArgumentParser()

# optional arguments
parser.add_argument('--iterations', help='number of iterations to run for', type=int, default=10000)
parser.add_argument('--timestep', help='length of timestep', type=float, default=-1)
parser.add_argument('--trail_length', help='length of trail', type=float, default=40)
parser.add_argument('--skip', help='# timesteps to skip when rendering', type=int, default=100)

## optional skip CLI arguments (if invoked, cli will be skipped for faster simulating process)
parser.add_argument('--ss', help='(t/f) screenshot?', type=bool, default=None)
parser.add_argument('--plot', help='(t/f) plot energies?', type=bool, default=None)
parser.add_argument('--ic', help='initial positions (1: two body, 2: sun earth moon, 3: solar syste) ', type=int, default=None)

parsed = parser.parse_args()

## setup interactive arguments
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
        'type': 'list',
        'name': 'vis',
        'message': 'Select visualization mode.',
        'choices': ['2D', '3D']
    },
    {
        'type': 'confirm',
        'name': 'init',
        'message': 'Use a preset condition?',
    }
]

# select initial conditions
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

# random initialization
rand_question = [
    {
        'type': 'input',
        'name': 'nrand',
        'message': 'How many particles?',
        'validate': IntValidator,
    }
]

args = {}

# if optional skip CLI option is triggered (short cut for testing)
if (parsed.ss is not None or parsed.plot is not None or parsed.ic):
    args = {'ss': (parsed.ss if parsed.ss is not None else False), 
        'plot_energy': (parsed.plot if parsed.plot is not None else False), 
        'ic': (parsed.ic if parsed.ic is not None else 1), 
        'vis': '2D', 
        'init': True}

# go through CLI
else:
    args = prompt(questions)

    if (args['init'] == True):
        args['ic'] = prompt(ic_question)['ic']
    else:
        args['nrand'] = int(prompt(rand_question)['nrand'])
        #print(args)

# run 2D or 3D simulator
if(args['vis']=='2D'):
    run_nbody2d(parsed, args)
elif(args['vis']=='3D'):
    run_nbody3d(parsed, args)