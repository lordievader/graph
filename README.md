# Graph
This is a simple graph building library based on NetworkX.
Aimed at creating classification diagrams.

## Installing the requirements
To install the necessary requirements run:
```
pip3 install -r requirements.txt
```

## Example
First import the module:
```
from graph import Graph
```

Now you can use it to create graphs.
```
root = Graph('DNS TXT records')
verification = Graph(
    'Verification', parent=root,
    attributes={'value': 9667724})
Graph('Google', parent=verification)
Graph('Mailru', parent=verification)

email = Graph('Email', parent=root)
Graph('DKIM', parent=email, attributes={'value': 45247})
Graph('DMARC', parent=email, attributes={'value': 47542})
Graph('SPF', parent=email, attributes={'value': 48736443})

other = Graph(
    'Other', parent=root,
    attributes={'value': 0, 'color': 'yellow'})

root.build()
ax = root.show(figsize=(10, 7))
```

This will build a tree with at the root `DNS TXT records`, and as children
`Verification`, `Email` and `Other`.  `Verification` and `Email` have their own
children. Adding the color attribute changes the default color. If a child is
not given a color attribute it inherits the color of its parent.
