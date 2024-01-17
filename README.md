# ComfyUI Browser

[中文说明](README_CN.md)

This is an image/video/workflow browser and manager for ComfyUI.
You can sync your workflows to a remote Git repository and use them everywhere.

Welcome to submit your workflow source by submitting [an issue](https://github.com/talesofai/comfyui-browser/issues/new?assignees=tzwm&labels=workflow-repo&projects=&template=new-workflow-repository.md&title=New+workflow+repo%3A). Let's build the workflows together.

https://github.com/talesofai/comfyui-browser/assets/828837/803ce57a-1cf2-4e1c-be17-0efab401ef54

## Features

- Browse and manage your images/videos/workflows in the output folder.
- Add your workflows to the 'Saves' so that you can switch and manage them more easily.
- Sync your 'Saves' anywhere by Git.
- Subscribe workflow sources by Git and load them more easily.
- Search your workflow by keywords.
- Some useful custom nodes like xyz_plot, inputs_select.

## Custom Nodes

#### Select Inputs

- Select any inputs of the current graph.

<img width="256" alt="image" src="https://github.com/talesofai/comfyui-browser/assets/828837/8e505f62-f709-426a-8a0a-fca291784b08">


#### XYZ Plot

- Simple XYZ Plot by selecting inputs and filling in the values.

<img width="256" alt="image" src="https://github.com/talesofai/comfyui-browser/assets/828837/23ce6a4d-3311-4058-9b46-ddb50d07e22a">

<img width="256" alt="image" src="https://github.com/talesofai/comfyui-browser/assets/828837/347cad17-17c0-46f1-8df3-4b188b16a354">


## Preview


#### Outputs
<img width="1212" alt="Outputs" src="https://github.com/talesofai/comfyui-browser/assets/1184998/49936e2f-9682-4df8-af8e-6e1653e78ca1">

#### Saves
<img width="1207" alt="Saves" src="https://github.com/talesofai/comfyui-browser/assets/1184998/de3327e3-643e-4ae4-9e31-86df6a0353e0">

#### Sources
<img width="1504" alt="Sources" src="https://github.com/talesofai/comfyui-browser/assets/1184998/07671822-c4d1-4327-bd87-6b1c7e85a354">
<img width="1212" alt="Recommended Sources" src="https://github.com/talesofai/comfyui-browser/assets/1184998/f37852b9-1030-4044-abf3-12bd8158c446">

#### Models
<img width="1510" alt="Models" src="https://github.com/talesofai/comfyui-browser/assets/1184998/4f36378e-05e0-49dc-a5b2-07d24a8b96bc">

#### Side Bar View
<img width="1506" alt="SideBar" src="https://github.com/talesofai/comfyui-browser/assets/1184998/746a031e-88b0-4ccf-8e2d-e448c001f319">

## Installation

### ComfyUI Manager

Install [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager), search `comfyui-browser` in Install Custom Node and install it.

### Manually

Clone this repo into the `custom_nodes` folder and restart the ComfyUI.

```bash
cd custom_nodes && git clone https://github.com/tzwm/comfyui-browser.git
```

## Notes

- Your 'Saves' are stored in the `ComfyUI/custom_nodes/comfyui-browser/collections`.
- Press 'B' to toggle the Browser dialog in the ComfyUI.


## Development

- Prerequisite
  - Install [Node](https://nodejs.org/en/download/current)


- Framework

  - Frontend: [Svelte](https://kit.svelte.dev/)
  - Backend: [aiohttp](https://docs.aiohttp.org/)(the same as ComfyUI)

- Project Structure

```
├── __init__.py  (Backend Server)
├── web          (Frontend code loaded by ComfyUI)
    ├── build    (Built in Svelte)
    └── index.js (Frontend that interact with ComfyUI)
├── svelte       (Frontend in the Modal as a iframe, written in Svelte)
```

- Build and Run

  - Copy or link `comfyui-browser` to `ComfyUI/custom_nodes/`
  - Start backend by `cd ComfyUI && python main.py --enable-cors-header`
  - Start frontend by `cd ComfyUI/custom_nodes/comfyui-browser/svelte && npm i && npm run dev`
  - Open and debug by `http://localhost:5173/?comfyUrl=http://localhost:8188`
    - It will use `localhost:8188` as ComfyUI server
    - `localhost:5173` is a Vite dev server

- Notes

  - Please try to test on Windows, because I only have Linux/macOS


## TODO

- [x] Sync collections to remote git repository
- [x] Add external git repository to local collections
- [ ] Search workflow by node name and model name


## ChangeLog

To see [ChangeLog](CHANGELOG.md).


## Credits

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
