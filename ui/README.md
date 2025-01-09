# 项目名称

## 简介
该项目是一个简化的数据申请平台。用于简化数据申请流程，方便中小公司的业务人员对没有进行报表化的数据提起申请。

## 技术栈
- Vue3
- Element UI Plus

## 安装步骤
1. 克隆项目仓库到本地：
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
2. 安装项目依赖：
   ```bash
   npm install
   ```
3. 启动开发服务器：
   ```bash
   npm run serve
   ```
4. 服务打包
   ```bash
   npm run build
   ```

## 使用说明
1. 人员细分业务人员与数据处理人员，不允许注册，只能使用admin用户创建
2. 发起数据申请，填入申请说明，字段信息，或依据模板提交字段信息
3. 数据处理人员审核申请，通过后，根据需求查询生成csv文件，并上传
4.申请人员查看申请状态，下载数据；对于不合符数据可变更当前流程状态，并提交说明

## 贡献指南
欢迎任何形式的贡献！请遵循以下步骤：
1. Fork 项目仓库。
2. 创建一个新的分支 (`git checkout -b feature/AmazingFeature`)。
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)。
4. 推送到分支 (`git push origin feature/AmazingFeature`)。
5. 打开一个 Pull Request。

## 许可证
本项目采用 [MIT 许可证](LICENSE)。