# 📢 Repository Archived
I haven’t used ComfyUI in months, and maintaining this plugin has become more of a chore than a passion. The JS side of this codebase is a long list of hacks to work around ComfyUI’s quirks, and I no longer have the time or energy to keep up with it.

If anyone is interested in taking over the repo, feel free to open an issue, and we can discuss it. Otherwise, consider this project archived.

Thanks to everyone who used or contributed to it! 🚀


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

## Star History

<a href="https://star-history.com/#vivax3794/ComfyUI-Sub-Nodes&Timeline">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=vivax3794/ComfyUI-Sub-Nodes&type=Timeline&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=vivax3794/ComfyUI-Sub-Nodes&type=Timeline" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=vivax3794/ComfyUI-Sub-Nodes&type=Timeline" />
 </picture>
</a>
