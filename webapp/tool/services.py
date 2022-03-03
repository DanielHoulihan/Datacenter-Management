from tool.models import CurrentDatacenter, MasterIP, ConfiguredDataCenters

def get_current_sub_id():
    return str(CurrentDatacenter.objects.all().values().get()['current'])

def get_current_datacenter():
    return str(CurrentDatacenter.objects.all().values().get()['current'].split('-')[0])

def get_master():
    return MasterIP.objects.all().values().get()["master"]

def get_current_for_html():
    current = "-"
    if CurrentDatacenter.objects.filter(masterip=get_master()).all().count()!=0:
        current = get_current_sub_id()
    return current

def get_configured():
    return ConfiguredDataCenters.objects.filter(masterip=get_master()).all()

def get_pue():
    return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['pue']

def get_energy_cost():
    return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['energy_cost']

def get_carbon_conversion():
    return ConfiguredDataCenters.objects.filter(masterip=get_master()).filter(sub_id=get_current_sub_id()).all().values().get()['carbon_conversion']