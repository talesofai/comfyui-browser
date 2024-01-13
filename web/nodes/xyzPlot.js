import { app } from "../../../scripts/app.js";

const xyzPlotNodeType = 'XyzPlot //Browser';

app.registerExtension({
  name: "Browser.Nodes.XyzPlot",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name != xyzPlotNodeType) {
      return;
    }
    const orig = nodeType.prototype.onExecuted;
    nodeType.prototype.onExecuted = function(message) {
      const ret = orig?.apply(this, arguments);

      const resultPath = message.result_path[0];
      if (!resultPath) {
        return ret;
      }

      let button = this.widgets.find(w => w.type === 'button');
      const callback = () => { window.open(window.location.origin + resultPath, "_blank"); };
      if (!button) {
        this.addWidget("button", 'Open the result', '', callback);
      } else {
        button.callback = callback;
      }

      return ret;
    };
  },
});
