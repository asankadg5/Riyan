import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Add References to Revit API
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

# Import from Revit API
from Autodesk.Revit.DB import *

# For using a Transaction (if needed)
clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Set the active document (`doc`) as the current document in Revit.
doc = DocumentManager.Instance.CurrentDBDocument

# Function to get the first linked document
def get_first_linked_document(current_doc):
    # Create a filtered collector for RevitLinkInstances in the current document
    collector = FilteredElementCollector(current_doc).OfClass(RevitLinkInstance)
    # Get all RevitLinkInstances in the document
    linked_instances = collector.ToElements()
    
    if linked_instances:
        # Get the first RevitLinkInstance
        linked_instance = linked_instances[0]
        # Get the Document object of the linked instance
        linked_doc = linked_instance.GetLinkDocument()
        return linked_doc
    else:
        # If no linked instances are found, return None
        return None

# Start using the linked document
linkedDoc = get_first_linked_document(doc)

# Make sure to check if the linkedDoc is not None before using it
if linkedDoc:
    # You can now perform operations on the linked document
    # Example: print the title of the linked document
    print("Linked document title: " + linkedDoc.Title)
else:
    # Handle the case when there are no linked documents
    print("No linked documents found.")

# Note: To make any changes to Revit elements, you must perform those actions
# within a Transaction block. Example:
"""
TransactionManager.Instance.EnsureInTransaction(doc)
# ... Perform actions here ...
TransactionManager.Instance.TransactionTaskDone()
"""
