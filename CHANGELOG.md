## 1.1.2
* Bug fix: Allow reconnecting from input node to COMBO type after disconnecting it.
* Bug fix: Converting seed widget to input creates slot of type INT instead of "number"
* Bug fix: loading inputs for certain types of workflows
* Bug fix: Loading workflows containing subgraphs with no input slots by default would overwrite widgets converted to slots. 

## 1.1.1
* Bugfixa: for some COMBO widgets

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
