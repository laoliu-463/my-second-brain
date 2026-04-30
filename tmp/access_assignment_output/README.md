# Access 作业生成结果

这个目录里放了两套东西：

1. `Access作业-机自250X-张某某_数据查询版.accdb`
   - 这是我在当前机器上已经成功生成并验证过的 `accdb`
   - 含 `人员信息表` 和 7 个基础查询
   - 可直接用 Access 打开查看数据和查询

2. `create_access_assignment.vbs` + `run_generate_access.bat`
   - 这是完整窗体版的一键生成脚本
   - 运行后目标文件名是 `Access作业-机自250X-张某某.accdb`
   - 需要本机安装 Microsoft Access，并允许 “信任对 VBA 项目对象模型的访问”

## 当前机器测试结论

- 已确认可用：`Excel`、`ACE OLEDB`、`DAO`
- 已确认不可用：`Access.Application`
- 因此我已经完成了“数据层 accdb 生成 + 查询验证”
- 但“窗体 + 列表框 + VBA 模块自动写入”这一步，必须在装有 Access 的机器上执行

## 生成/验证脚本

- 构建数据查询版：
  - `D:\Docs\Books\my second brain\tools\access_assignment\build_data_access.ps1`
- 验证数据查询版：
  - `D:\Docs\Books\my second brain\tools\access_assignment\verify_access_engine.ps1`

## 备注

- 演示文件 `Access作业演示(64位版).accde` 也已放入本目录，作为老师演示件参考
- 源文件 `source.xls` 已同步到本目录，便于你后续在装有 Access 的环境里直接运行
