import requests
import urllib.parse
import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

KAMAR_KEY = 'vtku'
KAMAR_USER_AGENT = 'KAMAR/ Linux/ Android/'
KAMAR_DATE_FORMAT = '%d/%m/%Y'
KAMAR_DEBUG = False


class Notices:
    date: str
    notices: list or None = None
    errorMessage: str or None = None

    def __init__(self, date: str) -> None:
        """
        :param date: The date this notices response is for
        """
        self.date = date

    def is_success(self):
        return self.errorMessage is not None and self.notices is not None


class Notice:
    level: str
    subject: str
    body: str
    teacher: str

    def __init__(self, level: str, subject: str, body: str, teacher: str) -> None:
        """

        A Notice object

        :param level: The level of user this notice is targeted to
        :param subject: The subject/title content of the notice
        :param body: The body/content of the notice
        :param teacher: The teacher that posted the notice
        """
        self.level = level
        self.subject = subject
        self.body = body
        self.teacher = teacher

    def __str__(self) -> str:
        return "Notice{" \
               "Level=" + self.level + \
               ", Subject=" + self.subject + \
               ", Body=" + self.body + \
               ", Teacher=" + self.teacher + "}"


class MeetingNotice(Notice):
    place: str
    date: str
    time: str

    def __init__(self, level: str, subject: str, body: str, teacher: str, place: str, date: str, time: str):
        """
        A Meeting notice object

        :param level: The level of user this notice is targeted to
        :param subject: The subject/title content of the notice
        :param body: The body/content of the notice
        :param teacher: The teacher that posted the notice
        :param place: The place where this notice will occur
        :param date: The date this notice is for
        :param time: The time this notice is for (can be blank)
        """
        super().__init__(level, subject, body, teacher)
        self.place = place
        self.date = date
        self.teacher = time

    def __str__(self) -> str:
        return "MeetingNotice{" \
               "Level=" + self.level + \
               ", Subject=" + self.subject + \
               ", Body=" + self.body + \
               ", Teacher=" + self.teacher + \
               ", Place=" + self.place + \
               ", Date=" + self.date + \
               ", Time=" + self.time + \
               "}"


class KNI:
    url: str  # The url for requests

    def __init__(self, host: str, is_https: bool = True) -> None:
        """
        :param host:The host domain of the KAMAR Portal (e.g portal.your.school.nz)
        or provide the full url https://portal.yours.school.nz
        :param is_https:
        """
        # Add protocol if missing from host
        if not host.startswith('https://') or not host.startswith('http://'):
            host = f"{'https' if is_https else 'http'}://{host}"
        # Add trailing slash if missing
        if not host.endswith('/'):
            host += '/'
        # Add route to api path
        host += 'api/api.php'
        self.url = host

    def retrieve(self, date: str or None) -> Notices or None:
        if date is None:
            time = datetime.date.today()
            date = time.strftime(KAMAR_DATE_FORMAT)
        """
        Retrieves notices for the specified date

        :param date: The date to retrieve notices for or none for the current date
        :return: 
        """
        notices_object = Notices(date)
        content = urllib.parse.urlencode({
            'Key': KAMAR_KEY,
            'Command': 'GetNotices',
            'ShowAll': 'YES',
            'Date': date
        })
        response = requests.post(self.url,
                                 headers={'User-Agent': KAMAR_USER_AGENT,
                                          'Content-Type': 'application/x-www-form-urlencoded'},
                                 data=content)
        if response.status_code == 200:
            if KAMAR_DEBUG:
                print(response.text)
            el = ET.fromstring(response.text)
            error_element = el.find('Error')
            if error_element is not None:
                notices_object.errorMessage = error_element.text
                return notices_object

            notices: list = []

            elements: list = []

            meeting_notices = el.find('MeetingNotices')
            if meeting_notices is not None:
                meeting_elements = meeting_notices.findall('Meeting')
                elements.extend(meeting_elements)

            general_notices = el.find('GeneralNotices')
            if general_notices is not None:
                general_elements = general_notices.findall('General')
                elements.extend(general_elements)

            element: Element
            for element in elements:
                is_meeting = element.tag == 'Meeting'
                # General Notice
                level: str or None = None
                subject: str or None = None
                body: str or None = None
                teacher: str or None = None
                # Meeting Notice
                place: str or None = None
                date: str or None = None
                time: str or None = None

                child: Element
                for child in element:
                    name = child.tag
                    text: str or None = child.text
                    if text is None:
                        text = ''
                    if name == 'Level':
                        level = text
                    elif name == 'Subject':
                        subject = text
                    elif name == 'Body':
                        body = text
                    elif name == 'Teacher':
                        teacher = text
                    elif name == 'PlaceMeet':
                        place = text
                    elif name == 'DateMeet':
                        date = text
                    elif name == 'TimeMeet':
                        time = text

                if None in [level, subject, body, teacher] or is_meeting and None in [place, date, time]:
                    print('Bad notice')
                    continue

                if is_meeting:
                    notices.append(MeetingNotice(level, subject, body, teacher, place, date, time))
                else:
                    notices.append(Notice(level, subject, body, teacher))

            notices_object.notices = notices
            return notices_object
        else:
            raise IOError('Unable to connect to the KAMAR portal')
