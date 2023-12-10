import { app } from "../../scripts/app.js";
import { $el, ComfyDialog } from "../../scripts/ui.js";
import { api } from "../../scripts/api.js";

const browserUrl = "./browser/web/index.html";

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
      $el("div.comfy-list", {
        style: {
          width: "100%",
          "border-style": "none",
          "margin-bottom": "none",
        }
      }, [
        $el("button", {
          id: "comfyui-browser-button",
          textContent: "Browser",
          title: "Browse and manage your outputs and collections",
          style: {
            "font-size": "20px",
            color: "red !important",
            //color: "var(--descrip-text) !important",
            width: "80%",
          },
          onclick: () => {
            browserDialog.show($el("iframe", {
              src: browserUrl + "?timestamp=" + Date.now(),
              style: {
                width: "100%",
                height: "inherit",
              },
            }));
          },
        }),
        $el("button", {
          id: "comfyui-browser-collect-button",
          textContent: "💾",
          title: "Save workflow to collections",
          style: {
            width: "20%",
            "font-size": "17px",
          },
          onclick: (e) => {
            const saveBtn = e.target;
            const originBtnStyle = saveBtn.style.cssText;

            let filename = "workflow.json";
            const promptFilename = app.ui.settings.getSettingValue(
              "Comfy.PromptFilename",
              true,
            );
            if (promptFilename) {
              filename = prompt("Collect workflow as:", filename);
              if (!filename) return;
              if (!filename.toLowerCase().endsWith(".json")) {
                filename += ".json";
              }
            }
            app.graphToPrompt().then(async p => {
              const json = JSON.stringify(p.workflow, null, 2); // convert the data to a JSON string
              const res = await api.fetchApi("/browser/collections/workflows", {
                method: "POST",
                body: JSON.stringify({
                  filename: filename,
                  content: json,
                }),
              });
              if (res.ok) {
                saveBtn.style = originBtnStyle + "border-color: green;";
              } else {
                saveBtn.style = originBtnStyle + "border-color: red;";
              }
              setTimeout(() => {
                saveBtn.style = originBtnStyle;
              }, 1000);
            });
          },
        }),
      ])
    );

    window.comfyApp = app;
  },
});
