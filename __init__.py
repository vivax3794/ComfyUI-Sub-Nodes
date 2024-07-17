from unittest.mock import MagicMock, patch
import random
import os
import json
import pathlib
from aiohttp import web

from rich.console import Console

from execution import PromptExecutor, validate_prompt
import execution
import folder_paths
from server import PromptServer

console = Console(color_system="truecolor", force_terminal=True)

idempt = 0

orignal_input = execution.get_input_data
def new_input(*args):
    global idempt
    try:
        node_id = args[2]
        prompt = args[4]
        class_type = prompt[node_id]["class_type"];
        node_title = f"{class_type} #{node_id}"
        PromptServer.instance.send_sync("/viv/subgraph/executing", {"title": node_title, "idempt": idempt})
        idempt += 1
    except:
        pass

    return orignal_input(*args)
execution.get_input_data = new_input

class WrappedExecutor(PromptExecutor):
    def __init__(self):
        server = MagicMock()
        super().__init__(server)
        self._viv_error = None

    def handle_execution_error(self, *args):
        self._viv_error = args[-1]
        super().handle_execution_error(*args)

SUBNODE_FOLDER = pathlib.Path(folder_paths.base_path) / "subnodes"
if not SUBNODE_FOLDER.exists():
    os.mkdir(SUBNODE_FOLDER)


def get_workflow_names() -> list[str]:
    files = list(SUBNODE_FOLDER.glob("*.json"))
    return [file.name for file in files]

def load_workflow(workflow):
    with open(SUBNODE_FOLDER / workflow, encoding='utf-8') as f:
        data = json.load(f)

    if "api_prompt" in data:
        data = data["api_prompt"]

    return data

def get_outputs(workflow):
    prompt = load_workflow(workflow)
    for node in prompt.values():
        if node["class_type"] == "VIV_Subgraph_Outputs":
            return [key for key in node["inputs"].keys()]
    return []

def get_inputs(workflow):
    with open(SUBNODE_FOLDER / workflow, encoding='utf-8') as f:
        data = json.load(f)

    if "api_prompt" in data:
        prompt = data["api_prompt"]
        extra_data = True
    else:
        prompt = data
        extra_data = False

    for (node_id, node) in prompt.items():
        if node["class_type"] == "VIV_Subgraph_Inputs":
            break;
    else:
        return []

    inputs = {}
    for (id, node) in prompt.items():
        for (name, input) in node["inputs"].items():
            if isinstance(input, list):
                if input[0] == node_id:
                    type_ = "*"

                    prompt_name = name
                    node_name = node["class_type"]

                    if extra_data:
                        for graph_node in data["nodes"]:
                            if str(graph_node["id"]) == id:
                                if "title" in graph_node:
                                    node_name = graph_node["title"]
                                for graph_input in graph_node.get("inputs", []):
                                    if graph_input["name"] == name:
                                        type_ = graph_input["type"]
                                        if "label" in graph_input:
                                            prompt_name = graph_input["label"]

                    display_name = f"{prompt_name}.{node_name}.{id}"
                    inputs[input[1]] = {
                            "name": display_name,
                            "type": type_
                        }

    return [name for (_, name) in sorted(inputs.items(), key=lambda x: x[0])]

class Any(str):
    def __ne__(self, value: object, /) -> bool:
        return False

class AcceptAnyWidgetInput(dict):
    def __contains__(self, key: object, /) -> bool:
        return True

class VIV_Subgraph:
    @classmethod
    def INPUT_TYPES(cls):
        return {
                "required": AcceptAnyWidgetInput({
                    "workflow": (tuple(get_workflow_names()),)
                    }),
                }

    RETURN_TYPES = tuple(Any("*") for _ in range(100))
    RETURN_NAMES = tuple("*" for _ in range(100))
    FUNCTION = "run"
    CATEGORY = "sub_graph"
    OUTPUT_NODE = True

    def run(self, workflow: str, **kwargs):
        global depth

        console.print(f"[cyan]Running subgraph: [/cyan][yellow]{workflow}[/yellow]")
        exe = WrappedExecutor()

        prompt = load_workflow(workflow)
        _, error, outputs, _ = validate_prompt(prompt) 
        if error is not None:
            console.print(f"[red]INVALID SUBGRAPH: {workflow}[/red]")
            console.print(error)
            raise ValueError(f"Invalid subgraph: {error['message']}")

        inputs = get_inputs(workflow)
        input_order = [inp["name"] for inp in inputs]
        kwargs = {key: value for (key, value) in kwargs.items() if key in input_order}
        for inp in inputs:
            if inp["name"] not in kwargs:
                kwargs[inp["name"]] = None
        kwargs = sorted(kwargs.items(), key=lambda x: input_order.index(x[0]))
        kwargs = (value for (_, value) in kwargs)

        INPUTS.append(tuple(kwargs))
        exe.execute(prompt, random.random(), {}, outputs)
        if exe._viv_error is not None:
            console.print(f"[red]ERROR SUBGRAPH: {workflow}[/red]")
            raise exe._viv_error
        results = OUTPUT_RESULTS.pop()

        console.print("[cyan]Subgraph done[/cyan]")

        return tuple(results.values())

    @classmethod
    def IS_CHANGED(cls):
        return True

OUTPUT_RESULTS = []

class VIV_Subgraph_outputs:
    @classmethod
    def INPUT_TYPES(cls):
        return {
                "required": {},
                }

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "run"
    CATEGORY = "sub_graph"
    OUTPUT_NODE = True

    def run(self, **kwargs):
        OUTPUT_RESULTS.append(kwargs)
        return ()

INPUTS = []

class VIV_Subgraph_inputs:
    @classmethod
    def INPUT_TYPES(cls):
        return {
                "required": {},
                }

    RETURN_TYPES = tuple(Any("*") for _ in range(100))
    RETURN_NAMES = tuple("*" for _ in range(100))
    FUNCTION = "run"
    CATEGORY = "sub_graph"
    OUTPUT_NODE = True

    def run(self):
        return tuple(INPUTS.pop())

class VIV_Default:
    @classmethod
    def INPUT_TYPES(cls):
        return {
                "required": {
                    "default": Any("*"),
                    },
                "optional": {
                    "inp": Any("*"),
                    }
                }

    RETURN_TYPES = (Any("*"),)
    RETURN_NAMES = ("result",)
    FUNCTION = "run"
    CATEGORY = "sub_graph"
    OUTPUT_NODE = True

    def run(self, default, inp=None):
        if inp is None:
            return (default,)
        return (inp,)

@PromptServer.instance.routes.get("/viv/subgraph")
async def get_workflow(request):
    workflow = request.rel_url.query["workflow"] + ".json"
    with open(SUBNODE_FOLDER / workflow, encoding='utf-8') as f:
        data = json.load(f)
    return web.json_response(data)

@PromptServer.instance.routes.get("/viv/input_outputs")
async def get_input_outputs(request):
    workflow = request.rel_url.query["workflow"] + ".json"

    response = {
            "outputs": get_outputs(workflow),
            "inputs": get_inputs(workflow)
            }

    return web.json_response(response)

console.print("[green]Sub nodes, yay![/green]")
console.print("[red]WARNING: This is a very experimental setup :P![/red]")

NODE_CLASS_MAPPINGS = {
        "VIV_Subgraph": VIV_Subgraph,
        "VIV_Subgraph_Outputs": VIV_Subgraph_outputs,
        "VIV_Subgraph_Inputs": VIV_Subgraph_inputs,
        "VIV_Default": VIV_Default,
        }

MANIFEST = {
        "name": "VIVAX",
        }
WEB_DIRECTORY = "web"
