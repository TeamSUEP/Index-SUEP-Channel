# Index SUEP Channel

[上海电力大学表白墙](https://user.qzone.qq.com/1399896037/311)的简单公共消息日志，专注于识别图像中的文本。

通过修改配置文件，可用于其他 QQ 空间。

## 开始使用

### 安装依赖

```bash
git clone https://github.com/TeamSUEP/Index-SUEP-Channel.git
cd Index-SUEP-Channel
git worktree add dist dist
poetry install
```

### 修改配置

```bash
cp config.example.toml config.toml
vim config.toml
```

| 配置项               | 说明                                       |
| -------------------- | ------------------------------------------ |
| WORKDIR              | 工作目录，用于存放消息                     |
| FILE                 | 消息文件名                                 |
| AUTO_SAVE            | 自动保存间隔，单位为条，0 为不自动保存     |
| AUTO_SAVE_DIR        | 自动保存目录                               |
| STEP                 | 每次获取的消息条数                         |
| LIMIT                | 最大获取的消息条数                         |
| SLEEP_TIME           | 每次获取消息后的休眠时间，单位为秒         |
| MAX_RETRY            | 最大重试次数                               |
| SEARCH_OFFSET        | 历史消息搜索偏移量，单位为条               |
| UIN                  | 目标 QQ 号                                 |
| NICKNAME             | 目标 QQ 昵称                               |
| COOKIES              | QQ 空间 Cookies                            |
| AUTO_UPDATE          | 是否使用 selenium 自动更新 QQ 空间 Cookies |
| AUTO_UPDATE_HEADLESS | 自动更新是否使用无头模式                   |
| AUTO_UPDATE_FORCE    | 自动更新是否跳过检查强制更新               |
| AUTO_UPDATE_USER     | 用于自动更新 QQ 空间 Cookies 的 QQ 号      |
| AUTO_UPDATE_PASS     | 用于自动更新 QQ 空间 Cookies 的 QQ 密码    |
| AUTO_UPDATE_PROXY    | 用于自动更新 QQ 空间 Cookies 的代理        |
| USE_GPU              | OCR 是否使用 GPU                           |
| USE_MP               | OCR 是否使用多进程                         |
| TOTAL_PROCESS_NUM    | OCR 总进程数                               |

#### QQ 空间 Cookies 获取方法

##### 手动

1. 登录 QQ 空间
2. 打开浏览器开发者工具
3. 切换到控制台标签页
4. 输入 `document.cookie` 并回车
5. 复制输出的内容

##### 自动

1. `poetry install --with ci` 安装 ci 组依赖
2. 在配置中填写 `AUTO_UPDATE_USER` 和 `AUTO_UPDATE_PASS`
3. `poetry run python qzone_login_selenium.py`

### 运行

```bash
poetry run python main.py --new
```

## 许可证

本项目 main 分支根据 MIT 许可证授权，有关详细信息，请参阅 [LICENSE](https://github.com/TeamSUEP/Index-SUEP-Channel/blob/main/LICENSE) 文件。

本项目 dist 分支版权归原作者所有，本项目不对其内容负责。

## 致谢

- [上海电力大学表白墙](https://user.qzone.qq.com/1399896037/311)
- [Qzone-API](https://github.com/SmartHypercube/Qzone-API)
- [translation_grass_history](https://github.com/blueset/translation_grass_history)
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
