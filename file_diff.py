import pandas as pd
from typing import Dict, List, Union
import os
from datetime import datetime


def two_file_diff(
    file1_path: str,
    file2_path: Union[str, None] = None,
    key_column: str = None,
    sheet1: str = None,  # 可选：指定 sheet 名
    sheet2: str = None,
    output_report: bool = False,
    report_path: str = None,
    compare_mode: str = "file",  # 新增参数：比较模式，"file" 或 "sheet"
    file_path_for_sheet: str = None,  # 当比较模式为"sheet"时，指定文件路径
    file_type: str = "excel",  # 新增参数：文件类型，"excel"、"csv" 或 "txt"
    delimiter: str = ",",  # 新增参数：CSV/TXT文件的分隔符，默认为逗号
) -> Dict[str, List[str]]:
    """
    比较两个 Excel/CSV/TXT 文件或同一文件中的两个 Sheet 中基于关键列的共同列数据是否一致

    参数:
        file1_path: 第一个文件路径（通常是"全量数据"）
        file2_path: 第二个文件路径（待核对数据），当比较模式为"sheet"时可为None
        key_column: 用于匹配行的关键列名（如 '订单号'）
        sheet1: 第一个文件的 sheet 名（None 表示默认第一个 sheet，仅Excel文件有效）
        sheet2: 第二个文件的 sheet 名（None 表示默认第一个 sheet，仅Excel文件有效）
        output_report: 是否生成差异报告
        report_path: 报告保存路径（默认为自动生成的路径）
        compare_mode: 比较模式，"file"表示比较两个文件，"sheet"表示比较同一文件中的两个sheet
        file_path_for_sheet: 当比较模式为"sheet"时，指定包含两个sheet的文件路径
        file_type: 文件类型，"excel"表示Excel文件，"csv"表示CSV文件，"txt"表示TXT文件
        delimiter: CSV/TXT文件的分隔符，默认为逗号

    返回:
        字典，包含：
        - 'identical': 完全一致的行
        - 'mismatch': 值不一致的行及列
        - 'not_in_file1': 在 file2 但不在 file1 的行
        - 'not_in_file2': 在 file1 但不在 file2 的行
    """

    # 验证参数
    if compare_mode not in ["file", "sheet"]:
        raise ValueError("compare_mode 必须是 'file' 或 'sheet'")

    if compare_mode == "sheet" and not file_path_for_sheet:
        raise ValueError("当比较模式为 'sheet' 时，必须提供 file_path_for_sheet 参数")

    if file_type not in ["excel", "csv", "txt"]:
        raise ValueError("file_type 必须是 'excel'、'csv' 或 'txt'")

    if not key_column:
        raise ValueError("必须提供 key_column 参数")

    # 根据比较模式设置文件路径和sheet名称
    if compare_mode == "sheet":
        # Sheet比较模式：比较同一文件中的两个sheet（仅支持Excel文件）
        file1_path = file_path_for_sheet
        file2_path = file_path_for_sheet
        if not sheet1 or not sheet2:
            raise ValueError("当比较模式为 'sheet' 时，必须提供 sheet1 和 sheet2 参数")
        if file_type != "excel":
            raise ValueError("Sheet比较模式仅支持Excel文件")
        comparison_description = f"同一文件 '{os.path.basename(file1_path)}' 中的 Sheet '{sheet1}' 与 Sheet '{sheet2}'"
    else:
        # 文件比较模式：比较两个不同文件
        if not file2_path:
            raise ValueError("当比较模式为 'file' 时，必须提供 file2_path 参数")
        comparison_description = f"文件 '{os.path.basename(file1_path)}' 与 文件 '{os.path.basename(file2_path)}'"

    print(f"🔍 开始比较: {comparison_description}")
    print(f"📋 使用关键列: '{key_column}'")
    print(f"📄 文件类型: {file_type}")

    # 根据文件类型选择读取方法
    def read_file(file_path, sheet_name=None):
        try:
            if file_type == "excel":
                data = pd.read_excel(file_path, sheet_name=sheet_name)
                # 处理可能的字典返回值（当Excel有多个sheet且未指定sheet名时）
                if isinstance(data, dict):
                    # 如果是字典，取第一个sheet
                    first_sheet = list(data.keys())[0]
                    return data[first_sheet], first_sheet
                else:
                    return data, sheet_name or "默认sheet"
            elif file_type == "csv":
                return pd.read_csv(file_path, delimiter=delimiter), "CSV文件"
            elif file_type == "txt":
                return pd.read_csv(file_path, delimiter=delimiter), "TXT文件"
        except Exception as e:
            raise FileNotFoundError(f"无法读取文件 {file_path}, 错误: {e}")

    # 1. 读取两个文件
    df1, sheet1_display = read_file(file1_path, sheet1)
    print(f"✅ 已加载数据源1: {os.path.basename(file1_path)}, 类型: {sheet1_display}")

    df2, sheet2_display = read_file(file2_path, sheet2)
    print(f"✅ 已加载数据源2: {os.path.basename(file2_path)}, 类型: {sheet2_display}")

    # 2. 检查关键列是否存在
    if key_column not in df1.columns:
        raise ValueError(
            f"数据源1 中不存在关键列: {key_column}，可用列: {list(df1.columns)}"
        )
    if key_column not in df2.columns:
        raise ValueError(
            f"数据源2 中不存在关键列: {key_column}，可用列: {list(df2.columns)}"
        )

    # 3. 找出共同列
    common_columns = df1.columns.intersection(df2.columns).tolist()
    if not common_columns:
        raise ValueError("两个数据源没有共同列，无法比较")

    print(f"🔍 共同列: {common_columns}")

    # 4. 提取共同列数据
    df1_common = df1[common_columns].copy()
    df2_common = df2[common_columns].copy()

    # 5. 检查 key_column 是否有重复值
    if df1_common[key_column].duplicated().any():
        print(f"⚠️  Warning: 数据源1 的 '{key_column}' 存在重复值，将保留第一个")
        df1_common = df1_common.drop_duplicates(subset=[key_column], keep="first")
    if df2_common[key_column].duplicated().any():
        print(f"⚠️  Warning: 数据源2 的 '{key_column}' 存在重复值，将保留第一个")
        df2_common = df2_common.drop_duplicates(subset=[key_column], keep="first")

    # 6. 设置索引
    df1_indexed = df1_common.set_index(key_column)
    df2_indexed = df2_common.set_index(key_column)

    # 7. 找出差异行
    only_in_file2 = df2_indexed.index.difference(df1_indexed.index)
    only_in_file1 = df1_indexed.index.difference(df2_indexed.index)

    results = {
        "identical": [],
        "mismatch": [],
        "not_in_file1": list(only_in_file2),
        "not_in_file2": list(only_in_file1),
    }

    if only_in_file2.any():
        print(
            f"🟡 数据源2 有 {len(only_in_file2)} 行在 数据源1 中不存在: {list(only_in_file2)}"
        )

    if only_in_file1.any():
        print(
            f"🟡 数据源1 有 {len(only_in_file1)} 行在 数据源2 中不存在: {list(only_in_file1)}"
        )

    # 8. 取交集部分进行比较
    common_index = df1_indexed.index.intersection(df2_indexed.index)
    if common_index.empty:
        print("❌ 无共同行可用于比较")
        return results

    df1_compare = df1_indexed.loc[common_index]
    df2_compare = df2_indexed.loc[common_index]

    # 方法 1：尝试使用 compare()（pandas >= 1.1）
    try:
        diff = df2_compare.compare(df1_compare, align_axis=1)
        if diff.empty:
            print("✅ 所有匹配行在共同列上完全一致！")
            results["identical"] = list(common_index)
        else:
            print("❌ 发现不一致的数据：")
            print("\n详细差异：")
            for idx in diff.index:
                mismatch_cols = []
                for col in diff.columns.levels[0]:
                    val2 = diff.loc[idx, (col, "self")]  # self = df2
                    val1 = diff.loc[idx, (col, "other")]  # other = df1
                    if pd.notna(val2) or pd.notna(val1):
                        mismatch_cols.append(f"{col}: '{val2}' vs '{val1}'")
                if mismatch_cols:
                    msg = f"【{key_column}={idx}】 " + "; ".join(mismatch_cols)
                    results["mismatch"].append(msg)
                    print(f"  ❌ {msg}")

    except AttributeError:
        # 兼容老版本 pandas
        print("⚠️ 当前 pandas 版本不支持 .compare()，使用手动比较")
        mismatches = []
        identicals = []

        for idx in common_index:
            row1 = df1_compare.loc[idx]
            row2 = df2_compare.loc[idx]
            is_match = True
            mismatch_cols = []

            for col in common_columns:
                if col == key_column:
                    continue
                v1, v2 = row1[col], row2[col]
                if pd.isna(v1) and pd.isna(v2):
                    continue
                if v1 != v2:
                    is_match = False
                    mismatch_cols.append(f"{col}: '{v2}' vs '{v1}'")

            if is_match:
                identicals.append(idx)
            else:
                msg = f"【{key_column}={idx}】 " + "; ".join(mismatch_cols)
                mismatches.append(msg)
                print(f"  ❌ {msg}")

        if identicals:
            print(f"✅ {len(identicals)} 行完全一致")
            results["identical"] = identicals
        if mismatches:
            results["mismatch"] = mismatches

    # 9. 生成报告（可选）
    if output_report:
        # 生成默认报告路径
        if not report_path:
            if compare_mode == "sheet":
                base_name = (
                    os.path.basename(file1_path)
                    .replace(".xlsx", "")
                    .replace(".xls", "")
                )
                default_report_path = os.path.join(
                    os.path.dirname(file1_path),
                    f"{base_name}_{sheet1}_vs_{sheet2}_diff_report.csv",
                )
            else:
                file1_base = (
                    os.path.basename(file1_path)
                    .replace(".xlsx", "")
                    .replace(".xls", "")
                    .replace(".csv", "")
                    .replace(".txt", "")
                )
                file2_base = (
                    os.path.basename(file2_path)
                    .replace(".xlsx", "")
                    .replace(".xls", "")
                    .replace(".csv", "")
                    .replace(".txt", "")
                )
                default_report_path = os.path.join(
                    os.path.dirname(file1_path),
                    f"{file1_base}_vs_{file2_base}_diff_report.csv",
                )
            report_file = default_report_path
        else:
            report_file = report_path

        # 创建报告头部注释
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header_comments = [
            f"# Excel差异对比报告",
            f"# 生成时间: {timestamp}",
            f"# 比较对象: {comparison_description}",
            f"# 关键列: {key_column}",
            f"# 共同列: {', '.join(common_columns)}",
            f"# 数据源1: {os.path.basename(file1_path)} (类型: {sheet1_display})",
            f"# 数据源2: {os.path.basename(file2_path)} (类型: {sheet2_display})",
            f"# 统计信息:",
            f"# 完全一致的行数: {len(results['identical'])}",
            f"# 有差异的行数: {len(results['mismatch'])}",
            f"# 仅在数据源1中存在的行数: {len(results['not_in_file1'])}",
            f"# 仅在数据源2中存在的行数: {len(results['not_in_file2'])}",
            "",
        ]

        # 创建差异数据的DataFrame
        diff_data = []
        for item in results["mismatch"]:
            diff_data.append({"差异详情": item})

        for item in results["not_in_file1"]:
            diff_data.append({"差异详情": f"仅在数据源2中存在: {item}"})

        for item in results["not_in_file2"]:
            diff_data.append({"差异详情": f"仅在数据源1中存在: {item}"})

        # 如果没有差异，添加一条说明
        if not diff_data:
            diff_data.append({"差异详情": "没有发现差异"})

        diff_df = pd.DataFrame(diff_data)

        # 保存报告 - 先写入头部注释，再写入CSV数据
        with open(report_file, "w", encoding="utf-8-sig") as f:
            # 写入头部注释
            for line in header_comments:
                f.write(line + "\n")

            # 写入CSV数据，使用line_terminator参数避免额外空行
            diff_df.to_csv(f, index=False, encoding="utf-8-sig", line_terminator="\n")

        print(f"📝 差异报告已保存至: {report_file}")

    return results


# 示例用法 - Excel文件比较模式
# two_file_diff(
#     r"D:\源生命标签\new生命标签_4_2025-12-08.xlsx",
#     r"D:\源生命标签\生命标签_4_2025-12-08.xlsx",
#     "商品编码",
#     None,
#     None,
#     True,
#     r"D:\workspace\tools\src\data\生命标签diff_report3.csv",
# )

# 示例用法 - Excel Sheet比较模式
# two_file_diff(
#     file1_path=None,  # 在sheet模式下不需要
#     file2_path=None,  # 在sheet模式下不需要
#     key_column="商品编码",
#     sheet1="Sheet1",
#     sheet2="Sheet2",
#     output_report=True,
#     compare_mode="sheet",
#     file_path_for_sheet=r"D:\源生命标签\生命标签_4_2025-12-08.xlsx"
# )

# 示例用法 - CSV文件比较模式
# two_file_diff(
#     file1_path=r"D:\data\file1.csv",
#     file2_path=r"D:\data\file2.csv",
#     key_column="ID",
#     output_report=True,
#     file_type="csv",
#     delimiter=","
# )

# 示例用法 - TXT文件比较模式
# two_file_diff(
#     file1_path=r"D:\data\file1.txt",
#     file2_path=r"D:\data\file2.txt",
#     key_column="ID",
#     output_report=True,
#     file_type="txt",
#     delimiter="\t"
# )
