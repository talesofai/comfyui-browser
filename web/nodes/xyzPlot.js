import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

const xyzNodeType = 'XyzPlot|Browser';

app.registerExtension({
  name: "Browser.XyzPlot",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name == xyzNodeType) {
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = async function(message) {
        const res = await api.fetchApi('/test');
        console.log(res);
        console.log(message);
        const ret = onExecuted?.apply(this, arguments);
        console.log(arguments);
        return ret;
      }
    }
  },
});
