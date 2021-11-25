# coding: utf-8

import argparse
import json
import matplotlib.pyplot as plt
import os


def html2dict(html):
    d = {}
    with open(html, 'r', encoding='utf-8') as fp:
        for row in fp:
            if row.strip().startswith('const data = {'):
                data = row.strip().replace('const data = ', '')
                d = json.loads(data)
    return d


def barcode_rank_plot(data, outdir):
    for d in data:
        x = d["x"]
        y = d["y"]
        color = d["line"]["color"]
        name = d['name']
        text = d['text']
        if text == "Background" or "100% Cells" in text:
            plt.plot(x, y, color=color, label=name)
        else:
            plt.plot(x, y, color=color)
    plt.xscale("log")
    plt.yscale("log")
    # plt.style.use('seaborn')
    plt.title('Barcode Rank Plot', fontsize='large', fontweight='bold')
    plt.xlabel('Barcodes')
    plt.ylabel('UMI counts')
    plt.legend()

    fname = os.path.join(outdir, 'barcode_rank_plot.png')
    plt.savefig(fname, dpi=600, format='png', bbox_inches='tight')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--html', help='cellrange count web summary report')
    parser.add_argument('-o', '--outdir', help='out directory')
    args = parser.parse_args()
    html = args.html
    outdir = args.outdir
    d = html2dict(html)
    try:
        data = d["summary"]["summary_tab"]["cells"]["barcode_knee_plot"]["data"]
    except Exception as e:
        print('[ERROR] invalid data.')
        raise
    with plt.style.context('seaborn'):
        barcode_rank_plot(data, outdir)
