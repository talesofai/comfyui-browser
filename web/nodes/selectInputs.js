import { app } from "../../../scripts/app.js";

const selectInputsNodeType = 'SelectInputs //Browser';
const SPLITTER = '::';

function getGraphInputs(graph) {
  let inputs = [];
  graph._nodes?.forEach(n => {
    n.widgets?.forEach(w => {
      inputs.push([`#${n.id}`, n.title, w.name].join(SPLITTER));
    });
  });

  return inputs;
}

function refreshPreview(node) {
  let values = [];
  node.widgets.forEach(w => {
    if (w.type === 'combo' && w.name.startsWith('input_')) {
      const v = w.value.split(SPLITTER);
      values.push({
        node_id: v[0].substring(1),
        node_title: v[1],
        widget_name: v[2],
      });
    }
  });
  const preview = node.widgets.find(w => w.name === 'preview');
  preview.value = JSON.stringify(values);
}

function refreshInputs(node, app) {
  const inputs = getGraphInputs(app.graph);
  node.widgets.forEach(w => {
    if (w.type != 'combo') {
      return;
    }

    w.options.values = inputs;
    w.value = inputs[0];
  });
  const size = node.computeSize();
  node.setSize([size[0] * 1.5, size[1]]);

  refreshPreview(node);
}

app.registerExtension({
  name: "Browser.Nodes.SelectInputs",
  nodeCreated(node, app) {
    if (node.constructor.type != selectInputsNodeType) {
      return;
    }

    node.widgets.forEach(w => {
      if (w.name === 'preview') {
        if (w.element) {
          w.element.disabled = true;
        }
      }
      if (w.type === 'combo' && w.name.startsWith('input_')) {
        const oriCallback = w.callback;
        w.callback = () => {
          oriCallback?.apply(arguments);
          refreshPreview(node)
        };
      }
    });
    node.addWidget(
      "button", 'Refresh', '',
      () => refreshInputs(node, app)
    );
    refreshInputs(node, app);
  },
  loadedGraphNode(node, app) {
    if (node.type != selectInputsNodeType) {
      return;
    }

    refreshInputs(node, app);
  }
});
