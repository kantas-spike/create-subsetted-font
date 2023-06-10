import argparse
import json
import os
from fontTools.subset import Options, load_font, Subsetter, save_font


def create_subsetted_font(org_font_path, output_font_dir, charset_text):
    subset_options = Options(
        flavor="woff2",
        with_zopfli=True,
        layout_features=["*"],
        hinting=False,
        drop_tables=[],
        name_IDs=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    )
    font = load_font(org_font_path, subset_options)
    subsetter = Subsetter(subset_options)
    subsetter.populate(text=charset_text)
    subsetter.subset(font)

    base_name = os.path.basename(org_font_path)
    woff2_name = os.path.splitext(base_name)[0] + ".woff2"
    output_font_path = os.path.join(output_font_dir, woff2_name)
    print(f"create {output_font_path}...")
    save_font(font, output_font_path, subset_options)


def load_text_from_json(json_path):
    charset = set()
    with open(json_path) as f:
        obj = json.load(f)
        for val in obj.values():
            charset |= set(val)
        return "".join(charset)


if __name__ == "__main__":

    DEFAULT_OUTPUT_DIR = "./subsetted_fonts"
    parser = argparse.ArgumentParser(description="指定したフォントファイルのサブセットを作成する")
    parser.add_argument('-b', '--base-charset-json', required=True, metavar="BASE_JSON", help="基準となる文字セット")
    parser.add_argument('-o', '--output-dir', metavar="OUTPUT_DIR", default=DEFAULT_OUTPUT_DIR,
                        help=f"サブセット化したフォントの出力先ディレクトリ(デフォルト値: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument('fonts', metavar="FONT_FILE", nargs='+', help="フォントファイル")
    args = parser.parse_args()
    # print(args)
    if not os.path.isdir(args.output_dir):
        print(f"mkdir {args.output_dir}...")
        os.makedirs(args.output_dir)

    charset_text = load_text_from_json(args.base_charset_json)
    print("number of charsets: ", len(charset_text))

    for font_path in args.fonts:
        create_subsetted_font(font_path, args.output_dir, charset_text)
