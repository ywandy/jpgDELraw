# JPG与RAW文件同步删除工具

这个Python工具用于删除RAW目录中那些在JPG目录中不存在对应文件的RAW文件。

## 功能特点

- 支持通配符模式指定JPG和RAW目录
- 基于文件名（不包含扩展名）进行匹配
- 预览功能，显示将要删除的文件列表
- 安全确认机制，防止误删
- 干运行模式，仅预览不删除
- 详细的删除统计信息

## 使用方法

### 基本用法（预览模式，默认不删除）

```bash
python jpg_del_raw.py --jpg-dir ./jpg --raw-dir ./raw
```

### 实际删除文件

```bash
python jpg_del_raw.py --jpg-dir ./jpg --raw-dir ./raw --delete
```

### 指定文件扩展名

```bash
python jpg_del_raw.py --jpg-dir ./photos --raw-dir ./raw --jpg-ext .jpeg --raw-ext .cr2
```

### 自动确认删除（跳过确认提示）

```bash
python jpg_del_raw.py --jpg-dir ./jpg --raw-dir ./raw --delete --auto-confirm
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
   python jpg_del_raw.py --jpg-dir ./exported --raw-dir ./raw --raw-ext .rw2
   ```

2. **删除不匹配的Canon RAW文件:**
   ```bash
   python jpg_del_raw.py --jpg-dir ./processed --raw-dir ./raw --jpg-ext .jpeg --raw-ext .cr2 --delete
   ```

3. **预览Nikon RAW文件:**
   ```bash
   python jpg_del_raw.py --jpg-dir ./photos --raw-dir ./raw --raw-ext .nef
   ```

## 工作原理

1. 扫描JPG目录，获取所有文件的基础名称（不含扩展名）
2. 扫描RAW目录，找出基础名称不在JPG目录中的文件
3. 显示预览列表，包含文件大小信息
4. 用户确认后执行删除操作

## 安全特性

- **默认预览模式**: 默认只预览，需要 `--delete` 参数才实际删除
- **预览功能**: 删除前显示完整的文件列表和文件大小
- **确认机制**: 需要用户确认才会执行删除
- **错误处理**: 删除失败时显示详细错误信息

## 注意事项

⚠️ **重要警告**: 
- 删除操作不可逆，请谨慎使用
- 程序默认为预览模式，使用 `--delete` 参数才会实际删除
- 确保备份重要文件

## 系统要求

- Python 3.6+
- 无需额外依赖包，使用Python标准库
