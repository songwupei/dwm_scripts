from pathlib import Path

csv_paths = Path("./中国兵器工业集团有限公司-20230430_/").rglob("*.csv")

for csv_path in csv_paths:
    rename = f"006_中国兵器工业集团有限公司_{csv_path.stem}_20230430{csv_path.suffix}"
    csv_path.rename(rename)
