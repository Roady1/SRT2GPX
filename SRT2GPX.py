#!/usr/bin/env python

import os
import argparse
from xml.dom import minidom

__author__ = "Emre Yildiz"
__license__ = "GPL"
__tool_ = "SRT2GPX"
__version__ = "1.0.0"


def feet2meter(feetalt):
    stringmeteralt = []
    for i in feetalt:
        stringmeteralt.append(str(round(float(i) * 0.3048, 6)))

    return stringmeteralt


def get_lat(data):
    start = None
    end = None
    a = []

    for line in data:
        if line.find('latitude') > 0:
            start = line.find('latitude') + 11
            end = start + 9
            lat = line[start:end]
            a.append(lat)
    return a


def get_lon(data):
    start = None
    end = None
    a = []

    for line in data:
        if line.find('longtitude') > 0:
            start = line.find('longtitude') + 13
            end = start + 8
            long = line[start:end]
            a.append(long)
    return a


def get_altitude_feet(data):
    start = None
    end = None
    a = []

    for line in data:
        if line.find('altitude') > 0:
            start = line.find('altitude') + 10
            end = start + 10
            long = line[start:end]
            a.append(long)
    return a


def get_altitude_meter(data):
    start = None
    end = None
    a = []

    for line in data:
        if line.find('altitude') > 0:
            start = line.find('altitude') + 10
            end = start + 10
            long = line[start:end]
            a.append(long)
    return feet2meter(a)


def read_str(path):
    with open(path, 'r') as file:
        data = file.read().splitlines()
        return data


def write_gpx(path, gpx):
    xml = gpx.toprettyxml(indent="\t")
    with open(path, "w") as f:
        f.write(xml)


def define_gpx_structure(lat, long, alt):
    xml = minidom.Document()

    ## Create Elements
    gpx = xml.createElement('gpx')
    trk = xml.createElement('trk')
    trkseg = xml.createElement('trkseg')

    ## Add Attributes to gpxtag
    gpx.setAttribute('version', '1.0')
    gpx.setAttribute('creator', __tool_)

    ## Add Childs to Each Other
    xml.appendChild(gpx)
    gpx.appendChild(trk)
    trk.appendChild(trkseg)

    ## Add trkpts
    count = 0
    for i in lat:
        ## Create trkpttag and eletag for each entry
        trkpt = xml.createElement('trkpt')
        ele = xml.createElement('ele')
        time = xml.createElement('time')

        ## Add Attributes to Elements
        trkpt.setAttribute('lat', i)
        trkpt.setAttribute('lon', long[count])

        ## Add TextNode with altvalue to eletag
        ele.appendChild(xml.createTextNode(alt[count]))

        ## Add Child Ele to trkpttag
        trkpt.appendChild(ele)
        trkpt.appendChild(time)

        ## Add trktag to trksegtag
        trkseg.appendChild(trkpt)

        count += 1

    return xml


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument('-str', type=is_str_file, help='SOURCE .STR FILE')
    parser.add_argument('-dst', type=is_path, help='DESTINATION PATH OF CONVERTED .GPX OUTPUT')

    return parser.parse_args()


def is_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")


def is_str_file(file):
    if os.path.isfile(file):
        return file
    else:
        raise argparse.ArgumentTypeError(f"{file} is not a valid file")


def main():
    ## Parse Arguments
    parsed_args = parse_arguments()
    str = parsed_args.str
    dst = parsed_args.dst

    if not str or not dst:
        print(__tool_+" "+__version__+"\n"
              "Error: Arguments Missing!\n"
              "Call with \'--help\' to print a list of valid arguments:")
        exit()

    ## write SRT File to data
    data = read_str(str)

    ## Get Lists with values from data
    lat = get_lat(data)
    long = get_lon(data)
    feetalt = get_altitude_feet(data)
    meteralt = get_altitude_meter(data)

    ## Make XML with tags and values
    xml = define_gpx_structure(lat, long, meteralt)

    ## Write XML to file
    write_gpx(dst + "output.gpx", xml)


if __name__ == '__main__':
    main()
