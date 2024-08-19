# LATTE Bulk importer. 

This tool is designed to load different CSVs into a NEO4J cypher database. Each subtype of nodes are supposed to be stored in their own CSV file. Across all those files nodes are to be identified with a unique ID.

Edges are imported and connected to the proper nodes by referencing those unique IDs. The designated file for edge information holds no edge properties other than a string representing the label of the relation!

## Data preparation. 
Data has to be prepared using a tool of your choice (e.g. open refine). There are some constraints in place when using this tool. 
1) Used quote symbol = "
2) Used delimiter = ,
3) Escape symbol = \

When a ```"``` is in the text it's recommended to escape this character by prepending it with ```\```. Similarly if ```\``` is part of the text, it should be escaped by doubling it to ```\\```. Rows are separated using ```,```. To avoid complications commas in your text are best escaped with ```\```.

## Relationship contstraints
Edges are always defined with three values per row. In Latte, edges do not hold aditional properties and they are directional. This means that the order of entering them in the edges CSV-file matters. 

Per row you should have the following three values to define an edge:
1) INTEGER: ID of the node where a relation originates. 
2) INTEGER: ID of the node where the relation ends.
3) STRING: Label of the relation.
The two ID's used when defining an edge are the unique node ID values. 

Some relations have specific (mandatory labels). The schema below holds the edge label between ```[]```. The two node labels are free to choose. The node containing a text might have the label 'TEXT' or 'ARTICLE' and it could be connected to an 'ANNOTATION' or 'MENTION', whatever the nodelabel you choose, the edge label must be ```contains```. Please note that an ENTITY node is never directly connected to a TEXT node! 
- Edge labels starting with ```priv_``` should not be used. 
- The edge labels mentioned beleow are mandatory. 

TEXT -[contains]-> ANNOTATION
ANNOTATION -[references]-> ENTITY (could be PERSON, PLACE, EVENT, LAW,...)
ENTITY -[same_as]-> VARIANT (alternate spellings...)
ENTITY -[see_also]-> EXTERNAL_KB (External Knowledgebase partner (URI)...)


## NODE constraints
Nodes need to have exactly one label. The YAML configuration file needs to be matched up to the config.inc.php file where you define the nodesmodel of LATTE. Nodes ending with the suffic ```_auto``` should not be used.

Node property names need to adhere to the following standards:
- All property names should be in lowercase.
- No property name should start with a number.
- No property name should contain a space.
- No property name should start with the ```priv_```-prefix
- No property should have ```uid``` set as a property, if you have UUIDs generated elsewhere and need to import these, you should do so under another propertyname with datatype ```str```ing



## Installation
TODO