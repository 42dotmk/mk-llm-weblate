import os
import pandas as pd
import os
import polib

def main():
    files = [os.path.join("input_data", f) for f in os.listdir('input_data')]
    for file_path in files:
      df = pd.read_parquet(file_path)
      name = os.path.basename(file_path)[:-8]

      df.rename(columns={"text": "source", "translated_text": "target"}, inplace=True)
      df.drop(columns=["words", "translated_words", "diff_words"], inplace=True)

      i = 0

      source_po = polib.POFile()
      translated_po = polib.POFile()

      for row in df.iterrows():
        i += 1
        entry = polib.POEntry(
            msgid="{}_{}".format(name, i),
            msgstr=polib.unescape(row[1]["source"]),
        )
        translated = polib.POEntry(
            msgid="{}_{}".format(name, i),
            msgstr=row[1]["target"]
        )
        source_po.append(entry)
        translated_po.append(translated)
      source_po.save("po/{}_en.po".format(name))
      translated_po.save("po/{}_mk.po".format(name))


if __name__ == "__main__":
    main()
