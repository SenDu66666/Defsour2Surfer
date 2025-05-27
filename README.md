# Defsour2Surfer
# Defsour2Surfer

## 简介

`reforma.py` 是一个 Python 脚本，用于将 UTM 坐标转换为经纬度坐标，并将转换后的数据写入不同的文件。该脚本主要用于处理包含 UTM 坐标的地质数据文件，并根据数据的特定属性将其分类到不同的输出文件中。

## 功能

-   **UTM 坐标到经纬度坐标转换：** 使用自定义 UTM 区域将 UTM 坐标转换为经纬度坐标。
-   **数据分类：** 根据第 7 列的值将数据分类到不同的文件中，包括 strike、dip、tensile 和 pressure 类型。
-   **文件处理：** 从输入文件中读取数据，并将转换后的数据写入到输出文件中。
-   **错误处理：** 能够处理无效的 UTM 坐标和处理过程中的错误。

## 使用方法

1.  **安装依赖：** 确保安装了 `pyproj` 库。可以使用 pip 安装：

    ```bash
    pip install pyproj
    ```

2.  **准备输入文件：** 将包含 UTM 坐标的文本文件（例如 `MD*.txt`）放置在 `test/input/` 目录下。

3.  **配置参数：** 在脚本底部，可以设置 `latitude_origin` 和 `longitude_origin` 来定义自定义 UTM 区域。

    ```python
    latitude_origin = 40.5
    longitude_origin = -112.2
    ```

4.  **运行脚本：**

    ```bash
    python reforma.py
    ```

5.  **查看输出结果：** 转换后的数据将保存在 `test/output/` 目录下，包括 `all.txt`（包含所有数据）以及 `strike.txt`、`dip.txt`、`tensile.txt` 和 `pressure.txt`（包含分类后的数据）。

## 文件结构

-   `reforma.py`: 主脚本文件，包含 UTM 坐标转换和文件处理的逻辑。
-   `LICENSE`: 许可证文件，采用 MIT 许可证。
-   `README.md`: 说明文档，提供脚本的介绍和使用方法。
-   `test/input/`: 存放输入文件的目录。
-   `test/output/`: 存放输出文件的目录。

## 函数说明

-   [`utm_to_latlon_custom_zone(utm_easting, utm_northing, latitude_origin, longitude_origin)`](d:\personal_documents\Defsour2Surfer\reforma.py)：将 UTM 坐标转换为经纬度坐标。
-   [`process_file(filename, latitude_origin, longitude_origin)`](d:\personal_documents\Defsour2Surfer\reforma.py)：处理单个文件，读取 UTM 坐标，进行转换，并将结果写入不同的文件。

## 依赖

-   [pyproj](https://pyproj4.github.io/pyproj/stable/): 用于坐标转换。
-   [glob](https://docs.python.org/3/library/glob.html): 用于查找符合特定模式的文件名。
-   [os](https://docs.python.org/3/library/os.html): 用于文件和目录操作。
-   [re](https://docs.python.org/3/library/re.html): 用于正则表达式匹配。

## 目录结构
