# from tool.models import Report, HostReport
# import requests

# def find_all_reports():
#     url = "http://localhost:3002/reports" 
#     response = requests.get(url)
#     data = response.json()

#     for i in data:
#         Report.objects.get_or_create(
#             reportId = i['id'],
#             createDate = i['createDate'],
#             message = i['message'],   
#             hosts = len(i['hostReports']),
#             racks = len(i['rackReports']),
#         )


# def get_reports_details(id):
#     find_all_reports()
#     url = "http://localhost:3002/reports" 
#     response = requests.get(url)
#     data = response.json()

#     for i in data:
#         if i['id']==id:
#             print(id)
#             print(i['id'])
#             for report in i['hostReports']:
#                 HostReport.objects.get_or_create(
#                     reportId = Report.objects.get(id = id),
#                     hostId = report['hostId'],
#                     hostName = report['hostName'],
#                     IPAddress = report['IPAddress'],
#                     cpu_usage = round(report['averageCpuUsage'],2),
#                     energyConsumption = round(report['energyConsumption'],2),
#                     operationalCost = round(report['operationalCost'],2),
#                     apparentWastageCost = round(report['apparentWastageCost'],2),
#                     carbonFootprint = round(report['carbonFootprint'],2),
#         )           
#                 #host_reports_to_show = HostReport.objects.filter(reportId = 
#                     #Report.objects.get(id = id)).order_by('-reportId')