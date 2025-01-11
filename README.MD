# DataBrigLite - 数据桥梁轻量化平台

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/nothing4any/DataBrigLite//LICENSE)
[![FastAPI](https://img.shields.io/badge/Framework-FastAPI%200.68.2-brightgreen.svg)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Frontend-Vue.js%203.2.31-%234FC08D.svg)](https://v3.vuejs.org/)
[![GitHub issues](https://img.shields.io/github/issues/nothing4any/DataBrigLite.svg)](https://github.com/nothing4any/DataBrigLite/issues)
[![GitHub stars](https://img.shields.io/github/stars/nothing4any/DataBrigLite.svg?style=social&label=Star)](https://github.com/nothing4any/DataBrigLite/stargazers)

## 目录
- [简介](#简介)
- [特性](#特性)
- [快速开始](#快速开始)
  - [安装](#安装)
  - [配置](#配置)
  - [运行](#运行)
- [使用文档](#使用文档)
- [贡献](#贡献)
- [许可证](#许可证)

## 简介

**DataBrigLite** 是一个专为业务人员设计的轻量化数据请求与处理平台，旨在简化从申请到获取CSV格式数据的整个流程。通过连接业务人员与总部的数据部门，DataBrig提供了便捷的数据提取服务，确保了高效的工作流。

## 特性

- **流畅的体验**：使用vue3+fastapi构建，能够快速相应，异步处理。
- **简便的申请流程**：业务人员可以轻松发起数据提取请求。
- **直观的用户界面**：提供易于使用的界面，使操作更加友好。
- **高效的协作环境**：促进业务人员与数据团队之间的无缝合作。

## 功能
- **用户创建**: 仅限于总部数据管理人员使用admin账户创建。
- **数据提取请求**：业务人员可以轻松发起数据提取请求。
- **数据提取处理**：后台系统负责处理数据提取请求，并返回结果。
- **数据提取结果**：业务人员可以查看数据提取结果及文件下载。
- **数据提取记录**：系统记录数据提取请求和结果，以供查询。

大致功能展示：
- 主页公共功能页

  ![DataBrigLite](https://github.com/nothing4any/DataBrigLite/docs/img/home.png)

- 业务人员处理界面

  ![DataBrigLite](https://github.com/nothing4any/DataBrigLite/docs/img/业务人员处理.PNG.png)

- 数据人员工作空间

  ![DataBrigLite](https://github.com/nothing4any/DataBrigLite/docs/img/数据人员工作空间.PNG.png)

- 数据处理界面

  ![DataBrigLite](https://github.com/nothing4any/DataBrigLite/docs/img/数据处理.PNG.png)

## 快速开始

### 安装

DataBrigLite

1. 克隆仓库:
    ```bash
    git clone https://github.com/nothing4any/DataBrigLite.git
    ```
2. 进入项目目录:
    ```
    cd DataBrigLite
    ```
3. 进入后端service目录
    ```
    cd service
    ```
4. 安装依赖项:
    ```
    pip install -r requirements.txt
    ```
5. 进入前端web目录
    ```
    cd ui
    ```
6. 安装依赖项:
    ```
    npm install
    ```
7. 运行服务:
    ---
    一、前后端分离启动
      - 启动后端服务:
          ```
          uvicorn main:app --reload
          ```
      - 启动前端服务:
          ```
          npm run serve
          ```
    ---
    二、前后端不分离启动
      - 修改vue项目公共路径
        ```
        在ui/vue.config.js文件中修改publicPath为'/ui/'
        ```
      - 前端打包
        ```
        npm run build
        ```
      - 放置静态文件
        ```
        将ui文件夹下的dist文件复制到service/ui/static/目录下
        ```
      - 启动后端服务:
        ```
        uvicorn main:app --reload
        ```
    



## 使用文档 - 配置
详细的使用文档位于链接到使用文档。该文档包含数据库及redis配置的指导[CONFIG.md](https://github.com/nothing4any/DataBrigLite/docs/CONFIG.md) 。

## 贡献
我们欢迎任何形式的贡献！如果您发现了bug或者有改进建议，请提交issue或pull request。更多详情请参阅[CONTRIBUTING.md](https://github.com/nothing4any/DataBrigLite/docs/CONTRIBUTING.md) 。

## 许可证
本项目采用MIT License许可，详情请参阅 [LICENSE](https://github.com/nothing4any/DataBrigLite/LICENSE) 文件。
