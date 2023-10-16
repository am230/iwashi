import argparse

from .helper import print_result
from .iwashi import visit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-url", type=str, required=False)
    args = parser.parse_args()
    result = visit(args.url)
    assert result
    print("\n" * 4)
    print_result(result)


if __name__ == "__main__":
    main()
