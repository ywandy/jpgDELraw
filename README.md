# JPG与RAW文件同步删除工具

这个Python工具用于将RAW目录中那些在JPG目录中不存在对应文件的RAW文件移动到系统回收站。

## 功能特点

- 支持通配符模式指定JPG和RAW文件路径
- 基于文件名（不包含扩展名）进行匹配
- 预览功能，显示将要移动到回收站的文件列表
- 安全确认机制，防止误操作
- 默认预览模式，仅显示不移动
- 文件移动到系统回收站，可恢复
- 详细的操作统计信息

## 命令行参数

```bash
python jpg_del_raw.py --jpg-dir <JPG文件模式> --raw-dir <RAW文件模式> [选项]
```

### 必需参数

- `--jpg-dir`: JPG文件的通配符模式，例如 `"./photos/*.jpg"` 或 `"./exported/*.jpeg"`
- `--raw-dir`: RAW文件的通配符模式，例如 `"./raw/*.rw2"` 或 `"./raw/*.cr2"`

### 可选参数

- `--delete`: 实际删除文件到回收站（默认为预览模式）
- `--auto-confirm`: 自动确认删除操作，跳过用户确认提示

## 使用方法

### 基本用法（预览模式，默认不移动）

```bash
python jpg_del_raw.py --jpg-dir "./jpg/*.jpg" --raw-dir "./raw/*.rw2"
```

### 移动文件到回收站

```bash
python jpg_del_raw.py --jpg-dir "./jpg/*.jpg" --raw-dir "./raw/*.rw2" --delete
```

### 指定不同的文件扩展名

```bash
python jpg_del_raw.py --jpg-dir "./photos/*.jpeg" --raw-dir "./raw/*.cr2" --delete
```

### 自动确认移动（跳过确认提示）

```bash
python jpg_del_raw.py --jpg-dir "./jpg/*.jpg" --raw-dir "./raw/*.rw2" --delete --auto-confirm
```

### 支持的RAW格式

- .rw2 (Panasonic)
- .cr2, .cr3 (Canon)
- .nef (Nikon)
- .arw (Sony)
- .dng (Adobe DNG)
- 等其他RAW格式

## 使用示例

1. **预览不匹配的Panasonic RAW文件:**
   ```bash
   python jpg_del_raw.py --jpg-dir "./exported/*.jpg" --raw-dir "./raw/*.rw2"
   ```

2. **移动不匹配的Canon RAW文件到回收站:**
   ```bash
   python jpg_del_raw.py --jpg-dir "./processed/*.jpeg" --raw-dir "./raw/*.cr2" --delete
   ```

3. **预览Nikon RAW文件:**
   ```bash
   python jpg_del_raw.py --jpg-dir "./photos/*.jpg" --raw-dir "./raw/*.nef"
   ```

4. **处理多个子目录中的文件:**
   ```bash
   python jpg_del_raw.py --jpg-dir "./photos/**/*.jpg" --raw-dir "./raw/**/*.rw2" --delete
   ```

5. **自动确认删除，无需手动确认:**
   ```bash
   python jpg_del_raw.py --jpg-dir "./jpg/*.jpg" --raw-dir "./raw/*.cr3" --delete --auto-confirm
   ```

## 输出示例

### 预览模式输出
```
JPG与RAW文件同步删除工具
========================================
JPG文件模式: ./photos/*.jpg
RAW文件模式: ./raw/*.rw2
运行模式: 预览模式

在JPG目录中找到 150 个文件
在RAW目录中找到 200 个文件
其中 50 个文件在JPG目录中没有对应文件

以下RAW文件将被移动到回收站：
--------------------------------------------------
  1. ./raw/IMG_001.rw2 (25.30 MB)
  2. ./raw/IMG_005.rw2 (24.85 MB)
  3. ./raw/IMG_010.rw2 (26.12 MB)
  ...
--------------------------------------------------
总计: 50 个文件，1250.45 MB

[预览模式] 如需将文件移动到回收站，请添加 --delete 参数
```

### 删除模式输出
```
JPG与RAW文件同步删除工具
========================================
JPG文件模式: ./photos/*.jpg
RAW文件模式: ./raw/*.rw2
运行模式: 回收站模式

在JPG目录中找到 150 个文件
在RAW目录中找到 200 个文件
其中 50 个文件在JPG目录中没有对应文件

以下RAW文件将被移动到回收站：
--------------------------------------------------
总计: 50 个文件，1250.45 MB

确定要将这些文件移动到回收站吗? (y/n): y

开始将文件移动到回收站...
✓ 已移动到回收站: ./raw/IMG_001.rw2
✓ 已移动到回收站: ./raw/IMG_005.rw2
...

操作完成: 成功移动到回收站 50 个，失败 0 个
```

## 工作原理

1. 使用通配符模式扫描JPG文件，获取所有文件的基础名称（不含扩展名）
2. 使用通配符模式扫描RAW文件，找出基础名称不在JPG文件集合中的文件
3. 显示预览列表，包含文件路径和大小信息
4. 用户确认后将孤立的RAW文件移动到系统回收站

## 安全特性

- **默认预览模式**: 默认只预览，需要 `--delete` 参数才实际移动文件
- **回收站功能**: 文件移动到系统回收站，可以恢复
- **预览功能**: 移动前显示完整的文件列表和文件大小
- **确认机制**: 需要用户确认才会执行移动操作
- **错误处理**: 移动失败时显示详细错误信息

## 重要注意事项

⚠️ **关键要点**: 

### 通配符模式说明
- `--jpg-dir` 和 `--raw-dir` 参数使用**通配符模式**，不是目录路径
- 必须包含文件扩展名，例如 `"./photos/*.jpg"` 而不是 `"./photos/"`
- 支持递归搜索，使用 `**` 模式，例如 `"./photos/**/*.jpg"`
- 路径中包含空格时，请使用引号包围整个路径

### 安全提示
- 文件移动到回收站，可以从回收站恢复
- 程序默认为预览模式，使用 `--delete` 参数才会实际移动文件
- 建议先运行预览模式查看将要删除的文件
- 确保重要文件有备份

### 文件匹配规则
- 基于文件名（不含扩展名）进行匹配
- 例如：`IMG_001.jpg` 和 `IMG_001.rw2` 会被认为是匹配的
- 大小写敏感匹配

## 安装和使用

### 系统要求

- Python 3.6+
- send2trash 库（用于回收站功能）

### 快速安装

运行自动安装脚本：

```bash
python install.py
```

### 手动安装依赖

```bash
pip install -r requirements.txt
```

或：

```bash
pip install send2trash
```

### 测试程序

运行测试脚本验证功能：

```bash
python test_trash.py
```

### 快速测试

创建测试文件并运行工具：

```bash
# 运行示例脚本（会创建测试文件并演示功能）
python example.py

# 或手动测试
mkdir -p test_jpg test_raw
touch test_jpg/photo001.jpg test_jpg/photo002.jpg
touch test_raw/photo001.rw2 test_raw/photo002.rw2 test_raw/photo003.rw2

# 预览模式测试
python jpg_del_raw.py --jpg-dir "./test_jpg/*.jpg" --raw-dir "./test_raw/*.rw2"

# 清理测试文件
rm -rf test_jpg test_raw
```
