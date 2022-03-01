from tool.models import CurrentDatacenter, MasterIP, ConfiguredDataCenters


def get_current_sub_id():
    return CurrentDatacenter.objects.all().values().get()['current']

def get_current_datacenter():
    return CurrentDatacenter.objects.all().values().get()['current'].split('-')[0]

def get_master():
    return MasterIP.objects.all().values().get()["master"]

def get_current_for_html():
    current = "-"
    if CurrentDatacenter.objects.filter(masterip=get_master()).all().count()!=0:
        current = CurrentDatacenter.objects.filter(masterip=get_master()).all().values().get()['current']
    return current

def get_configured():
    return ConfiguredDataCenters.objects.filter(masterip=get_master()).all()