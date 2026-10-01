# 资产上报 JSON 结构设计

一台机器的资产 = **机器自身的属性（单数）** + **挂载的设备（复数）** + **元信息**。

下面的结构示例取自真实采集输出（TEST_MODE 样例数据），字段值均为实际值。

## 设计原则

1. **同层同形** —— 同一层级的字段形状一致，不出现"有的多包一层、有的没有"
2. **单复数显式** —— 值类型自解释：对象 = 一个，数组 = 多个，消费端不必硬编码"哪个要遍历"
3. **单位进字段名** —— `capacity_mb` 而非 `capacity`，单位不靠猜
4. **类型一致** —— 同名字段跨来源保持同一种类型
5. **成功路径干净** —— 成功时不携带任何状态字段，无冗余
6. **失败集中** —— 采集失败统一落在 `errors`，不污染数据区
7. **可演进** —— 顶层带结构版本号，服务端能判断手里的数据是哪一版

## 结构示例

```json
{
  "schema_version": 1,
  "collected_at": "2026-10-01T15:40:12+08:00",

  "hostname": "c1.com",

  "os": {
    "platform": "Linux",
    "version": "CentOS release 6.6 (Final)"
  },

  "cpu": {
    "model": "Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz",
    "sockets": 2,
    "logical_processors": 24
  },

  "main_board": {
    "manufacturer": "Parallels Software International Inc.",
    "model": "Parallels Virtual Platform",
    "serial": "Parallels-1A 1B CB 3B 64 66 4B 13 86 B0 86 FF 7E 2B 20 30"
  },

  "disks": [
    {
      "slot": "0",
      "type": "SAS",
      "capacity_mb": 286102,
      "model": "SEAGATE ST300MM0006 LS08S0K2B5NV"
    },
    {
      "slot": "1",
      "type": "SAS",
      "capacity_mb": 286102,
      "model": "SEAGATE ST300MM0006 LS08S0K2B5AH"
    }
  ],

  "memory": [
    {
      "slot": "DIMM #0",
      "type": "DRAM",
      "capacity_mb": 1024,
      "speed_mhz": 667,
      "manufacturer": null,
      "serial": null
    }
  ],

  "nics": [
    {
      "name": "eth0",
      "up": true,
      "mac": "00:1c:42:a5:57:7a",
      "ipv4": [
        {
          "address": "10.211.55.4",
          "netmask": "255.255.255.0"
        }
      ]
    }
  ],

  "errors": {}
}
```

## 字段说明

### 元信息

| 字段 | 类型 | 说明 |
|---|---|---|
| `schema_version` | int | 结构版本号，结构变更时递增，服务端据此判断解析方式 |
| `collected_at` | string | 采集时刻，ISO 8601 带时区。资产数据必须具备时效性 |

### 机器属性（对象，单数）

| 字段 | 类型 | 说明 |
|---|---|---|
| `hostname` | string | 主机名 |
| `os.platform` | string | 系统平台，如 `Linux` |
| `os.version` | string | 系统版本 |
| `cpu.model` | string | CPU 型号 |
| `cpu.sockets` | int | 物理 CPU 颗数 |
| `cpu.logical_processors` | int | 逻辑处理器数（含超线程） |
| `main_board.manufacturer` | string \| null | 主板厂商 |
| `main_board.model` | string \| null | 主板型号 |
| `main_board.serial` | string \| null | 主板序列号 |

### 设备列表（数组，复数）

三个设备类统一是**数组**，消费端一律遍历，不需要为每个类写特例。

| 字段 | 类型 | 说明 |
|---|---|---|
| `disks[].slot` | string | 槽位编号 |
| `disks[].type` | string | 接口类型，如 `SAS` / `SATA` |
| `disks[].capacity_mb` | int | 容量，**单位 MB**（独立于原始输出的单位） |
| `disks[].model` | string | 磁盘型号 |
| `memory[].slot` | string | 内存槽位 |
| `memory[].type` | string | 内存类型，如 `DRAM` |
| `memory[].capacity_mb` | int | 容量，**单位 MB** |
| `memory[].speed_mhz` | int | 频率，**单位 MHz** |
| `memory[].manufacturer` | string \| null | 厂商，无则 `null` |
| `memory[].serial` | string \| null | 序列号，无则 `null` |
| `nics[].name` | string | 网卡名 |
| `nics[].up` | bool | 是否 UP |
| `nics[].mac` | string | MAC 地址 |
| `nics[].ipv4` | array | IPv4 地址列表，每项 `{address, netmask}` |

### 错误

| 字段 | 类型 | 说明 |
|---|---|---|
| `errors` | object | 采集失败的项：`{"disks": "失败原因"}`。**成功时为空对象 `{}`**，键名与顶层采集项一致 |

## 三个需要解释的设计决策

**① 设备一律用数组，即使只有一块盘**

```json
"disks": [ { ... } ]     // 而不是 "disk": { ... }
```

值类型（数组 / 对象）就是单复数声明。消费端写 `for d in data["disks"]` 永远成立，
不必知道"cpu 是单个、disk 是多个"。**用结构表达语义，而不是靠文档约定。**

**② 单位写进字段名，且统一换算到同一单位**

```json
"capacity_mb": 286102      // 磁盘，原始是 279.396 GB，换算成 MB
"capacity_mb": 1024        // 内存，原始就是 1024 MB
```

磁盘和内存的容量用**同一个字段名、同一种类型、同一个单位** —— 消费端一套代码处理两类设备。
`capacity` 这种无单位裸数字是歧义的来源。

**③ 空值用 `null`，不用占位符字符串**

```json
"manufacturer": null       // 而不是 "Not Specified"
```

数据源（dmidecode）用 `Not Specified` 占位，透传上去后消费端无法区分"没有这个信息"和"信息就是 Not Specified"。
`null` 才能表达"无"。

## 与现状结构的差异

| 现状 | 本设计 | 原因 |
|---|---|---|
| `hostname` 是裸值，`cpu` 是 `{status,message,data,error}` 包装 | 全部平铺，无包装 | 深度统一；包装层成功时无用、失败时把 traceback 传上去 |
| `cpu.data.cpu_model` | `cpu.model` | 去掉无意义的中间层 |
| `disk` 的对象键是 `"0"` `"1"` | `disks` 是数组，槽位在 `slot` 字段 | 数组语义明确，且不必动态生成键 |
| `capacity` 在 disk 是字符串 `"279.396"`、在 memory 是整数 `1024` | 统一 `capacity_mb`，int | 同名不同型不同单位是最阴的坑 |
| `cpu_count` / `cpu_physical_count` | `logical_processors` / `sockets` | 名称准确表达含义 |
| `nic.ipaddrs` 是 `"/"` 拼接的字符串 | `nics[].ipv4` 是对象数组 | 拼接会丢失 IP 与掩码的配对关系 |
| 空内存槽 `capacity: 0` 也上报 | 只上报已安装的模块 | 空槽不是内存；`0` 分不清"没装"和"容量为 0" |
| 无版本号 | `schema_version` | 结构演进时服务端需要判断 |
| `message: null` / `status: true` 重复 5 次 | 移除 | 成功路径零冗余 |
| 失败时 `error` 是完整 traceback | `errors` 里是简短原因 | traceback 含本地路径和代码行号，不该外传 |
