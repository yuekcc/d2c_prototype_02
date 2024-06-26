# d2c prototype 02

Design To Code 原型。

目前已实现：

- [x] 原型图分割
- [x] 组件识别
  - [x] 简单组件：button、input、label、select、close
- [x] 输出结构化数据

效果：

| 输入                  | 输出                   |
| --------------------- | ---------------------- |
| ![](./demo_input.png) | ![](./demo_output.png) |

## 使用

```shell
# 安装依赖，目前只在 windows11+python310 测试
pip install -r requirements.txt

# 更新数据库。一般只需要执行一次
python comp_db.py

# 执行识别脚本
python main.py
```

输出 JSON 数据

```json
[
  {
    "id": "0",
    "cells": [
      {
        "id": "0_0",
        "rect": [5, 18, 68, 21],
        "component_type": "label"
      },
      {
        "id": "0_1",
        "rect": [409, 18, 25, 21],
        "component_type": "close"
      }
    ],
    "rect": [0, 18, 440, 21]
  },
  {
    "id": "1",
    "cells": [
      {
        "id": "1_0",
        "rect": [14, 91, 48, 35],
        "component_type": "label"
      },
      {
        "id": "1_1",
        "rect": [83, 91, 326, 35],
        "component_type": "input"
      }
    ],
    "rect": [0, 91, 440, 35]
  },
  {
    "id": "2",
    "cells": [
      {
        "id": "2_0",
        "rect": [13, 158, 49, 35],
        "component_type": "label"
      },
      {
        "id": "2_1",
        "rect": [83, 158, 326, 35],
        "component_type": "input"
      }
    ],
    "rect": [0, 158, 440, 35]
  },
  {
    "id": "3",
    "cells": [
      {
        "id": "3_0",
        "rect": [169, 265, 138, 36],
        "component_type": "button"
      }
    ],
    "rect": [0, 265, 440, 36]
  }
]
```

## LICENSE

MIT
