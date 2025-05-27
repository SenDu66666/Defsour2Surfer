import glob
import os
import re
import pyproj

def utm_to_latlon_custom_zone(utm_easting, utm_northing, latitude_origin, longitude_origin):
    """
    Converts UTM coordinates to latitude and longitude using a custom UTM zone
    determined by the origin latitude and longitude.
    """
    # Determine UTM zone and letter
    zone_number = int((longitude_origin + 180) / 6) + 1
    latitude_band = 'CDEFGHJKLMNPQRSTVWXX'[int((latitude_origin + 80) / 8)]

    # Define the PROJ projection string
    p = pyproj.Proj(proj='utm', zone=zone_number, ellps='WGS84', datum='WGS84')

    # Convert UTM to latitude and longitude
    longitude, latitude = p(utm_easting, utm_northing, inverse=True)

    return latitude, longitude

def process_file(filename, latitude_origin, longitude_origin):
    """
    Reads UTM coordinates from a file, converts them to latitude and longitude,
    and writes the results to separate files based on the 7th column value,
    preserving all 8 columns including latitude, longitude, and elevation.
    """
    output_dir = "test/output"
    os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在

    # 构建输出文件名
    output_filename_all = os.path.join(output_dir, os.path.splitext(os.path.basename(filename))[0] + "all.txt")

    # 打开原始文件进行读取
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 合并每两行
    merged_lines = []
    for i in range(2, len(lines) - 95, 2):
        line1 = lines[i].strip()
        line2 = lines[i+1].strip() if i+1 < len(lines) else ""
        merged_line = lines[i].strip() + " " + lines[i+1].strip()

        # 分割成列，只保留前 8 列
        columns = re.split(r"\s+", merged_line)  # 使用正则表达式分割，匹配一个或多个空白字符
        truncated_columns = columns[:8]

        # 使用 tab 分隔符连接
        merged_lines.append("\t".join(truncated_columns))

    # 写入 merged_lines 到 all.txt 文件
    with open(output_filename_all, "w", encoding="utf-8") as f:
        for line in merged_lines:
            f.write(line + "\n")

    # 定义不同类型的行
    strike_lines = []
    dip_lines = []
    tensile_lines = []
    pressure_lines = []

    # 分类行并进行坐标转换
    for line in merged_lines:
        parts = line.split("\t")
        if len(parts) == 8:  # 确保有8列
            try:
                utm_easting = float(parts[0])
                utm_northing = float(parts[1])
                elevation = float(parts[2])

                # Convert UTM to latitude and longitude using custom zone
                latitude, longitude = utm_to_latlon_custom_zone(utm_easting, utm_northing, latitude_origin, longitude_origin)

                if latitude is not None and longitude is not None:
                    # 更新行数据，包含转换后的坐标
                    updated_line = f"{longitude:.8f}\t{latitude:.8f}\t{elevation:.2f}\t{parts[3]}\t{parts[4]}\t{parts[5]}\t{parts[6]}\t{parts[7]}"

                    # 根据第7列的值进行分类
                    value = int(parts[6])
                    if value in [1, -1]:
                        strike_lines.append(updated_line)
                    elif value in [2, -2]:
                        dip_lines.append(updated_line)
                    elif value in [3, -3]:
                        tensile_lines.append(updated_line)
                    elif value in [4, -4]:
                        pressure_lines.append(updated_line)
                else:
                    print(f"Invalid UTM coordinates in line: {line.strip()}")

            except ValueError:
                print(f"Error processing line: {line.strip()}")

    # 写入不同类型的文件
    def write_lines_to_file(lines, suffix):
        output_filename = os.path.join(output_dir, os.path.splitext(os.path.basename(filename))[0] + suffix + ".txt")
        with open(output_filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")

    write_lines_to_file(strike_lines, "strike")
    write_lines_to_file(dip_lines, "dip")
    write_lines_to_file(tensile_lines, "tensile")
    write_lines_to_file(pressure_lines, "pressure")

# Example usage:
latitude_origin = 40.5
longitude_origin = -112.2

# 遍历所有 MD*.txt 文件
for filename in glob.glob("test\input\MD*.txt"):
    process_file(filename, latitude_origin, longitude_origin)
