## 1.1.0

* Allow renaming nodes
* Massivly improve widgets
    * They are no longer duplicated as slots (use convert to input if you want that)
    * They now use the defaults and settings of whatever node the inputs are connected to in the subgraph   
        * Hence inherithing its defaults, better way to set defaults for subgraph to come.
    * Combos now work so you can pick a checkpoint directly on the node
        * NOTE: This requires the input node to be connected directly to a node with a checkpoint dropdown.


## 1.0.0

* Added better error reporting
* Avoid the flash of a literall 100 outputs on some nodes when loading (and when errors happen)
* Subgraphs should now only rerun when a change to the workflow file is made (or a subworkflow of it again is changed), instead of always beign executed.
* Fix encoding issues running/loading subgraphs containing emoji
