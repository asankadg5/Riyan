import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit import script, forms

# Get the current document
doc = __revit__.ActiveUIDocument.Document

# Function to get all model categories in use in the current model
def get_model_categories_in_use(doc):
    model_categories = set()
    for elem in FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements():
        if elem.Category is not None and elem.Category.CategoryType == CategoryType.Model:
            model_categories.add(elem.Category.Name)
    return sorted(list(model_categories))

# Function to join elements
def join_elements(elements_to_join):
    with Transaction(doc, "Join Elements") as trans:
        trans.Start()
        for pair in elements_to_join:
            wall, framing = pair
            if not JoinGeometryUtils.AreElementsJoined(doc, wall, framing):
                JoinGeometryUtils.JoinGeometry(doc, wall, framing)
        trans.Commit()

# Function to unjoin elements
def unjoin_elements(elements_to_unjoin):
    with Transaction(doc, "Unjoin Elements") as trans:
        trans.Start()
        for pair in elements_to_unjoin:
            wall, framing = pair
            if JoinGeometryUtils.AreElementsJoined(doc, wall, framing):
                JoinGeometryUtils.UnjoinGeometry(doc, wall, framing)
        trans.Commit()

# Function to collect elements from user-selected categories
def collect_elements_from_selected_categories(selected_categories):
    elements = []
    for category_name in selected_categories:
        bic = getattr(BuiltInCategory, 'OST_' + category_name.replace(" ", ""))
        category_filter = ElementCategoryFilter(bic)
        collector = FilteredElementCollector(doc).WherePasses(category_filter).WhereElementIsNotElementType().ToElements()
        elements.extend(collector)
    return elements

# Function to pair elements (this should be customized based on your logic)
def get_paired_elements(elements):
    paired_elements = []
    walls = [e for e in elements if e.Category.Name == 'Walls']
    framings = [e for e in elements if e.Category.Name == 'Structural Framing']
    # Simple pairing logic (you need to implement actual logic based on your requirements)
    for wall in walls:
        for framing in framings:
            paired_elements.append((wall, framing))
    return paired_elements

# Main script execution
all_model_categories = get_model_categories_in_use(doc)
selected_categories = forms.SelectFromList.show(all_model_categories,
                                                multiselect=True,
                                                button_name='Select Categories')

if selected_categories:
    elements = collect_elements_from_selected_categories(selected_categories)
    paired_elements = get_paired_elements(elements)
    if paired_elements:
        join_unjoin_choice = forms.CommandSwitchWindow.show(['Join', 'Unjoin'], message='Choose an action:')
        if join_unjoin_choice == 'Join':
            join_elements(paired_elements)
        elif join_unjoin_choice == 'Unjoin':
            unjoin_elements(paired_elements)
