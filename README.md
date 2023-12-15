# ComfyUI Browser

This is an image/video/workflow browser and manager for ComfyUI.
You can sync your workflows to a remote Git repository and use them everywhere.

Welcome to submit your workflow source by submitting [an issue](https://github.com/talesofai/comfyui-browser/issues/new?assignees=tzwm&labels=workflow-repo&projects=&template=new-workflow-repository.md&title=New+workflow+repo%3A). Let's build the workflows together.

## Features

- Browse and manage your images/videos/workflows in the output folder.
- Add your workflows to the 'Saves' so that you can switch and manage them more easily.
- Sync your collection anywhere by Git.
- Subscribe workflow sources by Git and load them more easily.
- Search your workflow by keywords.

## Preview

![b359de5f6556649512e7ed8f812ba67d444be9914173e2467018450ce1a3ce1d](https://github.com/talesofai/comfyui-browser/assets/828837/4b0b0f4c-28a8-49ef-98c2-d293df5b7747)
![c91157bf819ef5b9a129976d9e45588106dd6c7ea39ecb0a22519acd72afc7ce](https://github.com/talesofai/comfyui-browser/assets/828837/ee3df970-017c-4825-ab5d-9465cdb77ed6)
![53053f43847da9597efebab207140eed703b8c7bbe8eb1e63ce5630b5d8c9a3f](https://github.com/talesofai/comfyui-browser/assets/828837/4acb522a-f21c-47ad-9a23-56b08c6e73a5)
![c7b93b2ec0891eb7cac1385505e855fb28934ec958f7b21cac53c9bf18e6136c](https://github.com/talesofai/comfyui-browser/assets/828837/ef0d5cd2-9238-4e80-9f65-0f7db05ffbf3)

## Installation

### Comfy Manager

Search for `comfyui-browser` and install it.

### Manually

Clone this repo into the `custom_nodes` folder and restart the ComfyUI.

```bash
cd custom_nodes && git clone https://github.com/tzwm/comfyui-browser.git
```

## Notes

- Your collections are stored in the `ComfyUI/custom_nodes/comfyui-browser/collections`.

## TODO

- [x] Sync collections to remote git repository
- [x] Add external git repository to local collections
- [ ] Search workflow by node name and model name


## ChangeLog

To see [ChangeLog](CHANGELOG.md).


## Credits

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
