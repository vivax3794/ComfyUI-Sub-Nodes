# Subgraph nodes?!

YES! Finally!


https://github.com/vivax3794/ComfyUI-Sub-Nodes/assets/51753506/5d75fdfb-acd2-424f-9ee4-3fa47c9a687c

## Disclaimer

This project is still very young, there are likely a good amount of bugs to be found.
More quality of life stuff will be coming as I have time (and the sanity) to implement them.

## How to use

### Creating subgraph

Create a workflow and use `VIV_Subgraph_Inputs` and `VIV_Subgraph_Outputs` to define the inputs and outputs respectfully. **ANY** object can be passed between subgraphs.

Now create a folder in the root of your comfyui install (i.e next to `custom_nodes`, `models`, etc.) called `subnodes`. And use the normal `Save` button to put your workflows there. (also works with the api format export, but you lose some of the information that way, and it wont load back correctly in the editor).

**NOTE:** this package adds some extra keys to the normal save output to faciliate running the subgraph, as such any workflows saved previously wont work as subgraphs (tho ofc they wouldnt be much use without opening them up and adding the input/output nodes anway)

### Calling subgraphs

Create a `VIV_Subgraph` node and select your subgraph (might need to hit the "Refresh" button first), the input/outputs should then be populated automatically (resize the node a bit and it should snap to a good size automatically). Any progress bars in the subgraph and any previews in the subgraph will show on the subgraph node, but any previews (like image previews) wont.
