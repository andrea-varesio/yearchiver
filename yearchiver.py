#!/bin/python3
#https://github.com/andrea-varesio/yearchiver

import sys
import argparse
import datetime
import os
import os.path
import shutil

import inquirer

def show_license():
    print('\n**************************************************')
    print('"yearchiver" - Automatically sort files into folders by year')
    print('Copyright (C) 2023 Andrea Varesio (https://www.andreavaresio.com/).')
    print('This program comes with ABSOLUTELY NO WARRANTY')
    print('This is free software, and you are welcome to redistribute it under certain conditions')
    print('Full license available at https://github.com/andrea-varesio/yearchiver')
    print('**************************************************\n\n')

def parse_arguments():
    show_license()
    parser = argparse.ArgumentParser()
    extensions = parser.add_mutually_exclusive_group()
    parser.add_argument('-i', '--input', type=str,
                        help='Specify input directory')
    parser.add_argument('-o', '--output', type=str,
                        help='Specify output directory')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Disable prompts and verbosity')
    extensions.add_argument('-a', '--all', action='store_true',
                            help='Archive all files, regardless of extension')
    extensions.add_argument('-m', '--media', action='store_true',
                            help='Archive files matching media extensions (default)')
    extensions.add_argument('-f', '--filter', type=str,
                            help='Only archive files matching this extension (ie .png)')
    extensions.add_argument('--advanced-filter', action='store_true',
                            help='Select file extensions to process through a prompt')
    parser.add_argument('--dry-run', action='store_true',
                        help='Display what files would be moved, without making any changes')
    return parser.parse_args()

def filter_media():
    filter_media_ext = [
        '.asf', '.avi', '.bmp', '.bpg', '.cdr', '.crw', '.dng', '.dpx', '.dsc',
        '.dv', '.flv', '.gif', '.heic', '.icns', '.ico', '.jpg', '.jpeg',
        '.m2ts', '.mkv', '.mov', '.mp3', '.mp4', '.mpg', '.mpeg', '.mpo',
        '.mrw', '.oci', '.orf', '.pct', '.pcx', '.png', '.psb', '.psd','.psp',
        '.r3d', '.raf', '.raw', '.rdc', '.riff', '.wav', '.sit', '.skd',
        '.skp','.spe', '.tib', '.rif', '.wdp', '.xcf', '.xv'
    ]
    return filter_media_ext

def filter_inquirer():
    filter_inquirer_param = [inquirer.Checkbox(
        'filter',
        message = '[space] to select, [enter] to confirm',
        choices = filter_media(),
        default = filter_media()
    )]
    return list(inquirer.prompt(
        filter_inquirer_param,
        theme=inquirer.themes.GreenPassion()
    ).values())[0]

def get_year(subdir, file, output_dir):
    created_timestamp = datetime.datetime.fromtimestamp(min([
        os.stat(os.path.join(subdir, file)).st_ctime,
        os.stat(os.path.join(subdir, file)).st_mtime
    ]))
    created_year = created_timestamp.strftime('%Y')
    output_dir_year = os.path.join(output_dir, str(created_year))
    return output_dir_year

def loop(args, subdir, file, output_dir_year):
    if args.dry_run and not os.path.isfile(os.path.join(output_dir_year, file)):
        print(f'{os.path.join(subdir, file)} > {output_dir_year}')
    elif not args.dry_run:
        archive(subdir, file, output_dir_year)

def archive(subdir, file, output_dir_year):
    if not os.path.isdir(output_dir_year):
        os.mkdir(output_dir_year)
    if not os.path.isfile(os.path.join(output_dir_year, file)):
        shutil.move(os.path.join(subdir, file), output_dir_year)

def process_arguments():
    args = parse_arguments()

    if args.input and os.path.isdir(args.input):
        input_dir = args.input
    elif args.input:
        print(f'{args.input} is not a valid path')
        sys.exit(1)
    elif not args.input:
        input_dir = os.path.dirname(__file__)

    if args.output and os.path.isdir(args.output):
        output_dir = args.output
    elif args.output:
        print(f'{args.output} is not a valid path')
        sys.exit(1)
    elif not args.output:
        output_dir = os.path.dirname(__file__)

    if args.filter and args.filter.startswith('.'):
        ext_filter = [args.filter]
    elif args.filter:
        ext_filter = [f'.{args.filter}']
    elif args.advanced_filter:
        ext_filter = filter_inquirer()
    else:
        ext_filter = filter_media()

    if not args.quiet and not args.input and not args.output and not args.dry_run:
        print('Process files in current working directory?')
        print(os.path.dirname(__file__))
        if input('Proceed (P) or abort (A)? ').lower() != 'p':
            print('Okay, exiting...')
            sys.exit(0)

    return args, input_dir, output_dir, ext_filter

def main():
    args, input_dir, output_dir, ext_filter = process_arguments()
    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            output_dir_year = get_year(subdir, file, output_dir)
            if file != os.path.basename(__file__) and args.all:
                loop(args, subdir, file, output_dir_year)
            elif (
                file != os.path.basename(__file__) and
                os.path.splitext(file)[1].lower() in ext_filter
            ):
                loop(args, subdir, file, output_dir_year)

if __name__ == "__main__":
    main()
