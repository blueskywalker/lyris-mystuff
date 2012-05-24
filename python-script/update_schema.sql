
UPDATE schema_table
SET listschema = LOAD_FILE('listschema.xml')
WHERE orgSuborgId = 'lyris_fulcrumtechinc' 
