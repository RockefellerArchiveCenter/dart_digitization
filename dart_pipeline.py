import argparse

from create_bags.digitization_pipeline import DigitizationPipeline


def main():
    parser = argparse.ArgumentParser(
        description="Uses DART to create bags of digitized content that will be sent to Zorya.")
    parser.add_argument(
        "root_dir",
        help="A directory containing subdirectories (named using ref ids) for archival objects.")
    parser.add_argument(
        "tmp_dir",
        help="A directory in which to create generated image derivatives and manifests.")
    parser.add_argument(
        '-l',
        '--list',
        nargs='+',
        help='List of rights IDs (integers). E.g.: -l 2 4',
        type=int,
        required=True)
    args = parser.parse_args()
    DigitizationPipeline(args.root_dir, args.tmp_dir).run()


if __name__ == "__main__":
    main()
