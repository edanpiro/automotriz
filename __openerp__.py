# coding= utf-8

{
    "name": "Sur Motors",
    "version": "1.0",
    "depends": [
        "base", "sale", "fleet", "hr",
        "mrp", "mrp_operations", "product_manufacturer"
    ],
    "auhtor": "Edgard Pimentel - SIDET",
    "website": "",
    "category": "Module Customized",
    "description": "Vehiculos",
    'init_xml': [
        "security/ir.model.access.csv",
        "sale/sale_view.xml",
        "res_partner/res_partner_view.xml",
        "fleet/fleet_view.xml",
        "fleet/surmotors_contract_workflow.xml",
        "surmotors_bahias/surmotors_bahia_view.xml",
        #"surmotors_bahias/surmotors_bahia_workflow.xml",
        "mrp/mrp_view.xml",
        "product/product_view.xml",
        "purchase/purchase_view.xml",
        "stock/stock_view.xml"
    ],
    'installable': True,
    'active': False
}
