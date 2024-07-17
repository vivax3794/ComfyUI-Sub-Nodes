
### 18-07-2024

* Added better error reporting
* Avoid the flash of a literall 100 outputs on some nodes when loading (and when errors happen)
* Subgraphs should now only rerun when a change to the workflow file is made (or a subworkflow of it again is changed), instead of always beign executed.
* Fix encoding issues running/loading subgraphs containing emoji
