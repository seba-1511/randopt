#!/usr/bin/env pybon

import webbrowser
import os
import sys
import json as json
import argparse

viz_header = '''<!DOCTYPE html>
<html lang="en">
<head>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.27.8/js/jquery.tablesorter.min.js"></script>
  <script type="text/javascript" src="https://cdn.plot.ly/plotly-latest.min.js"></script>
  <title>{self._experiment_name} Visualization</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.27.8/css/theme.default.min.css">
</head>
<body>

<div class="container">
  <h2 class="text-center">{self._experiment_name}</h2>
  <div id="plotter-container" class="text-center" style="display:none;">
    <h3>Parameter Plotting</h3>
    <div id="plotter" style="margin:auto;height:450px;"></div>
  </div>
  <hr />
  <div style="overflow-x: auto;">
  <table id="dataTable" class="table table-hover table-striped">
    <thead>
        <tr>'''

viz_footer = '''
    </tbody>
  </table>
  </div>
</div>

</body>
</html>

<script>
    $(document).ready(function() {
            $("#dataTable").tablesorter();
        });
'''

viz_end = '''

    var ARRAY_PLOT = 1;

    function plotArray(name, idx, traceNb) {
        var div = document.getElementById('plotter'), i,
            x = [],
            y = expData[name][idx];
        for (i=0; i < y.length; i++) {
            debugger;
            x.push(i);
        }
        var data = [{
            x: x,
            y: y,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Result #' + traceNb,
        }];
        var layout = {
            margin: {t: 0},
            xaxis: {title: 'index in array'},
            yaxis: {title: name}
        };
        document.getElementById('plotter-container').style.display = '';
        if (ARRAY_PLOT) {
            Plotly.plot(div, data, layout);
        }
        else {
            Plotly.newPlot(div, data, layout);
            ARRAY_PLOT = 1;
        }
    };

    function plotError(name) {
        var div = document.getElementById('plotter'),
            x = expData[name],
            y = expData['result'];
        var data = [{
            x: x,
            y: y,
            type: 'scatter',
            mode: 'markers',
        }];
        var layout = {
            margin: {t: 0},
            xaxis: {title: name},
            yaxis: {title: 'Result'}
        };
        document.getElementById('plotter-container').style.display = '';
        Plotly.newPlot(div, data, layout);
        ARRAY_PLOT = 0;
    };
</script>
'''


def is_array(value):
    return isinstance(value, list)


class Visualizer:
    def __init__(self, name=None, path=None, sort_style='min'):
        self.name = None
        self.path = None
        self._sort_style = sort_style
        self.counter = 1
        self.exp_metadata = ['__filename__']
        self.exp_data = {'result': []}
        if name is not None:
            self.name = name
            self._experiment_name = name
        elif path is not None:
            self.path = path
            self._experiment_name = os.path.basename(path)

    def write_row(self, res):
        self._output_writer.write('<tr>')
        self._output_writer.write('<td>' + str(self.counter) + '</td>')
        self._output_writer.write('<td>' + str(res['result']) + '</td>')
        self.exp_data['result'].append(res['result'])
        specials = ['result'] + self.exp_metadata
        for key in res.keys():
            if key not in specials:
                text = str(res[key])
                if len(text) > 20:
                    text = text[:47] + '...'
                if not is_array(res[key]):
                    self.exp_data[key].append(res[key])
                    self._output_writer.write('<td><a style="cursor:pointer;text-decoration:none;color:black;" onclick="plotError(\'' + key + '\');">' + text + '</a></td>')
                else:
                    self.exp_data[key].append(res[key])
                    self._output_writer.write('<td><a style="cursor:pointer;text-decoration:none;color:black;" onclick="plotArray(\'' + key + '\', ' + str(len(self.exp_data[key]) - 1) + ', ' + str(self.counter) + ');">' + text + '</a></td>')
        self._output_writer.write('<td><a target="_blank" href="file://' + res['__filename__'] + '" class="btn btn-primary btn-xs">Download</a></td>')
        self._output_writer.write('</tr>\n')
        self.counter += 1

    def write_header(self, res):
        self._output_writer.write("<th>#</th>")
        self._output_writer.write("<th>Result</th>")
        specials = ['result'] + self.exp_metadata
        for key in res.keys():
            if key not in specials:
                self._output_writer.write('<th>' + key.title() + '</th>')
                self.exp_data[key] = []
        self._output_writer.write('</tr></thead><tbody>')

    def write_js_data(self):
        for key in self.exp_data:
            self._output_writer.write('var expData = ' + json.dumps(self.exp_data) + ';')


    def write_data(self, data, output_path):
        self._output_writer = open(output_path, "w")
        self._output_writer.write(viz_header.format(**locals()))
        if(len(data) > 0):
            self.write_header(data[0])
            for datum in data:
                self.write_row(datum)

        self._output_writer.write(viz_footer)
        self.write_js_data()
        self._output_writer.write(viz_end)
        self._output_writer.close()

    def create_visualization(self):
        cwd = os.getcwd()
        randopt_folder = os.path.join(cwd, 'randopt_results')
        if not os.path.exists(randopt_folder):
            os.mkdir(randopt_folder)
        if self.path is not None:
            experiment_path = self.path
        else:
            experiment_path = os.path.join(randopt_folder, self._experiment_name)
            if not os.path.exists(experiment_path):
                print("Experiment \"%s\" does not exist" % self._experiment_name)
                return

        #The folder exists, so load in the data
        data = []
        for fname in os.listdir(experiment_path):
            base, ext = os.path.splitext(fname)
            if 'json' in ext:
                fpath = os.path.join(experiment_path, fname)
                with open(fpath, 'r') as f:
                    try:
                        res = json.load(f)
                        res['__filename__'] = fpath
                        data.append(res)
                    except ValueError:
                        print('Issue when reading file: ', f, ' - ignored.')

        #sort the data
        #only reverse it if the sort style is max
        data = sorted(data, key=lambda k: k['result'], reverse = self._sort_style == 'max')
        viz_path = os.path.join(experiment_path, 'viz.html')
        self.write_data(data, viz_path)
        webbrowser.open("file:///" + os.path.abspath(viz_path))


def main():
    parser = argparse.ArgumentParser(description='Visualize the results of randopt')
    # parser.add_argument('expname', metavar='name', type=str,
                        # help='the name of the experiment to visualize')
    parser.add_argument('--expname', '-e', dest='expname', metavar='e', type=str, required=False,
                        help='the name of the experiment to visualize')
    parser.add_argument('--path', '-p', dest='exp_path', metavar='p', type=str, required=False,
                        help='the path to the experiment to visualize')
    parser.add_argument('--sort', '-s', dest='sort', type=str, choices=['min', 'max'],
                        default='min', help='sort style')

    args = parser.parse_args()
    if args.expname:
        viz = Visualizer(name=args.expname, sort_style=args.sort)
        viz.create_visualization()

    if args.exp_path:
        viz = Visualizer(path=args.exp_path, sort_style=args.sort)
        viz.create_visualization()

main()
