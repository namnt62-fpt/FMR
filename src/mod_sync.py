from mod_sync_codelist import sync_codelist
from mod_sync_concept import sync_concept
from mod_sync_datastructure import sync_datastructure
from mod_sync_dataflow import sync_Dataflow
from mod_sync_dataconstraint import sync_dataconstraint


# Đồng bộ Codelist
X = sync_codelist.Codelist()
Y = sync_concept.conceptscheme()
Z = sync_datastructure.DataStructure()
J = sync_Dataflow.Dataflow()
K = sync_dataconstraint.DataConstraint()