import pykakasi

# 漢字仮名混じり文をローマ字に変換するスクリプト

def convert_to_romaji(text):
    kakasi = pykakasi.kakasi()
    kakasi.setMode("H", "a")  # Hiragana to ascii, default: no conversion
    kakasi.setMode("K", "a")  # Katakana to ascii, default: no conversion
    kakasi.setMode("J", "a")  # Japanese to ascii, default: no conversion
    kakasi.setMode("r", "Hepburn")  # default: use Hepburn Roman table
    kakasi.setMode("s", True)  # add space, default: no separator
    conv = kakasi.getConverter()
    result = conv.do(text)
    return result

if __name__ == "__main__":
    text = input()
    romaji = convert_to_romaji(text)
    print(romaji)

