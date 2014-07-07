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
        "vehicle/vehicle.xml",
        "surmotors_sale_order/surmotors_sale_order.xml",
        "surmotors_res_partner/surmotors_res_partner.xml",
        "surmotors_fleet_vehicle/surmotors_fleet_vehicle.xml",
        #"form_carac_autos/form_carac_autos.xml",
        "surmotors_fleet_vehicle_log_contract/surmotors_contract.xml",
        "surmotors_fleet_vehicle_log_contract/surmotors_contract_workflow.xml",
        "surmotors_hr_employee/surmotors_hr_employee.xml",
        "surmotors_bahias/surmotors_bahia_view.xml",
        #"surmotors_bahias/surmotors_bahia_workflow.xml",
        "surmotors_production/surmotors_production_view.xml",
#       "surmotors_fleet_vehicle_product/fleet_vehicle_product.xml",
        "product/surmotors_product_view.xml",
    ],
    'installable': True,
    'active': False
}
