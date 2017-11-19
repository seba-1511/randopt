#!/usr/bin/env python3

import webbrowser
import os
import sys
import json


if __name__ == '__main__':
    roviz_path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print('The new usage of roviz is: roviz.py path/to/experiment')
        sys.exit(-1)
    exp_path = sys.argv[1]
    path = os.path.abspath('.')
    path = os.path.join(path, exp_path)
    results = []
    for fname in os.listdir(path):
        if fname.endswith('.json'):
            fpath = os.path.join(path, fname)
            with open(fpath, 'r') as f:
                results.append(json.load(f))
    results = sorted(results, key=lambda x: float(x['result']))
    content = 'var DATA = ' + json.dumps(results) + ';'
    header_path = os.path.join(roviz_path, 'header.html')
    with open(header_path, 'r') as f:
        header = f.read()
    footer_path = os.path.join(roviz_path, 'footer.html')
    with open(footer_path, 'r') as f:
        footer = f.read()
    content = header + content + footer
    out_path = os.path.join(exp_path, 'viz.html')
    with open(out_path, 'w') as f:
        f.write(content)
    webbrowser.open("file:///" + os.path.abspath(out_path))
