from page_loader import download

import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Download web-page')
    parser.add_argument(
        '-o', '--output',
        default=f'{os.getcwd()}',
        help='set path to download (default: current directory)',
        type=str
    )
    parser.add_argument('page_url', type=str)

    args = parser.parse_args()
    print(download(args.output, args.page_url))


if __name__ == '__main__':
    main()
