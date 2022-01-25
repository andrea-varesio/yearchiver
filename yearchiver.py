#!/bin/python3
#https://github.com/andrea-varesio/yearchiver

from argparse import ArgumentParser
from datetime import date, datetime
from inquirer import Checkbox, List, prompt
from inquirer.themes import GreenPassion
from os import listdir, mkdir, stat, walk
from os.path import basename, dirname, isdir, isfile, join, splitext
from shutil import move
from sys import exit

def license():
    print('\n**************************************************')
    print('"yearchiver" - Automatically sort files into folders by year')
    print('Copyright (C) 2022 Andrea Varesio (https://www.andreavaresio.com/).')
    print('This program comes with ABSOLUTELY NO WARRANTY')
    print('This is free software, and you are welcome to redistribute it under certain conditions')
    print('Full license available at https://github.com/andrea-varesio/yearchiver')
    print('**************************************************\n\n')

def parser():
    parser = ArgumentParser(description='Copyright (C) 2022 Andrea Varesio <https://www.andreavaresio.com>')
    extensions = parser.add_mutually_exclusive_group()
    parser.add_argument('-i', '--input', help='Specify input directory', type=str)
    parser.add_argument('-o', '--output', help='Specify output directory', type=str)
    parser.add_argument('-q', '--quiet', help='Disable prompts and verbosity', action='store_true')
    extensions.add_argument('-a', '--all', help='Archive all files, regardless of extension', action='store_true')
    extensions.add_argument('-m', '--media', help='Archive files matching media extensions (default)', action='store_true')
    extensions.add_argument('-f', '--filter', help='Only archive files matching this extension (ie .png)', type=str)
    extensions.add_argument('--advanced-filter', help='Select file extensions to process through a prompt', action='store_true')
    parser.add_argument('--dry-run', help='Visually display what files would be moved, without making any changes', action='store_true')
    return parser.parse_args()

def filter_media():
    filter_media = ['.asf', '.avi', '.bmp', '.bpg', '.cdr', '.crw', '.dng', '.dpx', '.dsc', '.dv', '.flv', '.gif', '.heic', '.icns', '.ico', '.jpg', '.jpeg', '.m2ts', '.mkv', '.mov', '.mp3', '.mp4', '.mpg', '.mpeg', '.mrw', '.oci', '.orf', '.pct', '.pcx', '.png', '.psb', '.psd','.psp', '.r3d', '.raf', '.raw', '.rdc', '.riff', '.wav', '.sit', '.skd', '.skp', '.spe', '.tib', '.rif', '.wdp', '.xcf', '.xv']
    return filter_media

def filter_inquirer():
    filter_inquirer = [
        Checkbox('filter',
            message = 'Select [space] the file extensions you want to process, then confirm [enter]',
            choices = filter_media(),
            default = filter_media()
        ),
    ]
    return list(prompt(filter_inquirer, theme=GreenPassion()).values())[0]

def get_year():
    created_timestamp = datetime.fromtimestamp(min([stat(join(subdir, file)).st_ctime, stat(join(subdir, file)).st_mtime]))
    created_year = created_timestamp.strftime('%Y')
    output_dir_year = join(output_dir, str(created_year))
    return output_dir_year

def loop():
    if args.dry_run and not isfile(join(output_dir_year, file)):
        print(f'{join(subdir, file)} > {output_dir_year}')
    elif not args.dry_run:
        archive()

def archive():
    if not isdir(output_dir_year):
        mkdir(output_dir_year)
    if not isfile(join(output_dir_year, file)):
        move(join(subdir, file), output_dir_year)

args = parser()

if args.input and isdir(args.input):
    input_dir = args.input
elif args.input:
    print(f'{args.input} is not a valid path')
    exit(1)
elif not args.input:
    input_dir = dirname(__file__)

if args.output and isdir(args.output):
    output_dir = args.output
elif args.output:
    print(f'{args.output} is not a valid path')
    exit(1)
elif not args.output:
    output_dir = dirname(__file__)

if args.filter and args.filter.startswith('.'):
    filter = [args.filter]
elif args.filter:
    filter = [f'.{args.filter}']
elif args.advanced_filter:
    filter = filter_inquirer()
else:
    filter = filter_media()

if not args.quiet:
    license()

if not args.quiet and not args.input and not args.output and not args.dry_run:
    print('Process files in current working directory?')
    print(dirname(__file__))
    if input('Proceed (P) or abort (A)? ').lower() != 'p':
        print('Okay, exiting...')
        exit(0)

for subdir, dirs, files in walk(input_dir):
    for file in files:
        output_dir_year = get_year()
        if file != basename(__file__) and args.all:
            loop()
        elif file != basename(__file__) and splitext(file)[1].lower() in filter:
            loop()
