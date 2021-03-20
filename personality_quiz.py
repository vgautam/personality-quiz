from flask import Flask, session, redirect, url_for, request
from markupsafe import escape
import os
import random
import re

app = Flask(__name__)
app.secret_key = os.urandom(16)
PORT = 5000

qualities = ['disarming',
             'chaotic',
             'organized',
             'skeptical',
             'adventurous',
             'spontaneous',
             'genuine',
             'warm',
             'sarcastic',
             'feisty',
             'awkward',
             'charming',
             'physical',
             'intellectual',
             'sensible',
             'wise',
             'relaxed',
             'anxious',
             'fearless',
             'brave',
             'lavish',
             'weird',
             'conventional',
             'flamboyant',
             'modest',
             'confident',
             'alpha',
             'beta',
             'naughty',
             'honest',
             'playful',
             'serious',
             'careful',
             'conflict-averse',
             'fierce',
             'creative',
             'trusting',
             'suspicious',
             'mainstream',
             'cheerful',
             'somber',
             'melancholy',
             'loyal',
             'traitorous',
             'fast',
             'slow',
             'balanced',
             'stylish',
             'nurturing',
             'judgemental',
             'intimate',
             'distant',
             'scientific',
             'artistic',
             'mature',
             'rebellious',
             'law-abiding',
             'selfish',
             'generous',
             'forgiving',
             'gracious',
             'meek',
             'wild',
             'tame',
             'social',
             'reclusive',
             'superficial',
             'deep',
             'weary',
             'whimsical',
             'manipulative',
             'straightforward',
             'ambitious',
             'calculating',
             'lazy',
             'resilient',
             'thoughtful',
             'impulsive',
             'resourceful',
             'complacent',
             'committed',
             'angry',
             'sentimental',
             'enthusiastic',
             'stoic',
             'equanimous',
             'effusive',
             'aloof',
             'introverted',
             'competent',
             'kind',
             'good-humoured']
assert len(qualities) == len(set(qualities))

@app.route('/')
def index():
    return '''
        <button type="button"><a href="/start">Start Quiz!</a></button>
    '''

def get_form_input(index, quality):
    # Shocking: re turns out to be the fastest way to do this!
    # https://stackoverflow.com/a/1277047
    pattern = re.compile('\W+')
    q_scrubbed = pattern.sub('', quality)
    return f'''
        <br/>
        <label for="{q_scrubbed}">{index}. <output id="{q_scrubbed}_val">50</output>% {quality}</label>
        <br/>
        <input type="range" id="{q_scrubbed}" name="{quality}" min="0" max="100" value="50" step="5" onchange="{q_scrubbed}_val.value=value">
        <br/>
    '''


@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        for quality in qualities:
            session[quality] = request.form[quality]
        # TODO: redirect to results
        return redirect(url_for('index'))
    random.shuffle(qualities)
    form_inputs = '\n'.join([get_form_input(i+1, quality) for i, quality in enumerate(qualities)])
    return f'''
        <form method="post" autocomplete="off">
            {form_inputs}
            <p><input type=submit value=Submit>
        </form>
    '''

@app.route('/end')
def end():
    session.pop('first', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True)

# TODO: make results page w pretty graphs
# TODO: db to compare people
# TODO: decide how to identify people (KISS - GUIDs prob fine)
# TODO: figure out the session invalidation flow - make that more intuitive
