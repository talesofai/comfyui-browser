# ComfyUI 浏览器

查看和管理 ComfyUI 的所有输出文件，并且添加收藏方便随时调用。

远程同步工作流到你的 Git 仓库，方便团队共享和版本管理。

还能订阅社区开放的工作流仓库，方便抄作业！

https://github.com/talesofai/comfyui-browser/assets/828837/803ce57a-1cf2-4e1c-be17-0efab401ef54

也可以参考B站的中文解说：
https://www.bilibili.com/video/BV1qc411m7Gp/

## 功能

- 浏览和管理你的 ComfyUI 输出文件
- 添加工作流到收藏夹，方便管理和调用
- 可以通过 Git 来远程同步收藏夹
- 订阅工作流仓库，方便抄作业
- 通过关键词搜索工作流


## 预览

![b359de5f6556649512e7ed8f812ba67d444be9914173e2467018450ce1a3ce1d](https://github.com/talesofai/comfyui-browser/assets/828837/4b0b0f4c-28a8-49ef-98c2-d293df5b7747)
![c91157bf819ef5b9a129976d9e45588106dd6c7ea39ecb0a22519acd72afc7ce](https://github.com/talesofai/comfyui-browser/assets/828837/ee3df970-017c-4825-ab5d-9465cdb77ed6)
![53053f43847da9597efebab207140eed703b8c7bbe8eb1e63ce5630b5d8c9a3f](https://github.com/talesofai/comfyui-browser/assets/828837/4acb522a-f21c-47ad-9a23-56b08c6e73a5)
![c7b93b2ec0891eb7cac1385505e855fb28934ec958f7b21cac53c9bf18e6136c](https://github.com/talesofai/comfyui-browser/assets/828837/ef0d5cd2-9238-4e80-9f65-0f7db05ffbf3)

## 安装方式

### ComfyUI Manager
安装[ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)， 在 Install Custom Node 中搜索 `comfyui-browser` 来安装。

### 手动

下载这个仓库的代码放到 `ComfyUI/custom_nodes` 目录下，并重启 ComfyUI。

```bash
cd custom_nodes && git clone https://github.com/tzwm/comfyui-browser.git
```

## 开发

- 前置需求
  - 安装[Node](https://nodejs.org/en/download/current)

- 使用的框架

  - 前端: [Svelte](https://kit.svelte.dev/)
  - 后端: [aiohttp](https://docs.aiohttp.org/)(和 ComfyUI 一样)

- 目录介绍

```
├── __init__.py  (后端服务)
├── web          (ComfyUI 加载的前端路径)
    ├── build    (Svelte 的生成文件)
    └── index.js (和 ComfyUI 交互的前端代码)
├── svelte       (前端主体部分)
```

- 开发和调试

  - 复制或者链接 `comfyui-browser` 到 `ComfyUI/custom_nodes/`
  - 启动服务端: `cd ComfyUI && python main.py --enable-cors-header`
  - 启动前端: `cd ComfyUI/custom_nodes/comfyui-browser/svelte && npm i && npm run dev`
  - 调试地址 `http://localhost:5173/?comfyUrl=http://localhost:8188`
    - `localhost:8188` 是 ComfyUI server 地址
    - `localhost:5173` 是 Vite dev server

- 备注

  - 请尽量在 Windows 上测试, 因为我只有 Linux 和 macOS
  - 在 ComfyUI 中可以按 'B' 键来打开/关闭 Browser



## 更新记录

详见：[ChangeLog](CHANGELOG.md)

## 感谢

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
