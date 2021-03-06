import os
import re

import sqlite3

import math

from matplotlib import ticker
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

data_path = "../data/local_lamda_api_data/ecoviz_bench_s3.db"

FETCH_SUMMARY = "SELECT time_fetch_all from %s where _rowid_>=? and _rowid_<?;"

FETCH_STEPS = "SELECT num_entries FROM CLIENT_STORE_GET GROUP BY num_entries"
TABLENAME_DROPLET = "ECOVIZ_S3_FETCH_DROPLET_%d"
TABLENAME_BASELINE = "ECOVIZ_S3_FETCH_BASELINE_%d"

def fetch_data_from_db(db_path, table_name, from_row, to_row):
    query = FETCH_SUMMARY % table_name
    with sqlite3.connect(db_path) as conn:
        return np.asarray(conn.execute(query, (from_row, to_row)).fetchall())


def fetch_steps(db_path):
    with sqlite3.connect(db_path) as conn:
        return [x for [x] in conn.execute(FETCH_STEPS).fetchall()]


def process_data(data):
    return np.average(data), np.std(data)


def entries_to_day(entries):
    return entries / 86400


def create_list(max):
    return map(lambda a: a * 86400,[2**x for x in range(max)])

granularities = [21600, 43200, 86400, 604800]
gran_to_str = {
    #3600: "1h",
    21600: "6h",
    43200: "12h",
    86400: "1d",
    604800: "1w"
}


def plot_dht_s3_get_tp(local_tablename):
    result_data = []

    for granularity in granularities:
        table = local_tablename % granularity
        from_id = 1
        to_id = 101
        temp_list = []
        for entry in create_list(8):
            data = fetch_data_from_db(data_path, table, from_id, to_id)
            print data.shape
            data_avg, data_err = process_data(data)
            temp_list.append([entry, data_avg, data_err])
            from_id += 100
            to_id += 100
        result_data.append((granularity, np.asarray(temp_list)))
    result_data = sorted(result_data, key=lambda tup: tup[0])


    # ---------------------------- GLOBAL VARIABLES --------------------------------#
    # figure settings
    fig_width_pt = 300.0  # Get this from LaTeX using \showthe
    inches_per_pt = 1.0 / 72.27 * 2  # Convert pt to inches
    golden_mean = ((math.sqrt(5) - 1.0) / 2.0) * .8  # Aesthetic ratio
    fig_width = fig_width_pt * inches_per_pt  # width in inches
    fig_height = (fig_width * golden_mean)  # height in inches
    fig_size = [fig_width, fig_height / 1.5] #1.22

    params = {'backend': 'ps',
        'axes.labelsize': 20,
        'legend.fontsize': 18,
        'xtick.labelsize': 18,
        'ytick.labelsize': 18,
        'font.size': 18,
        'figure.figsize': fig_size,
        'font.family': 'times new roman'}

    #fig_size = [fig_width, fig_height / 1.2]

    plt.rcParams.update(params)
    plt.axes([0.12, 0.32, 0.85, 0.63], frameon=True)
    plt.rc('pdf', fonttype=42)  # IMPORTANT to get rid of Type 3

    # plot_latency fixed
    if local_tablename == TABLENAME_BASELINE:
        pdf_pages = PdfPages("../plots/paper_plot_ecoviz_s3_baseline_daily.pdf")
    else:
        pdf_pages = PdfPages("../plots/paper_plot_ecoviz_s3_daily.pdf")
    fig, ax = plt.subplots()

    colors = ['0.1', '0.4', '0.6',  '0.85']
    linestyles = ['-', '-', '-', '-', '-']

    ax.set_yscale('log')
    ax.set_xscale('log', basex=2)
    for idx, (granularity, data) in enumerate(result_data):
        x_values = np.asarray(map(entries_to_day, data[:, 0].tolist()))
        ax.plot(x_values, data[:, 1], '-o', label="%s chunks" % gran_to_str[granularity], color=colors[idx], linestyle=linestyles[idx])

    ax.grid(True, linestyle=':', color='0.8', zorder=0)
    ax.get_yaxis().set_major_formatter(ticker.FormatStrFormatter("%d"))
    ax.get_xaxis().set_major_formatter(ticker.FormatStrFormatter("%d"))
    plt.xlabel('Number of Days')
    plt.ylabel('Time [ms]')
    plt.ylim(0,10000)
    #plt.grid(True, linestyle=':', color='0.8', zorder=0, axis='y')
    ax.yaxis.set_ticks([100,1000,10000])#np.arange(0, 201, 20.0))


    #bbox_to_anchor=(0., 1.00, 1., .102)
    plt.legend(loc=2, ncol=2, columnspacing=1)

    F = plt.gcf()
    F.set_size_inches(fig_size)
    pdf_pages.savefig(F, bbox_inches='tight')
    plt.clf()
    pdf_pages.close()


if __name__ == "__main__":
    plot_dht_s3_get_tp(TABLENAME_DROPLET)
    plot_dht_s3_get_tp(TABLENAME_BASELINE)