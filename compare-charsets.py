import argparse
import json


def load_base_charset(json_path):
    base_sets = set()
    with open(json_path) as f:
        obj = json.load(f)
        for val in obj.values():
            base_sets |= set(val)
    return base_sets


def update_charsets(sets, file_path):
    with open(file_path) as f:
        sets |= set(f.read())


def check_charsets(base_json_file, input_files):
    base_sets = load_base_charset(base_json_file)
    print("基準文字集合ファイルの文字セット数: ", len(base_sets))
    target_sets = set()

    for file in input_files:
        update_charsets(target_sets, file)

    print("引数で指定したファイルの文字セット数: ", len(target_sets))

    # check subset
    is_subset = target_sets in base_sets
    print("基準文字集合の文字セットは全ファイルの文字セットを含みますか?: ", is_subset)

    if not is_subset:
        # list differences
        diff = target_sets - base_sets
        print("記事文字集合に含まれない文字セットの数: ", len(diff))
        print()
        for idx, char in enumerate(diff, 1):
            print(idx, ":", char, "-", hex(ord(char)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="基準文字集合ファイル(JSON)の文字集合と引数のファイルの文字集合の差異をチェックする")
    parser.add_argument('-b', '--base-chars-json', metavar="BASE_CHARS_FILE",
                        required=True, help='基準となる文字集合を記載したJSONファイル')
    parser.add_argument('input_files', metavar='INPUT_FILE', nargs='+',
                        help='チェック対象のテキストファイル')
    args = parser.parse_args()
    # print(args)
    check_charsets(args.base_chars_json, args.input_files)
