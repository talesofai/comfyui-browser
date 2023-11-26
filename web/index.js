import { app } from "../../scripts/app.js";
import { $el, ComfyDialog } from "../../scripts/ui.js";

class BrowserDialog extends ComfyDialog {
  constructor() {
    super();
  }
}



app.registerExtension({
	name: "ComfyUI.Browser",
	init() {
  },
  async setup() {
    const browserDialog = new BrowserDialog();

    app.ui.menuContainer.appendChild(
      $el("button", {
        id: "comfyui-browser-button",
        textContent: "Browser",
        onclick: () => {
          console.log('click browser');
          var iframe = document.createElement('iframe');
          iframe.src = './build/index.html';
          browserDialog.show(iframe);
        },
      })
    );
  },
});
