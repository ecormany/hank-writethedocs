from jsonlines import open as jsonl_open
from glob import glob
from json import load
from sys import argv
from openai import Model

def model():
    with open('version.txt', 'r') as f:
        version = f.readlines()[0].replace('\n', '')
    version = f'hank-v{version}'
    response = Model.list()
    for m in response['data']:
        if version not in m['id']:
            continue
        print(m['id'])

def transform():
    data_files = glob('data/*.json')
    jsonl = []
    for data_file in data_files:
        with open(data_file, 'r') as f:
            data = load(f)
        for pair in data:
            prompt = pair[0]
            completion = pair[1]
            jsonl.append({'prompt': prompt, 'completion': completion})
        with jsonl_open('training.jsonl', 'w') as writer:
            writer.write_all(jsonl)
    # output = []
    # for item in data:
    #     original = item['original']
    #     edited = item['edited']
    #     prompt = 'FIXME: {}@STOP!!'.format(original)
    #     completion = ' {}'.format(edited)
    #     output.append({'prompt': prompt, 'completion': completion})
    #     with jsonlines.open('training.jsonl', 'w') as writer:
    #         writer.write_all(output)

if __name__ == '__main__':
    if argv[1] == 'model':
        model()
    if argv[1] == 'transform':
        transform()
    # main()
