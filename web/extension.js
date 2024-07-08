import { ComfyApp, app } from "../../scripts/app.js";
import { api } from "../../../scripts/api.js"
import {ComfyWidgets} from "../../../scripts/widgets.js";

const original = app.graphToPrompt;
app.graphToPrompt = async function() {
    let {workflow, output} = await original.apply(this)
    workflow.api_prompt = output
    return {workflow, output}
}

let executing_title = "OH NO, NO DATA!"

app.registerExtension({
    name: "Viv.Subgraph",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "VIV_Subgraph_Outputs") {
            nodeType.prototype.onNodeCreated = async function () {
                this.addInput("*", "*")

                setTimeout(() => {
                    if (this.graph) {
                        if (this.graph.findNodesByType("VIV_Subgraph_Outputs").length > 1) {
                            this.graph.remove(this);
                            alert("Subgraphs cant have multiple outputs\nif you wish to reset the outputs delete the original node first.");
                        };
                    }
                }, 100)
            }

            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info, node_slot) {
                if (!link_info) return;

                if (type == 1 && connected) {
                    if (node_slot.name == "*") {
                        this.addInput("*", "*")
                        const from_node = this.graph.getNodeById(link_info.origin_id);
                        if (from_node) {
                            const from_slot = from_node.outputs[link_info.origin_slot];
                            if (from_slot) {
                                node_slot.type = from_slot.type;
                                node_slot.name = `${from_slot.type}.${from_slot.name}.${(Math.random() * 100).toFixed()}`;
                            }
                        }
                    }

                }
            }
        }
        if (nodeData.name === "VIV_Subgraph_Inputs") {
            nodeType.prototype.onNodeCreated = async function () {
                setTimeout(() => {
                    if (this.graph) {
                        if (this.graph.findNodesByType("VIV_Subgraph_Inputs").length > 1) {
                            this.graph.remove(this);
                            alert("Subgraphs cant have multiple inputs\nif you wish to reset the inputs delete the original node first.");
                        };
                    }
                }, 100)

                if (this.outputs) {
                    while (this.outputs.length > 0) {
                        if (this.outputs[this.outputs.length - 1].type == "*") {
                            this.removeOutput(this.outputs.length - 1);
                        }
                    }
                }
                this.addOutput("*", "*")
            }

            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info, node_slot) {
                if (!link_info) return;

                if (type == 2 && connected) {
                    if (node_slot.name == "*") {
                        this.addOutput("*", "*")
                        const from_node = this.graph.getNodeById(link_info.target_id);
                        if (from_node) {
                            const from_slot = from_node.inputs[link_info.target_slot];
                            if (from_slot) {
                                node_slot.type = from_slot.type;
                                node_slot.name = `${from_slot.type}.${from_slot.name}.${(Math.random() * 100).toFixed()}`;
                            }
                        }
                    }
                }
            }
        }
        if (nodeData.name === "VIV_Subgraph") {
            const onDrawForeground = nodeType.prototype.onDrawForeground;
            nodeType.prototype.onDrawForeground = async function(ctx) {
                const r = onDrawForeground?.apply?.(this, arguments);
                ctx.save();

                if (app.runningNodeId == this.id) {
                    const sz = ctx.measureText(executing_title);
                    ctx.fillStyle = "dodgerblue"
                    ctx.beginPath();
                    ctx.roundRect(0, -LiteGraph.NODE_TITLE_HEIGHT - 20, sz.width + 12, 20, 5);
                    ctx.fill();

                    ctx.fillStyle = "#fff";
                    ctx.fillText(executing_title, 6, -LiteGraph.NODE_TITLE_HEIGHT - 6);
                }
                ctx.restore();
                return r;
            }
            nodeType.prototype.onNodeCreated = async function () {
                const node = this;
                const widget = this.widgets[0];
                let value = widget.value;

                this.addWidget("button", "open", undefined, () => {
                    let new_tab = window.open(window.location);

                    new_tab.addEventListener('load', function () {
                        const tab = this;
                        setTimeout(async function() {
                            let name = value.split(".")[0];
                            let data = await api.fetchApi(`/viv/subgraph?workflow=${name}`);
                            let workflow = await data.json();
                            tab.app.loadGraphData(workflow, true, true, value)
                        }, 500);
                    });
                });

                const timeout_id = setTimeout(() => load_input_outputs(node, value), 100);
                
                Object.defineProperty(widget, "value", {
                    get() {
                        return value;
                    },
                    set(newVal) {
                        if (newVal !== value) {
                            value = newVal;
                            load_input_outputs(node, value);
                            clearTimeout(timeout_id);
                        }
                    }
                })
            }
        }
        if (nodeData.name === "VIV_Default") {
            nodeType.prototype.onConnectionsChange = function (type, index, connected, link_info, node_slot) {
                if (!link_info) return;

                if (type == 1 && connected) {
                    const from_node = this.graph.getNodeById(link_info.origin_id);
                    if (from_node) {
                        const from_slot = from_node.outputs[link_info.origin_slot];
                        if (from_slot) {
                            for (let i = 0; i < 2; i++) {
                                this.inputs[i].type = from_slot.type;
                            }
                            this.outputs[0].type = from_slot.type;
                        }
                    }
                }
                if (type == 2 && connected) {
                    const from_node = this.graph.getNodeById(link_info.target_id);
                    if (from_node) {
                        const from_slot = from_node.inputs[link_info.target_slot];
                        if (from_slot) {
                            for (let i = 0; i < 2; i++) {
                                this.inputs[i].type = from_slot.type;
                            }
                            this.outputs[0].type = from_slot.type;
                        }
                    }

                }
            }
        }
    },
})

async function load_input_outputs(node, value) {
    let name = value.split(".")[0];

    let response = await api.fetchApi(`/viv/input_outputs?workflow=${name}`);
    let {outputs, inputs} = await response.json();


    if (node.outputs) {
        while (node.outputs.length > outputs.length) {
            node.removeOutput(node.outputs.length - 1);
        }
    }
    while (node.outputs.length < outputs.length) {
        node.addOutput("*", "*");
    }

    let i = 0;
    for (const output of outputs) {
        let type = output.split(".")[0];
        node.outputs[i].type = type;
        node.outputs[i].name = output;
        i++;
    }

    if (node.inputs) {
        while (node.inputs.length > inputs.length) {
            node.removeInput(node.inputs.length - 1);
        }
    }
    while ((node.inputs?.length || 0) < inputs.length) {
        node.addInput("*", "*");
    }

    node.widgets.splice(2);
    i = 0;
    for (const input of inputs) {
        node.inputs[i].type = input.type;
        node.inputs[i].name = input.name;
        i++;

        if (input.type == "COMBO") {
            continue;
        }

        let widget_func = ComfyWidgets[input.name.toLowerCase().includes("seed") ? "INT:seed" : input.type];
        if (widget_func !== undefined) {
            let widget = widget_func(node, input.name, [input.type, {}], app).widget;
            Object.defineProperty(widget, "value", {
                get() {
                    return node.properties[input.name];
                },
                set(newVal) {
                    node.properties[input.name] = newVal;
                }
            })
        }
    }
}

let last_idempt = -1;

api.addEventListener("/viv/subgraph/executing", ({ detail }) => {
    let { title, idempt } = detail;
    if (idempt > last_idempt) {
        last_idempt = idempt;
        executing_title = title;
    }
});
