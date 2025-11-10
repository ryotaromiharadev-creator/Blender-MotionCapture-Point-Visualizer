import csv

def read_motion_csv_in_groups(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # === "Trajectories" の開始位置を探す ===
    traj_start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("Trajectories"):
            traj_start = i
            break

    if traj_start is None:
        raise ValueError("Trajectories セクションが見つかりません。")

    # === 各行の位置 ===
    marker_line = traj_start + 2  # mihara:LFHD,... の行
    header_line = traj_start + 3  # Frame,Sub Frame,X,Y,Z,... の行
    data_start  = traj_start + 5  # データ本体開始

    # === ヘッダの構築 ===
    header1 = [h.strip() for h in lines[marker_line].strip().split(',')]
    header2 = [h.strip() for h in lines[header_line].strip().split(',')]

    columns = []
    prev_label = ""

    for h1, h2 in zip(header1, header2):
        if "_X" in h1 or "Frame" in h1 or "Sub Frame" in h1:
            prev_label = h1
        elif h1 == "" and h2 in ["Y", "Z"]:
            h1 = prev_label
        else:
            prev_label = h1

        if h1 and h2:
            columns.append(f"{h1}_{h2}")
        elif h2:
            columns.append(h2)
        else:
            columns.append(h1)

    # === データ部分をCSVリーダで読み込み ===
    data = []
    with open(path, "r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i < data_start:
                continue
            if not any(row):
                continue  # 空行スキップ
            data.append(row[:len(columns)])  # 列数合わせ

    if not data:
        raise ValueError("データが存在しません。")

    # === Frame, Sub Frame を除くデータ処理 ===
    Label = columns[2:]  # 最初の2列を除くラベル
    grouped_data = []

    # 数値データのみ抽出・変換
    numeric_data = []
    for row in data:
        row = row[2:]  # Frame, Sub Frame を除外
        numeric_data.append([float(x) if x.strip() != "" else 0.0 for x in row])

    # === 3列ずつに分割 ===
    num_cols = len(numeric_data[0])
    for i in range(0, num_cols, 3):
        group = [row[i:i+3] for row in numeric_data]
        grouped_data.append(group)

    return Label, grouped_data
