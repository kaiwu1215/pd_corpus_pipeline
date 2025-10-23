# 人民日报语料处理与分析项目（1998.01 与 2025.01–2025.10）

本项目实现以下流程：
1. 将 2025 年 10 月–1 月 与 2025 年 1 月的 **Excel** 转换为 **txt**。
2. 对转换后的 txt 进行**清洗**（去噪、规范化）。
3. 使用 `jieba`（含词性）进行**分词与词性标注**。
4. 对三份**已分词语料**分别执行：
   - **任务1**：字符级相邻二字的点式互信息（PMI）与邻近同现概率。
   - **任务2**：基于词性类别的互信息（相邻词性对）。
5. 对 **1998 年 1 月** 与 **2025 年 1 月** 执行：
   - **任务4**：词频差异对比与新词抽取（2025.01 中出现而 1998.01 未出现的词，支持阈值过滤）。

## 目录结构
```
pd_corpus_pipeline/
├─ data/
│  ├─ raw/      # 原始 Excel 或其他原始文件
│  ├─ txt/      # Excel→txt 的输出位置
│  ├─ clean/    # 清洗后的 txt
│  └─ seg/      # 分词+词性 标注后的 txt（以“词/词性”空格分隔）
├─ outputs/     # 各任务结果：CSV/TSV/可视化等
├─ scripts/
│  ├─ 01_excel_to_txt.py
│  ├─ 02_clean_text.py
│  ├─ 03_segment_pos.py
│  ├─ 04_task1_pmi_adjprob.py
│  ├─ 05_task2_pos_mi.py
│  ├─ 06_task3_freqdiff_newwords.py
│  └─ utils/
│     ├─ io_utils.py
│     ├─ text_utils.py
│     └─ stats_utils.py
├─ run_pipeline.py
├─ requirements.txt
└─ config.yml
```

## 快速开始
1. 安装依赖：`pip install -r requirements.txt`
2. 准备数据：
   - 将 `2025年10月到1月` 与 `2025年1月` 的 Excel 放入 `data/raw/`。
   - 将 `1998年1月` 已分词的 txt 放入 `data/seg/1998_01_seg.txt`（或放其他路径并在命令中指定）。
3. 运行脚本（样例）：
   ```bash
   # 1) Excel 转 txt（列名以 A=标题, B=正文, C=发布时间 为例；可通过参数调整）
   python scripts/01_excel_to_txt.py      --input data/raw/people_daily_2025_oct_to_jan.xlsx      --output data/txt/people_daily_2025_oct_to_jan.txt      --title_col 标题 --content_col 正文 --date_col 发布时间

   python scripts/01_excel_to_txt.py      --input data/raw/people_daily_2025_01.xlsx      --output data/txt/people_daily_2025_01.txt      --title_col 标题 --content_col 正文 --date_col 发布时间

   # 2) 清洗
   python scripts/02_clean_text.py      --input data/txt/people_daily_2025_oct_to_jan.txt      --output data/clean/people_daily_2025_oct_to_jan.clean.txt

   python scripts/02_clean_text.py      --input data/txt/people_daily_2025_01.txt      --output data/clean/people_daily_2025_01.clean.txt

   # 3) 分词 + 词性标注
   python scripts/03_segment_pos.py      --input data/clean/people_daily_2025_oct_to_jan.clean.txt      --output data/seg/people_daily_2025_oct_to_jan.seg.txt

   python scripts/03_segment_pos.py      --input data/clean/people_daily_2025_01.clean.txt      --output data/seg/people_daily_2025_01.seg.txt

   # 4) 任务1、2：对三份“已分词语料”（包含 1998.01）分别执行
   python scripts/04_task1_pmi_adjprob.py --input data/seg/1998_01_seg.txt --output outputs/1998_01_task1
   python scripts/05_task2_pos_mi.py      --input data/seg/1998_01_seg.txt --output outputs/1998_01_task2

   python scripts/04_task1_pmi_adjprob.py --input data/seg/people_daily_2025_01.seg.txt --output outputs/2025_01_task1
   python scripts/05_task2_pos_mi.py      --input data/seg/people_daily_2025_01.seg.txt --output outputs/2025_01_task2

   python scripts/04_task1_pmi_adjprob.py --input data/seg/people_daily_2025_oct_to_jan.seg.txt --output outputs/2025_oct_to_jan_task1
   python scripts/05_task2_pos_mi.py      --input data/seg/people_daily_2025_oct_to_jan.seg.txt --output outputs/2025_oct_to_jan_task2

   # 5) 任务4：1998.01 vs 2025.01
   python scripts/06_task3_freqdiff_newwords.py      --seg_2025 data/seg/people_daily_2025_01.seg.txt      --seg_1998 data/seg/1998_01_seg.txt      --out_dir outputs/task3_1998_vs_2025_01
   ```

> 说明：**任务1**脚本会基于“已分词语料”恢复连续汉字序列，计算**相邻两字**的 PMI 与同现概率；同时区分是否“在同一个词内”的二字对，用于分析“二字构成词”的概率与 PMI 的关系。**任务2**按相邻词的**词性类别**计算互信息。**任务4**对比 2025.01 与 1998.01 的词频差异，并输出 2025.01 中的新词清单。

## 输入/输出格式约定
- Excel→txt：默认每行 `日期\t标题\t正文`。日期无法解析时留空。
- 清洗后 txt：一行一篇文章的纯文本（中文+数字+少量常见符号保留）。
- 分词文件：一行一篇；以空格分隔的 `词/词性` 串（类似 1998.01 的示例）。

## 可调参数
参见 `config.yml` 或各脚本 `--help`。
