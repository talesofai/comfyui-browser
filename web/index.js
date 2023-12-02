import { app } from "../../scripts/app.js";
import { $el, ComfyDialog } from "../../scripts/ui.js";

const browserUrl = "./browser/index.html";

class BrowserDialog extends ComfyDialog {
  constructor() {
    super();

    this.element = $el("div.comfy-modal", {
      id: "comfy-browser-dialog",
      parent: document.body,
      style: {
        width: "100%",
        height: "100%",
        padding: "10px",
      },
    }, [
      $el("div.comfy-modal-content", {
        style: {
          width: "inherit",
          height: "inherit",
        },
      }, [
        $el("div", {
          $: (e) => (this.textElement = e), style: { height: "inherit",
          },
        }),
        ...this.createButtons(),
      ]),
		]);
  }

  createButtons() {
    const closeBtn = $el("button", {
      type: "button",
      textContent: "Close",
      onclick: () => this.close(),
    });
    const browseBtn = $el("a", {
      href: browserUrl,
      target: "_blank",
    }, [
      $el("button", {
        type: "button",
        textContent: "Browse in new tab",
      }),
    ]);
    return [
      $el("div", {}, [
        closeBtn,
        browseBtn,
      ]),
    ];
  }

  close() {
    this.element.style.display = "none";
  }

  show(html) {
    if (typeof html === "string") {
      this.textElement.innerHTML = html;
    } else {
      this.textElement.replaceChildren(html);
    }
    this.element.style.display = "flex";
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
          browserDialog.show($el("iframe", {
            src: browserUrl + "?timestamp=" + Date.now(),
            style: {
              width: "100%",
              height: "inherit",
            },
          }));
        },
      })
    );

    window.comfyApp = app;
  },
});
