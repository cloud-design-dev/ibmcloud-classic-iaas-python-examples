import SoftLayer
from pprint import pprint as pp

class example():

    def __init__(self):
        self.client = SoftLayer.Client()

    def main(self, tracking_id):

        tracking_service = self.client['SoftLayer_Metric_Tracking_Object']
        args = {
            'startDateTime' : '2022-04-16',
            'endDateTime':'2022-04-19',
            'metrics': [{'keyName':'PUBLICIN','summaryType':'counter','name':'vif_1_rx'}],
            'interval':600,
            'returnImage': False
        }
        custom_result = tracking_service.getCustomGraphData(args,id=tracking_id)
        pp(custom_result)

    # For use with a virtual Guest, just change
    # SoftLayer_Hardware_Server here with SoftLayer_Virtual_Guest
    def getTrackingId(self, server_id):
        tracking_id = self.client['SoftLayer_Hardware_Server'].getMetricTrackingObjectId(id=server_id)
        return tracking_id

if __name__ == "__main__":
    main = example()
    # CHANGE THIS
    my_server_id = 1534281
    tracking_id = main.getTrackingId(my_server_id)
    main.main(tracking_id)