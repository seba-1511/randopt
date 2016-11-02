import webbrowser
import os
import sys
import json as json
import argparse

vizHeader = '''<!DOCTYPE html>
<html lang="en">
<head>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.27.8/js/jquery.tablesorter.min.js"></script>
  <title>{self._experimentName} Visualization</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>
<body>

<div class="container">
  <h2>Experiment "{self._experimentName}" Data Visualization</h2>
  <table id="dataTable" class="table table-hover table-striped">
    <thead>
        <tr>'''

vizFooter = '''
    </tbody>
  </table>
</div>

</body>
</html>

<script>
    $(document).ready(function()
        {{
            $("#dataTable").tablesorter();
        }}
    );
</script>
'''

class Visualizer:
    def __init__(self, experimentName, sortStyle = 'min'):
        self._experimentName = experimentName
        self._sortStyle = sortStyle

    def WriteRow(self, res):
        self._outputWriter.write('<tr>')
        self._outputWriter.write('<td>' + str(res['result']) + '</td>')
        for key in res.keys():
            if key != 'result':
                self._outputWriter.write('<td>' + str(res[key]) + '</td>')
        self._outputWriter.write('</tr>')

    def WriteHeader(self, res):
        self._outputWriter.write("<th>Result</th>")
        for key in res.keys():
            if key != 'result':
                self._outputWriter.write('<th>' + key.title() + '</th>')
        self._outputWriter.write('</tr></thead><tbody>')

    def WriteData(self, data, outputPath):
        self._outputWriter = open(outputPath, "w")
        self._outputWriter.write(vizHeader.format(**locals()))

        if(len(data) > 0):
            self.WriteHeader(data[0])
            for datum in data:
                self.WriteRow(datum)

        self._outputWriter.write(vizFooter)
        self._outputWriter.close()

    def CreateVisualization(self):
        cwd = os.getcwd()
        randopt_folder = os.path.join(cwd, 'randopt_results')
        if not os.path.exists(randopt_folder):
            os.mkdir(randopt_folder)
        experiment_path = os.path.join(randopt_folder, self._experimentName)
        if not os.path.exists(experiment_path):
            print "Experiment \"%s\" does not exist" % self._experimentName
            return

        #The folder exists, so load in the data
        data = []
        for fname in os.listdir(experiment_path):
            base, ext = os.path.splitext(fname)
            if 'json' in ext:
                fpath = os.path.join(experiment_path, fname)
                with open(fpath, 'r') as f:
                    res = json.load(f)
                    data.append(res)

        #sort the data
        #only reverse it if the sort style is max
        data = sorted(data, key=lambda k: k['result'], reverse = self._sortStyle == 'max')
        vizPath = os.path.join(experiment_path, 'viz.html')
        self.WriteData(data, vizPath)
        webbrowser.open("file:///" + os.path.abspath(vizPath))


def main():
    parser = argparse.ArgumentParser(description='Visualize the results of RandOpt')
    parser.add_argument('--expname', '-e', dest='expname', metavar='e', type=str, required=True,
                        help='the name of the experiment to visualize')
    parser.add_argument('--sort', '-s', dest='sort', type=str, choices=['min', 'max'],
                        default='min', help='sort style')

    args = parser.parse_args()
    viz = Visualizer(args.expname, args.sort)
    viz.CreateVisualization()

main()
