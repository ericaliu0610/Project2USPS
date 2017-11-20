import urllib
# import urllib2
import xmltodict
import config as cfg


# trackNum number exmaple : "9405510200883557547244"
# reference : https://www.usps.com/business/web-tools-apis/track-and-confirm-api.htm

def sendRequest(trackNum):
    """
    :param trackNum: a format correct tracking number, it should be a String
    :return: 
    """

    USERID = cfg.boya_userid
    URL = "http://production.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML="
    XMLContent = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><TrackFieldRequest USERID=\"xxxxxxxx\"><TrackID ID=\"XXXXXXXXXXXX1\"></TrackID></TrackFieldRequest>"

    # replace user id and track#
    XMLContentReplace = XMLContent.replace("xxxxxxxx", USERID)
    XMLContentReplace = XMLContentReplace.replace("XXXXXXXXXXXX1", trackNum)

    # quote xml <> content
    xmlContentQuote = urllib.parse.quote(XMLContentReplace)

    # begin request from usps
    # TODO check restrictions and limit request
    r = urllib.request.Request(URL + xmlContentQuote, headers={'Content-Type': 'application/xml'})
    try:
        u = urllib.request.urlopen(r)
        resp = u.read()

        traj = xmltodict.parse(resp)

        try:
            return traj["TrackResponse"]["TrackInfo"]

        except KeyError:

            print("Invalid tracking #: " + str(trackNum))
            return {}

    except urllib.error.URLError as e:

        print(type(e))
        return {}

    except Exception as e:

        print(type(e))
        return {}
