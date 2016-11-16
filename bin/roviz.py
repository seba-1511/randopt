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
  <title>{self._experiment_name} Visualization</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.27.8/css/theme.default.min.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.27.8/css/theme.dark.min.css">
</head>
<body>

<div class="container">
  <h2 class="text-center">{self._experiment_name}</h2>
  <table id="dataTable" class="table table-hover table-striped">
    <thead>
        <tr>'''

viz_footer = '''
    </tbody>
  </table>
</div>

</body>
</html>

<script>
    $(document).ready(function() {
            $("#dataTable").tablesorter();
        });
</script>
'''

class Visualizer:
    def __init__(self, experiment_name, sort_style = 'min'):
        self._experiment_name = experiment_name
        self._sort_style = sort_style
        self.counter = 1
        self.exp_metadata = ['__filename__']

    def write_row(self, res):
        self._output_writer.write('<tr>')
        self._output_writer.write('<td>' + str(self.counter) + '</td>')
        self._output_writer.write('<td>' + str(res['result']) + '</td>')
        specials = ['result'] + self.exp_metadata
        for key in res.keys():
            if key not in specials:
                text = str(res[key])
                if len(text) > 20:
                    text = text[:47] + '...'
                self._output_writer.write('<td>' + text + '</td>')
        self._output_writer.write('<td><a target="_blank" href="file://' + res['__filename__'] + '" class="btn btn-primary btn-xs">Download</a></td>')
        self._output_writer.write('</tr>')
        self.counter += 1

    def write_header(self, res):
        self._output_writer.write("<th>#</th>")
        self._output_writer.write("<th>Result</th>")
        specials = ['result'] + self.exp_metadata
        for key in res.keys():
            if key not in specials:
                self._output_writer.write('<th>' + key.title() + '</th>')
        self._output_writer.write('</tr></thead><tbody>')

    def write_data(self, data, output_path):
        self._output_writer = open(output_path, "w")
        self._output_writer.write(viz_header.format(**locals()))

        if(len(data) > 0):
            self.write_header(data[0])
            for datum in data:
                self.write_row(datum)

        self._output_writer.write(viz_footer)
        self._output_writer.close()

    def create_visualization(self):
        cwd = os.getcwd()
        randopt_folder = os.path.join(cwd, 'randopt_results')
        if not os.path.exists(randopt_folder):
            os.mkdir(randopt_folder)
        experiment_path = os.path.join(randopt_folder, self._experiment_name)
        if not os.path.exists(experiment_path):
            print "Experiment \"%s\" does not exist" % self._experiment_name
            return

        #The folder exists, so load in the data
        data = []
        for fname in os.listdir(experiment_path):
            base, ext = os.path.splitext(fname)
            if 'json' in ext:
                fpath = os.path.join(experiment_path, fname)
                with open(fpath, 'r') as f:
                    res = json.load(f)
                    res['__filename__'] = fpath
                    data.append(res)

        #sort the data
        #only reverse it if the sort style is max
        data = sorted(data, key=lambda k: float(k['result']), reverse = self._sort_style == 'max')
        viz_path = os.path.join(experiment_path, 'viz.html')
        self.write_data(data, viz_path)
        webbrowser.open("file:///" + os.path.abspath(viz_path))


def main():
    parser = argparse.ArgumentParser(description='Visualize the results of randopt')
    # parser.add_argument('expname', metavar='name', type=str,
                        # help='the name of the experiment to visualize')
    parser.add_argument('--expname', '-e', dest='expname', metavar='e', type=str, required=True,
                        help='the name of the experiment to visualize')
    parser.add_argument('--sort', '-s', dest='sort', type=str, choices=['min', 'max'],
                        default='min', help='sort style')

    args = parser.parse_args()
    viz = Visualizer(args.expname, args.sort)
    viz.create_visualization()

main()
